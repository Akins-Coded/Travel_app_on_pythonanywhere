# listings/management/commands/seed_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with sample users (hosts and customers)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=5,
            help="Number of users to create (default: 5)",
        )

    def handle(self, *args, **options):
        count = options["count"]
        created_users = []

        for _ in range(count):
            username = fake.user_name()
            email = fake.email()
            password = "password123"  # simple default password

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
                created_users.append(user)

        if created_users:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Created {len(created_users)} fake users.")
            )
            self.stdout.write(
                self.style.WARNING("ℹ️ All users have default password: password123")
            )
        else:
            self.stdout.write(self.style.WARNING("⚠️ No new users were created."))
