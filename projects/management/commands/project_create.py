import random
from django.core.management.base import BaseCommand
from django.db import transaction
import factory
from factory.django import DjangoModelFactory
from projects.models import Project
from users.models import User

class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker('word')
    url = factory.Faker('url')
    created_at = factory.Faker('date_time')


class Command(BaseCommand):
    help = 'Create project django & project test'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Deleting old data...')
        Project.objects.all().delete()
        count = options['count']
        self.stdout.write('Creating new projects...')
        projects = []

        for _ in range(count):
            project = ProjectFactory()
            users = random.choices([i for i in User.objects.all()], k=random.randint(2, 5))
            project.users.add(*users)
            projects.append(project)
            print(f'Project {project.name} created')
        print('Done!')