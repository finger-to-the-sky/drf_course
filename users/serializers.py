from rest_framework.serializers import HyperlinkedModelSerializer
from users.models import User


class UserModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'first_name', 'last_name', 'username', 'email')


class UserModelSerializerV2(HyperlinkedModelSerializer):
    class Meta(UserModelSerializer.Meta):
        model = User
        fields = ('uuid', 'url', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff')