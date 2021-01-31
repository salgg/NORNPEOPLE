from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LoginLog(models.Model):
    datetimeLog = models.DateTimeField(auto_now_add=True, blank=True)
    userLog = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.datetimeLog) + " " + str(self.userLog)