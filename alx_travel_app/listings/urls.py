from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ListingViewSet,
    BookingViewSet,
    InitiatePaymentView,
    VerifyPaymentView,
    UserViewSet,
    UserSignupView,
)

# DRF Router
router = DefaultRouter()
router.register(r"listings", ListingViewSet, basename="listing")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"users", UserViewSet, basename="user")

# Explicit API endpoints
urlpatterns = [
    path("users/signup/", UserSignupView.as_view(), name="user-signup"),
    path("payments/initiate/<int:booking_id>/", InitiatePaymentView.as_view(), name="initiate-payment"),
    path("payments/verify/<str:transaction_id>/", VerifyPaymentView.as_view(), name="verify-payment"),
]

# Include router URLs (listings, bookings, users CRUD)
urlpatterns += router.urls
