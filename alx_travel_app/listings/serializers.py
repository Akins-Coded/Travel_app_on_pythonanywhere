from rest_framework import serializers
from .models import Listing, Booking, Review
from django.contrib.auth import get_user_model

User = get_user_model()


class ListingSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField(read_only=True)
    reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'slug', 'description', 'host',
            'location', 'listing_type', 'price_per_night',
            'capacity', 'available_from', 'available_to',
            'created_at', 'reviews_count', 'average_rating'
        ]


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    listing = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'listing', 'check_in', 'check_out',
            'guests', 'total_price', 'status', 'created_at'
        ]

