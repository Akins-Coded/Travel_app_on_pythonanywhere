from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from django.conf import settings
import requests

from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_payment_confirmation_email, send_booking_confirmation_email


# ----------------------------
# Helper function for Chapa
# ----------------------------
def chapa_initiate_payment(booking):
    """Prepare and send payment initiation request to Chapa"""
    url = "https://api.chapa.co/v1/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "amount": str(booking.price),
        "currency": "ETB",
        "email": booking.user.email,
        "first_name": booking.user.first_name,
        "last_name": booking.user.last_name,
        "tx_ref": f"booking-{booking.id}",
        "callback_url": f"{settings.FRONTEND_URL}/payment/callback/"
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json(), response.status_code


def chapa_verify_payment(transaction_id):
    """Verify payment status with Chapa"""
    url = f"https://api.chapa.co/v1/transaction/verify/{transaction_id}"
    headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json(), response.status_code


# ----------------------------
# Payment Views
# ----------------------------
class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)

        try:
            response_data, status_code = chapa_initiate_payment(booking)

            if status_code == 200 and response_data.get("status") == "success":
                transaction_id = response_data["data"]["id"]

                # Save payment
                payment = Payment.objects.create(
                    booking_reference=f"booking-{booking.id}",
                    transaction_id=transaction_id,
                    amount=booking.price,
                    status="PENDING",
                    booking=booking
                )

                return Response({
                    "message": "Payment initiated successfully.",
                    "payment_id": payment.id,
                    "payment_link": response_data["data"]["checkout_url"]
                }, status=status.HTTP_200_OK)

            return Response({"error": "Failed to initiate payment", "details": response_data},
                            status=status.HTTP_400_BAD_REQUEST)

        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyPaymentView(APIView):
    def get(self, request, transaction_id):
        payment = get_object_or_404(Payment, transaction_id=transaction_id)

        try:
            data, status_code = chapa_verify_payment(transaction_id)

            if status_code != 200 or data.get("status") != "success":
                return Response({"error": data}, status=status.HTTP_400_BAD_REQUEST)

            # Map Chapa status to Payment status
            status_map = {
                "successful": "COMPLETED",
                "failed": "FAILED"
            }
            payment.status = status_map.get(data["data"]["status"].lower(), "PENDING")
            payment.save()

            # Send confirmation email asynchronously
            if payment.status == "COMPLETED":
                send_payment_confirmation_email.delay(
                    payment.booking.user.email,
                    payment.booking_reference
                )

            return Response({
                "payment_status": payment.status,
                "transaction_id": payment.transaction_id
            }, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ----------------------------
# Listing & Booking ViewSets
# ----------------------------
class ListingViewSet(ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        # Trigger async email
        send_booking_confirmation_email.delay(booking.user.email, booking.id)