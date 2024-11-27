from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    def __str__(self):
        return self.username


class Circuits(models.Model):
    name = models.CharField(max_length=100)
    content_type = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_created', null=True, blank=True)

    class Meta:
        verbose_name = "Circuit"
        verbose_name_plural = "Circuits"


    def __str__(self):
        return self.name


    