from django.contrib import admin
from login.models import LoginLog, UserOptions
# Register your models here.

class adminLoginLog(admin.ModelAdmin):
    pass

class adminUserOptions(admin.ModelAdmin):
    pass

admin.site.register(LoginLog, adminLoginLog)
admin.site.register(UserOptions, adminUserOptions)