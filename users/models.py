from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField(blank=True, unique=True)

    def __str__(self):
        return f'user {self.first_name} {self.last_name}'
