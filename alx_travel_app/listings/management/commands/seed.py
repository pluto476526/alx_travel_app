from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Property, Booking, Review
import random
from datetime import datetime, timedelta
import uuid

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with sample listings, bookings, and reviews'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        self.run_seed()
        self.stdout.write('Done!')

    def run_seed(self):
        self.clear_data()
        self.create_users()
        self.create_properties()
        self.create_bookings()
        self.create_reviews()

    def clear_data(self):
        self.stdout.write("Deleting old data...")
        models = [Property, Booking, Review]
        for model in models:
            model.objects.all().delete()

    def create_users(self):
        self.stdout.write("Creating users...")
        users = [
            {'email': 'host1@example.com', 'first_name': 'John', 'last_name': 'Smith', 'role': 'host'},
            {'email': 'host2@example.com', 'first_name': 'Sarah', 'last_name': 'Johnson', 'role': 'host'},
            {'email': 'guest1@example.com', 'first_name': 'Michael', 'last_name': 'Brown', 'role': 'guest'},
            {'email': 'guest2@example.com', 'first_name': 'Emily', 'last_name': 'Davis', 'role': 'guest'},
        ]

        for user_data in users:
            user = User.objects.create_user(
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                password='password123',
                role=user_data['role']
            )
            self.stdout.write(f"Created user: {user.email}")

        self.hosts = User.objects.filter(role='host')
        self.guests = User.objects.filter(role='guest')

    def create_properties(self):
        self.stdout.write("Creating properties...")
        properties = [
            {
                'host': self.hosts[0],
                'title': 'Cozy Mountain Cabin',
                'location': 'Aspen, Colorado',
                'price_per_night': 175.00
            },
            {
                'host': self.hosts[0],
                'title': 'Beachfront Villa',
                'location': 'Miami, Florida',
                'price_per_night': 300.00
            },
            {
                'host': self.hosts[1],
                'title': 'Downtown Loft',
                'location': 'New York, NY',
                'price_per_night': 225.00
            },
            {
                'host': self.hosts[1],
                'title': 'Desert Oasis',
                'location': 'Palm Springs, California',
                'price_per_night': 195.00
            },
        ]

        for prop_data in properties:
            property = Property.objects.create(**prop_data)
            self.stdout.write(f"Created property: {property.title}")

        self.properties = Property.objects.all()

    def create_bookings(self):
        self.stdout.write("Creating bookings...")
        today = datetime.now().date()
        
        for i, prop in enumerate(self.properties):
            for j, guest in enumerate(self.guests):
                check_in = today + timedelta(days=(i+j)*30)
                check_out = check_in + timedelta(days=random.randint(2, 7))
                
                Booking.objects.create(
                    property=prop,
                    guest=guest,
                    check_in=check_in,
                    check_out=check_out
                )
                self.stdout.write(f"Created booking for {prop.title} by {guest.email}")

    def create_reviews(self):
        self.stdout.write("Creating reviews...")
        
        for booking in Booking.objects.all():
            Review.objects.create(
                guest=booking.guest,
                property=booking.property,
                booking=booking,
                rating=random.randint(3, 5),
                comment=self.get_random_comment(booking.property.title)
            )
            self.stdout.write(f"Created review for {booking.property.title}")

    def get_random_comment(self, property_title):
        comments = [
            f"Great stay at {property_title}! Would definitely recommend.",
            f"{property_title} was wonderful. Perfect for our vacation.",
            f"Nice place but could use some improvements.",
            f"Absolutely loved our time at {property_title}!",
            f"Good value for the price. Enjoyed our stay at {property_title}."
        ]
        return random.choice(comments)
