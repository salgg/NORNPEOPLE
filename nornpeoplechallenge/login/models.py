from django.db import models
from django.contrib.auth.models import User

'''
    Clase para los campos extras necesarios en el user
'''
class UserOptions(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    changePassCode = models.TextField(max_length=35, blank=True, default="") # campo que almacena un código si se necesita cambiar la contraseña

    def __str__(self):
        return str(self.user)

'''
    Clase para los logins 
'''
class LoginLog(models.Model):
    datetimeLog = models.DateTimeField(auto_now_add=True, blank=True)
    userLog = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.datetimeLog) + " " + str(self.userLog)