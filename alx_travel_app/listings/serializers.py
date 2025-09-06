from rest_framework import serializers
from .models import Listing, Booking
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user
    
class ListingSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField(read_only=True)
    reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'slug', 'description', 'host',
            'location', 'listing_type', 'price',
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
            'guests', 'price', 'status', 'created_at'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_staff"]
        read_only_fields = ["id", "is_staff"]