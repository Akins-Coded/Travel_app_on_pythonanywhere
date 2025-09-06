import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status, viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Listing, Booking, Payment
from .serializers import (
    ListingSerializer,
    BookingSerializer,
    UserSerializer,
    UserSignupSerializer,
)
from .tasks import (
    send_payment_confirmation_email,
    send_booking_confirmation_email,
    send_host_notification_email,
    send_signup_confirmation_email,
)
from .utils import run_task   # task runner (Celery or sync fallback)

User = get_user_model()


# ----------------------------
# User Signup
# ----------------------------
class UserSignupView(generics.CreateAPIView):
    """Public endpoint to register a new user."""
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        run_task(send_signup_confirmation_email, user.username, user.email)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # after saving user, redirect to listings endpoint
        return redirect("/api/listings/")

# ----------------------------
# Chapa Payment Helpers
# ----------------------------
def chapa_initiate_payment(booking):
    """Prepare and send payment initiation request to Chapa."""
    url = "https://api.chapa.co/v1/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "amount": str(booking.price),
        "currency": "ETB",
        "email": booking.user.email,
        "first_name": booking.user.first_name,
        "last_name": booking.user.last_name,
        "tx_ref": f"booking-{booking.id}",
        "callback_url": f"{settings.FRONTEND_URL}/payment/callback/",
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json(), response.status_code


def chapa_verify_payment(transaction_id):
    """Verify payment status with Chapa."""
    url = f"https://api.chapa.co/v1/transaction/verify/{transaction_id}"
    headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json(), response.status_code


# ----------------------------
# Payment Views
# ----------------------------
class InitiatePaymentView(APIView):
    """Start a payment flow for a booking."""
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)

        try:
            response_data, status_code = chapa_initiate_payment(booking)

            if status_code == 200 and response_data.get("status") == "success":
                transaction_id = response_data["data"]["id"]

                payment = Payment.objects.create(
                    transaction_id=transaction_id,
                    amount=booking.price,
                    status="PENDING",
                    booking=booking,
                )

                return Response(
                    {
                        "message": "Payment initiated successfully.",
                        "payment_id": payment.id,
                        "payment_link": response_data["data"]["checkout_url"],
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"error": "Failed to initiate payment", "details": response_data},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except requests.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyPaymentView(APIView):
    """Verify the status of a payment transaction with Chapa."""
    def get(self, request, transaction_id):
        payment = get_object_or_404(Payment, transaction_id=transaction_id)

        try:
            data, status_code = chapa_verify_payment(transaction_id)

            if status_code != 200 or data.get("status") != "success":
                return Response({"error": data}, status=status.HTTP_400_BAD_REQUEST)

            status_map = {
                "successful": "COMPLETED",
                "failed": "FAILED",
            }
            payment.status = status_map.get(
                data["data"]["status"].lower(), "PENDING"
            )
            payment.save()

            if payment.status == "COMPLETED":
                run_task(
                    send_payment_confirmation_email,
                    payment.booking.user.email,
                    payment.booking.id,
                )

            return Response(
                {
                    "payment_status": payment.status,
                    "transaction_id": payment.transaction_id,
                },
                status=status.HTTP_200_OK,
            )

        except requests.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ----------------------------
# Booking & Listings
# ----------------------------
class BookingViewSet(viewsets.ModelViewSet):
    """Manage bookings (CRUD)."""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)

        if booking.user and booking.user.email:
            run_task(send_booking_confirmation_email, booking.user.email, booking.id)

        if booking.listing.host and booking.listing.host.email:
            guest_name = booking.user.get_full_name() or booking.user.username
            run_task(
                send_host_notification_email,
                booking.listing.host.email,
                booking.id,
                guest_name,
            )


class ListingViewSet(viewsets.ModelViewSet):
    """Manage listings (CRUD)."""
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ----------------------------
# Users
# ----------------------------
class UserViewSet(viewsets.ModelViewSet):
    """CRUD API endpoint for users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Return the current authenticated user."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
