from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LoginLog(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)