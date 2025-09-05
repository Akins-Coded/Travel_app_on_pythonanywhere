# ALX Travel App

**ALX Travel App** is a robust Django-based travel booking platform that enables users to explore listings—including hotels, tours, rentals, and activities—make bookings, and process payments securely via the **Chapa** payment gateway. The system also supports **payment verification**, **asynchronous email notifications**, and background task handling using **Celery** with **RabbitMQ**.

---

## Features

### Listings

* Browse available Hotels, Tours, Rentals, and Activities.
* Perform CRUD operations on listings through API endpoints.

### Bookings

* Create bookings with check-in and check-out dates.
* Track booking status: Pending, Confirmed, Cancelled, Completed.

### Payments

* Initiate payments via the Chapa API.
* Verify payment status with Chapa.
* Automatically update payment status in the database: Pending, Completed, Failed, Refunded.
* Send booking confirmation emails asynchronously via Celery.

### Reviews

* Submit ratings for listings (1–5 stars).
* Restrict users to one review per listing.

### Background Tasks

* Celery integration with RabbitMQ for background task management.
* Asynchronous execution of email notifications on booking creation.
* Configurable SMTP backend for email delivery.

---

## Tech Stack

* **Backend:** Django 5.x, Django REST Framework
* **Database:** MySQL
* **Task Queue:** Celery with RabbitMQ
* **Payment Gateway:** Chapa
* **Environment Management:** django-environ
* **API Documentation:** drf-yasg (Swagger)

---

## API Endpoints

| Endpoint                             | Method             | Description                                    |
| ------------------------------------ | ------------------ | ---------------------------------------------- |
| `/listings/`                         | GET / POST         | List all listings or create a new listing      |
| `/listings/<id>/`                    | GET / PUT / DELETE | Retrieve, update, or delete a specific listing |
| `/bookings/`                         | GET / POST         | List all bookings or create a new booking      |
| `/bookings/<id>/`                    | GET / PUT / DELETE | Retrieve, update, or delete a specific booking |
| `/payments/initiate/<booking_id>/`   | POST               | Initiate a Chapa payment for a booking         |
| `/payments/verify/<transaction_id>/` | GET / POST         | Verify the status of a payment transaction     |
