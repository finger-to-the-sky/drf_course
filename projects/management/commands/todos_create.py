from django.core.management.base import BaseCommand
from django.db import transaction

import factory
from factory.django import DjangoModelFactory

from projects.models import Project, ToDo
from users.models import User


class TodoFactory(DjangoModelFactory):
    class Meta:
        model = ToDo

    user_id = factory.Iterator([i for i in User.objects.all()])
    project_id = factory.Iterator([i for i in Project.objects.all()])
    name = factory.Faker('company')
    text = factory.Faker('text')
    is_active = factory.Faker('pybool')
    created_at = factory.Faker('date_time')
    update_at = factory.Faker('date_time')


class Command(BaseCommand):
    help = 'Create todos for test...'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Deleting old data')
        ToDo.objects.all().delete()
        count = options['count']
        self.stdout.write('Creating new todos')
        todos = []

        for _ in range(count):
            todo = TodoFactory()
            todos.append(todo)
            print(f'todo {todo.name} created!')
        print('Done!')