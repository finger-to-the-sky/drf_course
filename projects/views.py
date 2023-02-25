from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from projects.models import Project, ToDo
from projects.serializers import ProjectModelSerializer, ToDoModelSerializer
from projects.filtres import ProjectFilter, ToDoFilter
from rest_framework.permissions import IsAuthenticated, AllowAny


class ProfileLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10


class ToDoLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20


class ProjectModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.get_queryset().order_by('id')
    serializer_class = ProjectModelSerializer
    pagination_class = ProfileLimitOffsetPagination
    filterset_class = ProjectFilter


class ToDoModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ToDo.objects.get_queryset().order_by('project_id')
    serializer_class = ToDoModelSerializer
    pagination_class = ToDoLimitOffsetPagination
    filterset_class = ToDoFilter

    def destroy(self, request, pk=None, **kwargs):
        todo = get_object_or_404(ToDo, pk=pk)
        todo.is_active = False
        todo.save()
        return Response(ToDoModelSerializer(todo, context={'request': request}).data)