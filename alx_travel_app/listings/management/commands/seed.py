# listings/management/commands/seed.py

from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth import get_user_model
from faker import Faker
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        if not User.objects.exists():
            self.stdout.write(self.style.ERROR('No users found. Create a user first to act as host.'))
            return

        host = User.objects.first()
        listing_types = ['hotel', 'tour', 'rental', 'activity']

        for _ in range(10):  # create 10 sample listings
            title = fake.sentence(nb_words=4)
            Listing.objects.create(
                title=title,
                slug=fake.slug(title),
                description=fake.paragraph(nb_sentences=5),
                host=host,
                location=fake.city(),
                listing_type=random.choice(listing_types),
                price=random.randint(50, 500),
                capacity=random.randint(1, 10),
                available_from=fake.date_this_year(),
                available_to=fake.date_between(start_date='+30d', end_date='+90d'),
            )

        self.stdout.write(self.style.SUCCESS('✅ Successfully seeded 10 listings.'))
