import json
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APITestCase
from mixer.backend.django import mixer
from django.contrib.auth.models import User

from projects.views import ProjectModelViewSet, ToDoModelViewSet
from users.models import User
from projects.models import Project, ToDo


class TestProjectModelViewSet(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('django', 'django@gb.local', 'geekbrains')
        self.test_user = User.objects.create_user('test_user', 'test_user@gb.local', 'geekbrains')
        self.project = Project.objects.create(name='test_project_name', repo_url='https://www.test.github.com/')
        self.project_data = {"name": "test_project_name", "repo_url": "https://www.test.github.com/",
                             "users": [self.superuser.uuid]}
        self.project_data_upd = {'name': 'test_name_upd', 'repo_url': 'https://www.test.com/',
                                 'users': [self.test_user.uuid]}

    """ List projects """
    def test_get_list_guest(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_auth(self):
        self.client.login(username='test_user', password='geekbrains')
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_admin(self):
        self.client.login(username='django', password='geekbrains')
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """ Detail projects """

    def test_get_detail_projects_for_guest(self):
        response = self.client.get(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detail_projects_for_user(self):
        self.client.login(username='test_user', password='geekbrains')
        response = self.client.get(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_projects_for_admin(self):
        self.client.login(username='django', password='geekbrains')
        response = self.client.get(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """ Create projects """

    def test_create_project_for_guest(self):
        factory = APIRequestFactory()
        request = factory.post('/api/projects/', self.project_data, format='json')
        view = ProjectModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_project_for_user(self):
        factory = APIRequestFactory()
        request = factory.post('/api/projects/', self.project_data, format='json')
        force_authenticate(request, user=self.test_user)
        view = ProjectModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_project_for_admin(self):
        factory = APIRequestFactory()
        request = factory.post('/api/projects/', self.project_data, format='json')
        force_authenticate(request, user=self.superuser)
        view = ProjectModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



    """ Delete projects """

    def test_delete_project_for_guest(self):
        project = mixer.blend(Project)
        client = APIClient()
        response = client.delete(f'/api/projects/{project.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_project_for_user(self):
        project = mixer.blend(Project)
        client = APIClient()
        client.login(username='test_user', password='geekbrains')
        response = client.delete(f'/api/projects/{project.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        client.logout()

    def test_delete_project_for_admin(self):
        project = mixer.blend(Project)
        client = APIClient()
        client.login(username='django', password='geekbrains')
        response = client.delete(f'/api/projects/{project.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        client.logout()

    """ Edit projects """

    def test_edit_project_for_guest(self):
        response = self.client.put(f'/api/projects/{self.project.id}/', self.project_data_upd)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_edit_project_for_user(self):
        project = mixer.blend(Project)
        self.client.force_login(user=self.test_user)
        response = self.client.put(f'/api/projects/{project.id}/', self.project_data_upd, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project = Project.objects.get(id=project.id)
        self.assertEqual(project.name, self.project_data_upd['name'])
        self.assertEqual(project.repo_url, self.project_data_upd['repo_url'])

    def test_edit_project_for_admin(self):
        project = mixer.blend(Project)
        self.client.force_login(user=self.superuser)
        response = self.client.put(f'/api/projects/{project.id}/', self.project_data_upd, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project = Project.objects.get(id=project.id)
        self.assertEqual(project.name, self.project_data_upd['name'])
        self.assertEqual(project.repo_url, self.project_data_upd['repo_url'])


class TestToDoModelViewSet(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('django', 'django@gb.local', 'geekbrains')
        self.user = User.objects.create_user('test_user', 'test_user@gb.local', 'geekbrains')
        self.project = Project.objects.create(name='test_project_name', repo_url='https://www.test.github.com/')
        self.todo = ToDo.objects.create(name='test_todo_name', text='test_text', is_active=1,
                                        project_id=self.project, user_id=self.user)
        self.todo_data = {'name': 'test_todo_name', 'text': 'test_todo_text', 'is_active': 1,
                          'project_id': f"http://127.0.0.1:8000/api/projects/{self.project.id}/",
                          'user_id': f'http://127.0.0.1:8000/api/users/{self.user.uuid}/'}
        self.todo_data_upd = {'name': 'test_todo_name_upd', 'text': 'test_todo_text_upd', 'is_active': 0}

    """List todos"""

    def test_get_list_guest(self):
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_auth(self):
        self.client.login(username='test_user', password='geekbrains')
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_admin(self):
        self.client.login(username='django', password='geekbrains')
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """Detail todos"""

    def test_get_detail_todo_for_guest(self):
        client = APIClient()
        response = client.get(f'/api/todos/{self.todo.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detail_todo_for_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get(f'/api/todos/{self.todo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_todo = json.loads(response.content)
        self.assertEqual(response_todo['name'], 'test_todo_name')
        self.assertEqual(response_todo['text'], 'test_text')

    def test_get_detail_todo_for_admin(self):
        self.client.force_login(user=self.superuser)
        response = self.client.get(f'/api/todos/{self.todo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_todo = json.loads(response.content)
        self.assertEqual(response_todo['name'], 'test_todo_name')
        self.assertEqual(response_todo['text'], 'test_text')

    """Create todos"""

    def test_create_todo_for_guest(self):
        factory = APIRequestFactory()
        request = factory.post('/api/todos/', self.todo_data, format='json')
        view = ToDoModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_todo_for_admin(self):
        factory = APIRequestFactory()
        request = factory.post('/api/todos/', self.todo_data, format='json')
        force_authenticate(request, user=self.superuser)
        view = ToDoModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_todo_for_user(self):
        factory = APIRequestFactory()
        request = factory.post('/api/todos/', self.todo_data, format='json')
        force_authenticate(request, user=self.user)
        view = ToDoModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    """Edit todos"""

    def test_edit_todo_for_guest(self):
        client = APIClient()
        response = client.patch(f'/api/todos/{self.todo.id}/', self.todo_data_upd)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_todo_for_user(self):
        todo = mixer.blend(ToDo)
        self.client.force_login(user=self.user)
        response = self.client.patch(f'/api/todos/{todo.id}/', self.todo_data_upd)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo = ToDo.objects.get(id=todo.id)
        self.assertEqual(todo.name, self.todo_data_upd['name'])
        self.assertEqual(todo.text, self.todo_data_upd['text'])
        self.assertEqual(todo.is_active, self.todo_data_upd['is_active'])

    def test_edit_todo_for_admin(self):
        todo = mixer.blend(ToDo)
        self.client.force_login(user=self.superuser)
        response = self.client.patch(f'/api/todos/{todo.id}/', self.todo_data_upd)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo = ToDo.objects.get(id=todo.id)
        self.assertEqual(todo.name, self.todo_data_upd['name'])
        self.assertEqual(todo.text, self.todo_data_upd['text'])
        self.assertEqual(todo.is_active, self.todo_data_upd['is_active'])

    """Delete todos"""

    def test_delete_todo_for_guest(self):
        response = self.client.delete(f'/api/todos/{self.todo.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_todo_for_user(self):
        todo = mixer.blend(ToDo)
        self.client.force_login(user=self.user)
        response = self.client.delete(f'/api/todos/{todo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo = ToDo.objects.get(id=todo.id)
        self.assertEqual(todo.is_active, 0)

    def test_delete_todo_for_admin(self):
        todo = mixer.blend(ToDo)
        self.client.force_login(user=self.superuser)
        response = self.client.delete(f'/api/todos/{todo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo = ToDo.objects.get(id=todo.id)
        self.assertEqual(todo.is_active, 0)
