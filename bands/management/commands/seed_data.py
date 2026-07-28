import random
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from faker import Faker

from bands.models import Musician, Band, Venue, Room

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with fake Musicians, Bands, Venues, and Rooms"

    def add_arguments(self, parser):
        parser.add_argument("--musicians", type=int, default=30)
        parser.add_argument("--bands", type=int, default=8)
        parser.add_argument("--venues", type=int, default=5)
        parser.add_argument("--rooms-per-venue", type=int, default=3)
        parser.add_argument(
            "--flush", action="store_true", help="Delete existing data first"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(
                self.style.ERROR("Refusing to seed data outside DEBUG mode")
            )
            return

        if options["flush"]:
            Room.objects.all().delete()
            Venue.objects.all().delete()
            Band.objects.all().delete()
            Musician.objects.all().delete()
            self.stdout.write("Cleared existing data.")

        # --- Musicians ---
        musicians = [
            Musician(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                birth=fake.date_of_birth(minimum_age=18, maximum_age=75),
            )
            for _ in range(options["musicians"])
        ]
        Musician.objects.bulk_create(musicians)
        musicians = list(Musician.objects.all())  # reload with PKs

        # --- Bands (M2M needs objects saved first) ---
        bands = []
        for _ in range(options["bands"]):
            band = Band.objects.create(
                name=fake.word().capitalize() + " " + fake.word().capitalize()
            )
            band_members = random.sample(musicians, k=random.randint(2, 5))
            band.musicians.set(band_members)
            bands.append(band)

        # --- Venues ---
        venues = [
            Venue(
                name=fake.city()
                + " "
                + random.choice(["Arena", "Hall", "Theatre", "Club"])
            )
            for _ in range(options["venues"])
        ]
        Venue.objects.bulk_create(venues)
        venues = list(Venue.objects.all())

        # --- Rooms ---
        rooms = []
        for venue in venues:
            for _ in range(options["rooms_per_venue"]):
                rooms.append(
                    Room(
                        name=random.choice(
                            [
                                "Main Stage",
                                "Side Room",
                                "Balcony",
                                "Lounge",
                                "Green Room",
                            ]
                        ),
                        venue=venue,
                    )
                )
        Room.objects.bulk_create(rooms)

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(musicians)} musicians, {len(bands)} bands, "
                f"{len(venues)} venues, {len(rooms)} rooms."
            )
        )
