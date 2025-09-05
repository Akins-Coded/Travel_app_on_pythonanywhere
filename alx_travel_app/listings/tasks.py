from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_payment_confirmation_email(user_email, booking_id):
    subject = "Payment Successful"
    message = f"Your payment for booking {booking_id} was successful."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])



@shared_task
def send_booking_confirmation_email(to_email, booking_id):
    subject = "Booking Confirmation"
    message = f"Your booking with ID {booking_id} has been created successfully!"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])



@shared_task
def send_host_notification_email(host_email, booking_id, guest_name):
    """Notify host when a new booking is created"""
    subject = "New Booking on Your Listing"
    message = f"You have a new booking (ID {booking_id}) from {guest_name}."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [host_email])