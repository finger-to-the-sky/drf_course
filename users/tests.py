from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from .views import UserModelViewSet
from .models import User


class TestUserModelViewSet(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('django', 'django@gb.local' , 'geekbrains')
        self.user = User.objects.create_user('test_user', 'test_user@gb.local', 'geekbrains')
        self.user_data = {'username': 'test_user', "first_name": "testerFN", "last_name": "testerLN",
                          "email": "test_user@gb.local"}
        self.user_data_upd = {'username': 'user_upd', "first_name": "first_name_upd", "last_name": "last_name_upd",
                              "email": "email_updr@gb.local"}

    def test_get_list_guest(self):
        factory = APIRequestFactory()
        request = factory.get('/api/users/')
        view = UserModelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_auth(self):
        factory = APIRequestFactory()
        request = factory.get('/api/users/')
        force_authenticate(request, user=self.user)
        view = UserModelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_guest(self):
        factory = APIRequestFactory()
        request = factory.post('/api/users/', self.user_data)
        view = UserModelViewSet.as_view({'post': 'update'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detail_guest(self):
        client = APIClient()
        response = client.get(f'/api/users/{self.user.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detail_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(f'/api/users/{self.user.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_admin(self):
        client = APIClient()
        client.force_authenticate(user=self.superuser)
        response = client.get(f'/api/users/{self.user.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_guest(self):
        client = APIClient()
        response = client.put(f'/api/users/{self.user.uuid}/', self.user_data_upd)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_admin(self):
        user = mixer.blend(User)
        client = APIClient()
        client.login(username='django', password='geekbrains')
        response = client.put(f'/api/users/{user.uuid}/', self.user_data_upd)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(uuid=user.uuid)
        self.assertEqual(user.username, self.user_data_upd['username'])
        self.assertEqual(user.first_name, self.user_data_upd['first_name'])
        self.assertEqual(user.last_name, self.user_data_upd['last_name'])
        self.assertEqual(user.email, self.user_data_upd['email'])
        client.logout()

    def test_edit_user(self):
        user = mixer.blend(User)
        client = APIClient()
        client.login(username='test_user', password='geekbrains')
        response = client.put(f'/api/users/{user.uuid}/', self.user_data_upd)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(uuid=user.uuid)
        self.assertEqual(user.username, self.user_data_upd['username'])
        self.assertEqual(user.first_name, self.user_data_upd['first_name'])
        self.assertEqual(user.last_name, self.user_data_upd['last_name'])
        self.assertEqual(user.email, self.user_data_upd['email'])
        client.logout()