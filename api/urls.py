from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api import views

urlpatterns = [
    path('events/create/', views.CreateEvent.as_view(), name='api-event-create'),
    path('events/', views.EventsList.as_view(), name='api-event-list'),
    path('events/<int:event_id>/bookers/', views.EventBookers.as_view(), name='api-event-bookers'),
    path('events/<int:event_id>/book/', views.BookEvent.as_view(), name='api-book-event'),

    path('user/<int:user_id>/events/', views.UsersEventsList.as_view(), name='api-user-event-list'),
    path('user/<int:user_id>/follow/', views.FollowUser.as_view(), name='api-follow-user'),

    path('my-bookings/', views.MyBookings.as_view(), name='api-my-bookings'),
    path('followings/', views.MyFollowings.as_view(), name='api-followings'),

    path('login/', TokenObtainPairView.as_view(), name="api-login"),
    path('token/refresh/', TokenRefreshView.as_view(), name="api-token-refresh"),
    path('register/', views.Register.as_view(), name="api-register"),
]
