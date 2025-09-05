
# 📄 `seed.py` – Seeder Command for Listings App

This document explains how to use the custom Django management command `seed.py` to populate your database with **sample `Listing` data** using Faker.

---

## 🧰 Command Location

> 📁 `listings/management/commands/seed.py`

This script seeds your database with random listings for testing or development purposes.

---

## 🚀 Features

- Auto-generates **10 random listings**
- Uses the `Faker` library to simulate realistic data
- Assigns the first user in the database as the **host**
- Covers:
  - Title, slug, description
  - Host (FK)
  - Location
  - Listing type (`hotel`, `tour`, `rental`, `activity`)
  - Price per night
  - Capacity
  - Available date range

---

## 📦 Prerequisites

Before running the command, ensure:

1. The database is migrated:
   ```bash
   python manage.py migrate
   ```

2. At least one user exists:
   ```bash
   python manage.py createsuperuser
   ```

3. `Faker` is installed:
   ```bash
   pip install Faker
   ```

---

## ⚙️ How to Run

```bash
python manage.py seed
```

> 💡 This will insert **10 new `Listing` records** using randomly generated data.

---

## 🖥️ Sample Output

```bash
✅ Successfully seeded 10 listings.
```

If no users are found:

```bash
No users found. Create a user first to act as host.
```

---

## 🧠 How It Works (Under the Hood)

- Uses Django's `BaseCommand` to define a custom management task
- Calls `Faker` to generate:
  - Sentence for the title
  - Paragraph for the description
  - Random city as location
  - Random dates, price, capacity
- `slug` is derived from the title using `Faker.slug(title)`
- Each listing is saved with `host = User.objects.first()`

---

## 📁 File Structure

```
listings/
├── management/
│   └── commands/
│       └── seed.py       # <-- The seeder command
├── models.py             # Listing, Booking, Review models
├── serializers.py
└── ...
```

---

## ✅ Output Example (In Django Admin)

Each listing created will show up in your admin panel under **Listings**, ready to test views, filters, or APIs.

---
