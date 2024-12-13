from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    bio = models.CharField(max_length=300, blank=True, null=True)
    work = models.CharField(max_length=150, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username


class Calculations(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    datas = models.JSONField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_created_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Calculation"
        verbose_name_plural = "Calculations"

    def __str__(self):
        return f"Created_by: {str(self.created_by).title()} >>> Calc_name: {self.name.title()} >>> ID: {self.pk}"
    


class ContactUs(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Full Name")
    email = models.EmailField(blank=False, verbose_name="Email Address")
    subject = models.CharField(max_length=100, blank=False, verbose_name="Subject")
    message = models.TextField(blank=False, verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted At")
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Contact Query"
        verbose_name_plural = "Contact Queries"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Query from {self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"
    

    

