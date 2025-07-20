# listings/serializers.py
from rest_framework import serializers
from .models import Property, Booking
from django.contrib.auth import get_user_model

User = get_user_model()

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class PropertySerializer(serializers.ModelSerializer):
    host = HostSerializer(read_only=True)
    
    class Meta:
        model = Property
        fields = [
            'id',
            'host',
            'title',
            'location',
            'price_per_night',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'host', 'created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    guest = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    property = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all()
    )
    property_details = PropertySerializer(
        source='property',
        read_only=True
    )
    
    class Meta:
        model = Booking
        fields = [
            'id',
            'guest',
            'property',
            'property_details',
            'check_in',
            'check_out',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """
        Validate booking dates:
        - Check-out must be after check-in
        - No overlapping bookings for the same property
        """
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date"
            )
        
        overlapping_bookings = Booking.objects.filter(
            property=data['property'],
            check_in__lt=data['check_out'],
            check_out__gt=data['check_in']
        ).exists()
        
        if overlapping_bookings:
            raise serializers.ValidationError(
                "This property is already booked for the selected dates"
            )
        
        return data

class PropertyDetailSerializer(PropertySerializer):
    bookings = BookingSerializer(many=True, read_only=True)
    
    class Meta(PropertySerializer.Meta):
        fields = PropertySerializer.Meta.fields + ['bookings']
