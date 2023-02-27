from django.core.management.base import BaseCommand
from django.db import transaction

import factory
from factory.django import DjangoModelFactory

from users.models import User
from projects.models import ToDo


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')


class Command(BaseCommand):
    help = 'Create superuser django & users to test'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        User.objects.all().delete()
        ToDo.objects.all().delete()
        count = options['count']
        superuser = User.objects.create_superuser(
            username='admin',
            email='django@gb.local',
            first_name='Джанго',
            last_name='Фреймворков',
            password='geekbrains',
        )
        print(f'Суперпользователь {superuser.username} создан')
        self.stdout.write("Creating new users...")
        people = []
        for _ in range(count):
            person = UserFactory()
            people.append(person)
            print(f'{person} создан')
        print('Done!')