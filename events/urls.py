from django.urls import path
from events import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('events/', views.event_list, name='event-list'),
    path('events/<int:event_id>/', views.event_detail, name='event-detail'),
    path('events/create/', views.event_create, name='event-create'),
    path('events/<int:event_id>/update/', views.event_update, name='event-update'),
    path('events/<int:event_id>/book/', views.book_event, name='book-event'),

    path("profile/", views.profile_detail, name="profile"),
    path("profile/edit/", views.profile_edit, name="edit-profile"),
    path("profile/change-password/", views.change_password, name="change-password"),
    path("profile/<int:user_id>/", views.users_profile, name="users-profile"),
    path("profile/<int:user_id>/follow/", views.follow_user, name="follow-user"),
    path("profile/<int:user_id>/unfollow/", views.unfollow_user, name="unfollow-user"),

    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel-booking'),

    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('no-access/', views.no_access, name='no-access'),
]
