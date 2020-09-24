from django.contrib import admin
from .models import Event, Booking, UserFollowing

admin.site.register(Event)
admin.site.register(Booking)
admin.site.register(UserFollowing)
