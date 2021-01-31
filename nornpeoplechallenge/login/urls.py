from django.urls import path
from login.views import Login_, Logout_, Welcome, RecoverPassword, ChangePassword

urlpatterns = [
    path('', Login_.as_view(), name="login_"),
    path('logout', Logout_.as_view(), name="logout_"),
    path('bienvenido', Welcome.as_view(), name="welcome"),
    path('recuperar', RecoverPassword.as_view(), name="recoverPassword"),
    path('cambiar_contraseña', ChangePassword.as_view(), name="changePassword"),
]