from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    location = models.CharField(max_length=300)
    datetime = models.DateTimeField()
    seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    img = models.ImageField(null=True, blank=True, default="01.jpg")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'event_id': self.id})


class Booking(models.Model):
    booker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookers")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings")
    number_of_tickets = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.booker.username} booked tickets for {self.event.title}"


class UserFollowing(models.Model):
    user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "following_user"]

    def __str__(self):
        return f"{self.user} follows {self.following_user}"
