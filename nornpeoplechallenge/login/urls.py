from django.urls import path
from login.views import Login_, Logout_, Welcome

urlpatterns = [
    path('', Login_.as_view(), name="login_"),
    path('logout', Logout_.as_view(), name="logout_"),
    path('bienvenido', Welcome.as_view(), name="welcome"),
]