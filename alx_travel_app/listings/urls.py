from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, InitiatePaymentView, VerifyPaymentView

# Initialize DRF router
router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)

# Standard URL patterns
urlpatterns = [
    path('payments/initiate/<int:booking_id>/', InitiatePaymentView.as_view(), name='initiate-payment'),
     path('payments/verify/<str:transaction_id>/', VerifyPaymentView.as_view(), name='verify-payment'),
]

# Include router URLs
urlpatterns += router.urls

