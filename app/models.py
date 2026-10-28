
from django.db import models


class users(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email

class Task(models.Model):
    user = models.ForeignKey(
        users,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title