from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from events.models import Event, Booking, UserFollowing
from .serializers import RegisterSerializer, CreateUpdateEventSerializer, EventSerializer, BookingSerializer, \
    UserFollowingSerializer, EventBookersSerializer, BookEventSerializer, FollowUserSerializer
from .permissions import IsEventOrganizer


class Register(CreateAPIView):
    serializer_class = RegisterSerializer


class CreateEvent(CreateAPIView):
    serializer_class = CreateUpdateEventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user, available_seats=self.request.data["seats"])


class EventsList(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', "description"]
    permission_classes = [IsAuthenticated]


class UsersEventsList(ListAPIView):
    lookup_field = "id"
    lookup_url_kwarg = "user_id"
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        organizer = User.objects.get(id=self.kwargs.get("user_id"))
        return Event.objects.filter(organizer=organizer)


class MyBookings(ListAPIView):
    lookup_field = "id"
    lookup_url_kwarg = "user_id"
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(booker=self.request.user)


class MyFollowings(ListAPIView):
    lookup_field = "id"
    lookup_url_kwarg = "user_id"
    serializer_class = UserFollowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserFollowing.objects.filter(user=self.request.user)


class EventBookers(ListAPIView):
    lookup_field = "id"
    lookup_url_kwarg = "event_id"
    serializer_class = EventBookersSerializer
    permission_classes = [IsAuthenticated, IsEventOrganizer]

    def get_queryset(self):
        event = Event.objects.get(id=self.kwargs.get("event_id"))
        return Booking.objects.filter(event=event)


class BookEvent(CreateAPIView):
    lookup_url_kwarg = "event_id"
    serializer_class = BookEventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        event = Event.objects.get(id=self.kwargs.get("event_id"))
        if event.available_seats >= int(self.request.data["number_of_tickets"]):
            event.available_seats -= int(self.request.data["number_of_tickets"])
            event.save()
            serializer.save(booker=self.request.user, event=event)


class FollowUser(CreateAPIView):
    lookup_url_kwarg = "user_id"
    permission_classes = [IsAuthenticated]
    serializer_class = FollowUserSerializer

    def perform_create(self, serializer):
        user = User.objects.get(id=self.kwargs.get("user_id"))
        serializer.save(user=self.request.user, following_user=user)
