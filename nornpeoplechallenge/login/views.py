from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from login.models import LoginLog


# Create your views here.

class Welcome(LoginRequiredMixin, TemplateView):

    template_name = "login/welcome.html"
    login_url = '/'

    def post(self, request):
        context = {}
        return render(request, self.template_name, context)



class Login_(TemplateView):

    template_name = "login/login.html"
    context = {}

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('welcome')
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                newlog = LoginLog(user=user)
                newlog.save()
                return redirect('welcome')
        self.context["error"] = "usuario no registrado o inactivo"
        return render(request, self.template_name, self.context)
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('welcome')
        return render(request, self.template_name, self.context)


class Logout_(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        logout(request)
        return redirect('login_')
    
    def post(self, request):
        logout(request)
        return redirect('login_')
