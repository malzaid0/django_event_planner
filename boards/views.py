from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import RegisterSerializer, CreateBoardSerializer, BoardListSerializer, CreateTaskSerializer, \
    BoardDetailSerializer, UpdateTaskSerializer, BoardAllDetailSerializer
from .models import Board, Task
from .permissions import IsBoardOwner


class Register(CreateAPIView):
    serializer_class = RegisterSerializer


class CreateBoard(CreateAPIView):
    serializer_class = CreateBoardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BoardsList(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated]


class BoardDetail(RetrieveAPIView):
    queryset = Board.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "board_id"
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        board = Board.objects.get(id=self.kwargs.get("board_id"))
        if board.owner == self.request.user:
            return BoardAllDetailSerializer
        else:
            return BoardDetailSerializer


class CreateTask(CreateAPIView):
    serializer_class = CreateTaskSerializer
    permission_classes = [IsAuthenticated, IsBoardOwner]

    def perform_create(self, serializer):
        board = Board.objects.get(id=self.kwargs.get("board_id"))
        if board.owner == self.request.user:
            serializer.save(board=board)


class UpdateTask(RetrieveUpdateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'task_id'
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateTaskSerializer

    def get_queryset(self):
        board = Board.objects.get(id=self.kwargs.get("board_id"))
        if board.owner == self.request.user:
            return Task.objects.filter(board=board)


class DeleteTask(DestroyAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'task_id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board = Board.objects.get(id=self.kwargs.get("board_id"))
        if board.owner == self.request.user:
            return Task.objects.filter(board=board)


class DeleteBoard(DestroyAPIView):
    queryset = Board.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'task_id'
    permission_classes = [IsAuthenticated, IsBoardOwner]
