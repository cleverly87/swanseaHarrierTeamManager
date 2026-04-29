"""
Load Swansea Harriers athletes into the database.
Run with: python manage.py load_athletes
"""
from django.core.management.base import BaseCommand
from relay.models import Athlete


ATHLETES = [
    ("Brychan", "Price-Davies"),
    ("Chris", "Lovatt"),
    ("Connor", "Rogers"),
    ("Daf", "Jones"),
    ("Dan", "Gurmin"),
    ("Dom", "Smith"),
    ("Elliot", "Lawrence"),
    ("Finley", "Hines"),
    ("Geraint", "Williams"),
    ("Jamie", "Taylor-Caldwell"),
    ("Morgan", "James"),
    ("Craig", "Jones"),
    ("Dan", "Rothwell"),
    ("Jon", "Butler"),
    ("Josh", "Morgan"),
    ("Kris", "Jones"),
    ("Marc", "Hobbs"),
    ("Matt", "Harvey"),
    ("Matt", "Rees"),
    ("Matt", "Verran"),
    ("Sam", "Joseph"),
    ("Steve", "Taylor"),
    ("Will", "Munday"),
    ("Alfie", "Robinson"),
    ("Afan", "Humphries"),
    ("Dewi", "Griffiths"),
    ("Will", "Ralston"),
    ("Chris", "Booth"),
    ("Ed", "Davies"),
    ("Jack", "Hurley"),
    ("Jacob", "Parry"),
    ("Chris", "Thomson"),
    ("Ben", "Mitchell"),
]


class Command(BaseCommand):
    help = 'Load Swansea Harriers athletes into the database'

    def handle(self, *args, **options):
        self.stdout.write("Loading Swansea Harriers athletes...")

        # Clear existing athletes (optional - comment out if you want to keep existing ones)
        Athlete.objects.all().delete()
        self.stdout.write("Cleared existing athletes.")

        # Create athletes
        for first_name, last_name in ATHLETES:
            athlete = Athlete.objects.create(
                first_name=first_name,
                last_name=last_name,
            )
            self.stdout.write(f"  ✓ Added: {athlete.full_name}")

        self.stdout.write(self.style.SUCCESS(f"\n✓ Successfully loaded {len(ATHLETES)} athletes!"))
        self.stdout.write(self.style.SUCCESS("  You can now add emails and URN numbers via the admin."))
