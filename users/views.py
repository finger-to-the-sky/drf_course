from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserModelSerializer, UserModelSerializerV2
from rest_framework.permissions import IsAuthenticated


class UserModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.get_queryset().order_by('uuid')
    serializer_class = UserModelSerializer

    def get_serializer_class(self):
        if self.request.version == '0.2':
            return UserModelSerializerV2
        return UserModelSerializer
