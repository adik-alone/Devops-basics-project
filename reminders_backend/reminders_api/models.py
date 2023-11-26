from django.db import models
from django.contrib.auth.models import User


class Reminder(models.Model):
    creator = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    content = models.TextField(max_length=1024, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    is_done = models.BooleanField(default=False)
    is_important = models.BooleanField(default=False)
