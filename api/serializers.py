from rest_framework import serializers
from django.contrib.auth.models import User
from events.models import Event, Booking, UserFollowing


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        return validated_data


class CreateUpdateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', "location", "datetime", "seats"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', "datetime", "available_seats"]


class BookingSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = Booking
        fields = ['event', "number_of_tickets", ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', "first_name", "last_name"]


class UserFollowingSerializer(serializers.ModelSerializer):
    following_user = UserSerializer()

    class Meta:
        model = UserFollowing
        fields = ['following_user']


class EventBookersSerializer(serializers.ModelSerializer):
    booker = UserSerializer()

    class Meta:
        model = Booking
        fields = ['booker', "number_of_tickets", ]


class BookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['number_of_tickets']


class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = []
