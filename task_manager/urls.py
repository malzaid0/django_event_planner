"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from boards import views
urlpatterns = [
    path('admin/', admin.site.urls),

    path("create/", views.CreateBoard.as_view(), name="create-board"),
    path("boards/", views.BoardsList.as_view(), name="boards-list"),
    path("boards/<int:board_id>/", views.BoardDetail.as_view(), name="board-detail"),
    path("boards/<int:board_id>/delete/", views.DeleteBoard.as_view(), name="delete-board"),

    path("boards/<int:board_id>/create_task/", views.CreateTask.as_view(), name="create-task"),
    path("boards/<int:board_id>/task/<int:task_id>/update/", views.UpdateTask.as_view(), name="update-task"),
    path("boards/<int:board_id>/task/<int:task_id>/delete/", views.DeleteTask.as_view(), name="delete-task"),
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('register/', views.Register.as_view(), name="register"),
]
