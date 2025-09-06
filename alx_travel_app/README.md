# 🧳 ALX Travel App

A production-ready **Django + Django REST Framework (DRF)** backend for managing travel listings, bookings, user authentication (JWT), payments, and notifications.  
Includes **Celery + RabbitMQ** for async email notifications and background tasks.

---

## 🚀 Features

- **User Management**
  - JWT authentication (`djangorestframework-simplejwt`)
  - CRUD operations on users via API
  - Browsable DRF UI with login/logout for testing
- **Listings**
  - Create, view, update, delete travel listings
  - Searchable and filterable API endpoints
- **Bookings**
  - Create bookings tied to listings and users
  - Auto-link user email to booking
  - Booking status management
- **Payments**
  - Initiate and verify payments for bookings
  - Mock integration (can extend with Stripe/PayPal/Chapa)
- **Notifications**
  - **Celery + RabbitMQ** for async background tasks
  - Email notifications:
    - Booking confirmations
    - Host notifications
    - Payment receipts
- **API Documentation**
  - **Swagger UI** (`/swagger/`)
  - **Redoc UI** (`/redoc/`)
  - **JSON schema** (`/swagger.json`)
- **Production Ready**
  - MySQL database (SQLite fallback in dev)
  - Gunicorn + Whitenoise for deployment
  - CORS enabled for frontend integration

---

## 📂 Project Structure

```
alx_travel_app/
│── alx_travel_app/                
│   ├── __init__.py
│   ├── settings.py                # Configurations (JWT, Celery, DRF, DB, Email, etc.)
│   ├── urls.py                    # Root URL configuration
│   ├── wsgi.py
│   ├── asgi.py
│   ├── celery.py                  # Celery setup
│
│── listings/                      # Core app
│   ├── models.py                  # User, Listing, Booking, Payment models
│   ├── views.py                   # ViewSets + API Views
│   ├── serializers.py             # Serializers for API endpoints
│   ├── urls.py                    # App URL routes
│   ├── tasks.py                   # Celery tasks (email notifications)
│   ├── management/
│   │   └── commands/
│   │       └── seed_users.py      # Seed DB with dummy users
│   ├── migrations/                
│
│── requirements.txt               # Dependencies
│── README.md                      # Project documentation
│── manage.py                      # Django CLI entry point
│── .env                           # Environment variables
│── db.sqlite3                     # SQLite fallback (dev only)
```

---

## 🔑 Authentication

- **Session Auth (for testing)**  
  `/api-auth/login/` and `/api-auth/logout/`  
- **JWT Authentication**  
  - `POST /api/token/` → Get access + refresh tokens  
  - `POST /api/token/refresh/` → Refresh access token  

---

## 📡 API Endpoints

### 👤 Users

| Endpoint           | Method | Description      |
|--------------------|--------|------------------|
| `/api/users/`      | GET    | List all users   |
| `/api/users/{id}/` | GET    | Retrieve a user  |
| `/api/users/`      | POST   | Create a user    |
| `/api/users/{id}/` | PUT    | Update a user    |
| `/api/users/{id}/` | DELETE | Delete a user    |

### 🏝️ Listings

| Endpoint              | Method | Description         |
|-----------------------|--------|---------------------|
| `/api/listings/`      | GET    | List all listings   |
| `/api/listings/{id}/` | GET    | Retrieve a listing  |
| `/api/listings/`      | POST   | Create a listing    |
| `/api/listings/{id}/` | PUT    | Update a listing    |
| `/api/listings/{id}/` | DELETE | Delete a listing    |

### 📑 Bookings

| Endpoint              | Method | Description         |
|-----------------------|--------|---------------------|
| `/api/bookings/`      | GET    | List all bookings   |
| `/api/bookings/{id}/` | GET    | Retrieve a booking  |
| `/api/bookings/`      | POST   | Create a booking    |
| `/api/bookings/{id}/` | PUT    | Update a booking    |
| `/api/bookings/{id}/` | DELETE | Cancel a booking    |

### 💳 Payments

| Endpoint                                   | Method | Description             |
|--------------------------------------------|--------|-------------------------|
| `/api/payments/initiate/{booking_id}/`     | POST   | Initiate a payment      |
| `/api/payments/verify/{transaction_id}/`   | GET    | Verify payment status   |

---

## 📧 Email Notifications (Celery + RabbitMQ)

- **Setup**
  1. Install and run RabbitMQ:
     ```bash
     rabbitmq-server
     ```
  2. Start Celery worker:
     ```bash
     celery -A alx_travel_app worker -l info
     ```
  3. (Optional) Run Celery beat for scheduled tasks:
     ```bash
     celery -A alx_travel_app beat -l info
     ```

- **Tasks implemented:**
  - Send booking confirmation email to user  
  - Send booking notification email to host  
  - Send payment confirmation email  

📌 Example from `listings/tasks.py`:

```python
@shared_task
def send_user_booking_email(user_email, booking_id):
    send_mail(
        "Booking Confirmation",
        f"Your booking #{booking_id} has been confirmed.",
        "noreply@alxtravel.com",
        [user_email],
    )
```

---

## 🌱 Seeding the Database

To create dummy users for testing:

```bash
python manage.py seed_users
python manage.py seed 
```

---

## ⚙️ Setup & Installation

1️⃣ Clone repo & install dependencies:

```bash
git clone <your-repo-url>
cd alx_travel_app
pip install -r requirements.txt
```

2️⃣ Configure `.env` (example):

```ini
DEBUG=True
SECRET_KEY=django-insecure-sample-key
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=alx_travel
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=127.0.0.1
DB_PORT=3306

CELERY_BROKER_URL=amqp://guest:guest@localhost//

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=yourpassword

CHAPA_SECRET_KEY=your_chapa_key
```

3️⃣ Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

4️⃣ Start Celery worker (Windows dev use `-P solo`):

```bash
celery -A alx_travel_app worker -l info -P solo
```

5️⃣ Start Django server:

```bash
python manage.py runserver
```

---

## 📖 API Documentation

- Swagger UI: <http://127.0.0.1:8000/swagger/>  
- Redoc: <http://127.0.0.1:8000/redoc/>  
- JSON: <http://127.0.0.1:8000/swagger.json>  

---

## 🛠️ Tech Stack

- Django 5.2.3  
- Django REST Framework  
- SimpleJWT  
- Celery 5.5.3  
- RabbitMQ  
- MySQL / SQLite  
- Swagger (drf-yasg)  
- Whitenoise  
- Gunicorn  

---


## 🌍 Endpoints

### 👤 User Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | `POST` | Signup (default homepage) |
| `/api/users/signup/` | `POST` | Signup new user (API) |
| `/api/users/` | `GET, POST` | List all users / create user |
| `/api/users/{id}/` | `GET, PUT, PATCH, DELETE` | Retrieve/update/delete a user |
| `/api/users/me/` | `GET` | Get current authenticated user |

#### Signup Request Example
```json
POST /api/users/signup/
{
  "username": "coded123",
  "email": "coded@example.com",
  "password": "securePassword!"
}
```
✅ Triggers a **signup confirmation email**.

---

### 🏡 Listings Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/listings/` | `GET, POST` | List or create listings |
| `/api/listings/{id}/` | `GET, PUT, PATCH, DELETE` | Retrieve/update/delete a listing |

---

### 📅 Booking Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/bookings/` | `GET, POST` | List or create bookings |
| `/api/bookings/{id}/` | `GET, PUT, PATCH, DELETE` | Retrieve/update/delete a booking |

✅ When a booking is created:
- User receives booking confirmation email
- Host receives new booking notification email

---

### 💳 Payment Endpoints (Chapa Integration)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/payments/initiate/{booking_id}/` | `POST` | Initiate payment for a booking |
| `/api/payments/verify/{transaction_id}/` | `GET` | Verify payment status |

✅ On successful payment:
- Payment status is updated in DB
- User receives a payment confirmation email

---

### 📖 API Documentation
- Swagger UI → `/swagger/`
- Redoc → `/redoc/`
- JSON Schema → `/swagger.json`

---

## 📧 Email Notifications
The following notifications are supported:
1. **Signup Confirmation** → Sent when a user signs up
2. **Booking Confirmation** → Sent to user after booking
3. **Host Notification** → Sent to host when new booking is created
4. **Payment Confirmation** → Sent to user on successful payment

---

## 🏗️ Roadmap

- [ ] Add Stripe/PayPal integration  
- [ ] Extend search & filter on listings  
- [ ] Add push notifications (WebSockets + Django Channels)  
- [ ] Dockerize with Celery + RabbitMQ + PostgreSQL  

---

## 📜 License

This project is maintained by **CODED**.
