import string, random, smtplib, ssl
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from login.models import LoginLog
from django.contrib.auth.models import User, UserManager
from django.core.mail import send_mail
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


'''
    Clase para cuando entra una vez logueado
'''
class Welcome(LoginRequiredMixin, TemplateView):

    template_name = "login/welcome.html"
    login_url = '/'

    def get(self, request):
        try:
            user = User.objects.filter(username=request.user.username)[0]
        except:
            raise Http404("Error en la autentificación del usuario")
        context = { "logs": LoginLog.objects.filter(userLog=user) }
        return render(request, self.template_name, context)

'''
    Clase loguearse
'''
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
                newlog = LoginLog(userLog=user)
                newlog.save()
                return redirect('welcome')
        self.context["error"] = "usuario no registrado o inactivo"
        return render(request, self.template_name, self.context)
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('welcome')
        return render(request, self.template_name, self.context)

'''
    Clase para salir de la sesión
'''
class Logout_(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        logout(request)
        return redirect('login_')
    
    def post(self, request):
        logout(request)
        return redirect('login_')

'''
    Clase que manda una contraseña nueva al correo
'''
class RecoverPassword(TemplateView):
    template_name = "login/recoverPassword.html"

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)
    
    def post(self, request):
        context = {}
        email = request.POST.get("email", None)
        if email is None or email is "":
            context = {"alert": "Correo no registrado o nulo"}
        else:
            try:
                user = User.objects.filter(email=email)[0] #
            except:
                context = {"alert": "Correo no registrado o nulo"}
                return render(request, self.template_name, context)
            newPassword = self.createNewRandomPassword()
            if self.sendEmailPassword(email=email, password=newPassword): #, develop=False): # usar esto en modo producción
                context = {"alert": "Hemos enviado a tu correo la nueva contraseña, recomendamos revisar tu spam"}
                user.set_password(newPassword)
                user.save()
            else:
                context = {"alert": "Error. Si persiste, favor de contactar a el encargado "}
        return render(request, self.template_name, context)

    def sendEmailPassword(self, email, password , debug=True):
        mailText= 'Tu nueva contraseña es: \n' + password + ' \n Nota: Podrás cambiarla una vez entres en el enlace que dice ¨cambiar contaseña¨'
        sender_email = "correosinsentidoquehiceparauntesteochallenge@outlook.com"
        if debug:
            smtp_server = "smtp.office365.com"
            port = 587
            sender_password = "notevoyadecirmipassword1"
            message = MIMEMultipart()
            message["Subject"] = "Tu contraseña para NORNPEOPLECHALLENGE"
            message["From"] = sender_email
            message["To"] = email
            message.attach(MIMEText(mailText, 'plain'))
            try:
                server = smtplib.SMTP(smtp_server, port)
                server.ehlo()
                server.starttls()
                server.login(sender_email, sender_password)
                text = message.as_string()
                server.sendmail(sender_email, email, text)
                server.quit()
            except:
                return False
            return True
        else:    
            try:
                send_mail(
                    'Tu nueva contraseña para NORNPEOPLECHALLENGE',
                    mailText,
                    sender_email,
                    [email],
                    fail_silently=False,
                )
                return True
            except:
                return False


    def createNewRandomPassword(self):
        letters = string.ascii_letters + string.digits + "_"
        password = ""
        for i in range(10):
            password = password + random.choice(letters)
        return password

'''
    Clase para cambiar la contraseña
'''
class ChangePassword(LoginRequiredMixin, TemplateView):
    template_name = 'login/changePassword.html'
    login_url = '/'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)
        
    def post(self, request):
        context = {}
        oldPass = request.POST.get("oldPassword", "")
        newPass = request.POST.get("newPassword", "")
        newPassR = request.POST.get("newPasswordRep", "")
        username=request.user.username
        if oldPass is "" or newPass is "" or newPassR is "":
            context = {"alert": "Los campos no pueden estar en blanco"}
        elif newPass != newPassR:
            context = {"alert": "Las contraseñas no coinciden"}
        elif authenticate(request, username=username, password=oldPass) is None:
            context = {"alert": "La contraseña actual no es correcta, favor de volver a intentar"}
        else:
            user = User.objects.filter(username=username)[0]
            user.set_password(newPass)
            user.save()
            context = {"alert": "Tu contraseña ha sido cambiada"}
        
        return render(request, self.template_name, context)