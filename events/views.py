from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import UserSignup, UserLogin, EventForm, BookingForm, ProfileForm
from .models import Event, Booking, UserFollowing
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
import random


def home(request):
    if request.user.is_authenticated:
        events = Event.objects.filter(datetime__gte=timezone.now())
        if len(events) >= 3:
            rand = random.sample(range(0, len(events) - 1), 3)
            context = {
                "sample_event1": events[rand[0]],
                "sample_event2": events[rand[1]],
                "sample_event3": events[rand[2]],
            }
        else:
            context = {
                "sample_event1": None,
            }
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("no-access")

    events = Event.objects.filter(organizer=request.user).order_by("datetime")
    previous_bookings = Booking.objects.filter(booker=request.user, event__datetime__lt=timezone.now()).order_by("event__datetime")
    upcoming_bookings = Booking.objects.filter(booker=request.user, event__datetime__gt=timezone.now()).order_by("event__datetime")
    context = {
        "events": events,
        "previous_bookings": previous_bookings,
        "upcoming_bookings": upcoming_bookings,
    }
    return render(request, "dashboard.html", context)


def event_list(request):
    if not request.user.is_authenticated:
        return redirect("no-access")

    events = Event.objects.filter(datetime__gte=timezone.now()).order_by("datetime")
    query = request.GET.get('search_term')
    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(organizer__username__icontains=query) |
            Q(organizer__first_name__icontains=query) |
            Q(organizer__last_name__icontains=query)
        ).distinct().order_by("datetime")
    context = {
        "events": events
    }
    return render(request, 'event_list.html', context)


def event_detail(request, event_id):
    if not request.user.is_authenticated:
        return redirect("no-access")
    event = Event.objects.get(id=event_id)
    bookings = Booking.objects.filter(event=event)
    context = {
        "event": event,
        "bookings": bookings
    }
    return render(request, 'event_detail.html', context)


def event_create(request):
    if not request.user.is_authenticated:
        return redirect("no-access")
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.available_seats = event.seats
            event.save()
            followers = request.user.followers.all()
            if followers:
                send_mail(
                    'Welcome to the club!',
                    f'Hey,\nI just created a new event!!\nplease check it out\n\n'
                    f'event: {event.title}\ntime: {event.datetime}\nlink: http://127.0.0.1:8000{event.get_absolute_url()}',
                    '3a1a3f93e1-d2fae3@inbox.mailtrap.io',
                    [follower.user.email for follower in followers],
                    fail_silently=False,
                )
            return redirect('event-list')
    context = {
        "form": form,
    }
    return render(request, 'event-create.html', context)


def event_update(request, event_id):
    event = Event.objects.get(id=event_id)
    num_of_seats = event.seats
    if not request.user == event.organizer:
        return redirect("no-access")
    if event.datetime < timezone.now():
        messages.warning(request, "You cannot edit old events")
        return redirect(event)
    form = EventForm(instance=event)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event_obj = form.save(commit=False)
            if num_of_seats != event_obj.seats:
                event_obj.available_seats -= (num_of_seats - event_obj.seats)
                if event.available_seats < 0:
                    messages.warning(request, "Number of tickets exceeds th number of available seats")
                    return redirect(event)
            event_obj.save()
            messages.success(request, "You have edited the event.")
            return redirect(event)
    context = {
        "event": event,
        "form": form,
    }
    return render(request, 'event-update.html', context)


def book_event(request, event_id):
    if not request.user.is_authenticated:
        return redirect("no-access")
    event = Event.objects.get(id=event_id)
    if event.datetime < timezone.now():
        messages.warning(request, "Are you trying to be smart here!? This's an old event!")
        return redirect(event)
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if booking.number_of_tickets <= event.available_seats:
                event.available_seats -= booking.number_of_tickets
                event.save()
                booking.booker = request.user
                booking.event = event
                booking.save()
                messages.success(request, "You have successfully booked.")
                send_mail(
                    'Welcome to the club!',
                    f'event: {event.title}\n'
                    f'time: {event.datetime}\nSeats: {booking.number_of_tickets}',
                    '3a1a3f93e1-d2fae3@inbox.mailtrap.io',
                    [request.user.email],
                    fail_silently=False,
                )
            else:
                messages.warning(request, "Number of tickets exceeds th number of available seats")
        return redirect(event)
    context = {
        "form": form,
        "event": event,
    }
    return render(request, "booking.html", context)


def cancel_booking(request, booking_id):
    if not request.user.is_authenticated:
        return redirect("no-access")
    booking = Booking.objects.get(id=booking_id)
    event = booking.event
    if not request.user == booking.booker:
        return redirect("no-access")

    if event.datetime > timezone.now():
        if (timezone.now() + timezone.timedelta(hours=3)) < event.datetime:
            booking.delete()
            messages.success(request, "You have successfully deleted your booking.")
            return redirect(event)
        messages.warning(request, "Too late")
        return redirect(event)


def profile_detail(request):
    if not request.user.is_authenticated:
        return redirect("no-access")
    following_list = [user.following_user for user in request.user.following.all()]
    context = {
        "following_list": following_list,
    }
    return render(request, 'profile.html', context)


def profile_edit(request):
    if not request.user.is_authenticated:
        return redirect("no-access")
    form = ProfileForm(instance=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect("profile")
    context = {
        "form": form,
    }
    return render(request, "edit-profile.html", context)


def users_profile(request, user_id):
    if not request.user.is_authenticated:
        return redirect("no-access")
    user = User.objects.get(id=user_id)
    events = Event.objects.filter(organizer=user).order_by("datetime")
    followed = UserFollowing.objects.filter(user=request.user, following_user=user)
    context = {
        "user": user,
        "events": events,
        "followed": followed,
    }
    return render(request, 'users-profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'change_password.html', context)


def follow_user(request, user_id):
    if not request.user.is_authenticated:
        return redirect("no-access")
    user = User.objects.get(id=user_id)
    if UserFollowing.objects.filter(user=request.user, following_user=user):
        messages.warning(request, "Can't follow the same user twice!!")
        return redirect("users-profile", user.id)
    follow = UserFollowing(user=request.user, following_user=user)
    follow.save()
    messages.success(request, f"You started following {user.username}")
    return redirect("users-profile", user.id)


def unfollow_user(request, user_id):
    if not request.user.is_authenticated:
        return redirect("no-access")
    user = User.objects.get(id=user_id)
    if UserFollowing.objects.filter(user=request.user, following_user=user):
        follow = UserFollowing.objects.get(user=request.user, following_user=user)
        follow.delete()
        messages.success(request, f"You unfollowed {user.username}")
        return redirect("users-profile", user.id)


class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")


def no_access(request):
    return render(request, "no_access.html")
