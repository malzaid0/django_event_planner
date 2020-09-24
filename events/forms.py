from django import forms
from django.contrib.auth.models import User
from .models import Event, Booking


class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

        widgets = {
            'password': forms.PasswordInput(),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['organizer', "available_seats", ]

        widgets = {
            'datetime': forms.DateTimeInput(),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["number_of_tickets"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
