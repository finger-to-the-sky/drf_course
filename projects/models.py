from django.db import models

from users.models import User


class Project(models.Model):
    name = models.CharField(max_length=32)
    url = models.URLField()
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ToDo(models.Model):
    user_id = models.ForeignKey(User, models.PROTECT)
    project_id = models.ForeignKey(Project, models.PROTECT)
    name = models.CharField(max_length=32)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.update_at}'