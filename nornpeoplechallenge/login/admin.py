from django.contrib import admin
from login.models import LoginLog
# Register your models here.

class adminLoginLog(admin.ModelAdmin):
    pass

admin.site.register(LoginLog, adminLoginLog)