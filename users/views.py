from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserModelSerializer
from rest_framework.permissions import IsAuthenticated


class UserModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer