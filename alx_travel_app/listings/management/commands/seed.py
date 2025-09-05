# listings/management/commands/seed.py

from django.core.management.base import BaseCommand
from listings.models import Listing, Booking, Review, Payment
from django.contrib.auth import get_user_model
from faker import Faker
from django.utils.text import slugify
from datetime import timedelta, date
from decimal import Decimal
import random
import uuid

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with sample data (Listings, Bookings, Reviews, Payments)"

    def handle(self, *args, **kwargs):
        if not User.objects.exists():
            self.stdout.write(self.style.ERROR(
                "❌ No users found. Create a user first to act as host and customer."
            ))
            return

        host = User.objects.first()
        users = list(User.objects.all())

        listing_types = ["hotel", "tour", "rental", "activity"]
        listings = []

        # --- Seed Listings ---
        for _ in range(10):  # create 10 sample listings
            title = fake.sentence(nb_words=4)
            slug = slugify(title)

            # Ensure slug uniqueness
            original_slug = slug
            counter = 1
            while Listing.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            listing = Listing.objects.create(
                title=title,
                slug=slug,
                description=fake.paragraph(nb_sentences=5),
                host=host,
                location=fake.city(),
                listing_type=random.choice(listing_types),
                price=Decimal(random.randint(50, 500)),
                capacity=random.randint(1, 10),
                available_from=date.today(),
                available_to=date.today() + timedelta(days=random.randint(30, 90)),
            )
            listings.append(listing)

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded 10 listings."))

        # --- Seed Bookings ---
        for listing in listings:
            customer = random.choice(users)
            check_in = date.today() + timedelta(days=random.randint(1, 20))
            check_out = check_in + timedelta(days=random.randint(1, 7))

            booking = Booking.objects.create(
                listing=listing,
                user=customer,
                user_email=customer.email or fake.email(),
                check_in=check_in,
                check_out=check_out,
                guests=random.randint(1, listing.capacity),
                price=listing.price * Decimal(random.randint(1, 3)),  # total price
                status=random.choice([c[0] for c in Booking.STATUS_CHOICES]),
            )

            # --- Seed Payment ---
            Payment.objects.create(
                booking=booking,
                status=random.choice([c[0] for c in Payment.PAYMENT_STATUS_CHOICES]),
                amount=booking.price,
                transaction_id=str(uuid.uuid4()),
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded Bookings and Payments."))

        # --- Seed Reviews ---
        for listing in listings:
            reviewer = random.choice(users)
            if not Review.objects.filter(listing=listing, user=reviewer).exists():
                Review.objects.create(
                    listing=listing,
                    user=reviewer,
                    rating=random.randint(1, 5),
                    comment=fake.paragraph(nb_sentences=3),
                )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded Reviews."))
        self.stdout.write(self.style.SUCCESS("🎉 Database seeding complete!"))
