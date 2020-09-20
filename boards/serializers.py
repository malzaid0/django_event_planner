from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Board, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class CreateBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["title"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["description", "creation_date", "is_done"]


class HiddenTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["description", "creation_date", "is_done", "is_hidden"]


class BoardDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ["title", "owner", "tasks"]

    def get_tasks(self, obj):
        tasks = Task.objects.filter(board=obj, is_hidden=False)
        return TaskSerializer(tasks, many=True).data


class BoardAllDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    tasks = serializers.SerializerMethodField()
    update = serializers.HyperlinkedIdentityField(view_name='update-task', lookup_field="id",
                                                  lookup_url_kwarg="task_id")

    class Meta:
        model = Board
        fields = ["title", "owner", "tasks", "update"]

    def get_tasks(self, obj):
        tasks = Task.objects.filter(board=obj)
        return HiddenTaskSerializer(tasks, many=True).data


class UpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["is_hidden", "is_done"]


class BoardListSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    detail = serializers.HyperlinkedIdentityField(view_name='board-detail', lookup_field="id",
                                                  lookup_url_kwarg="board_id")

    class Meta:
        model = Board
        fields = ["title", "owner", "detail"]


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["description", "is_hidden", "is_done"]


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
