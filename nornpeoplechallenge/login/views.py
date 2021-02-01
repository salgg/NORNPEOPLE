import smtplib, uuid
from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from login.models import LoginLog, UserOptions
from django.contrib.auth.models import User
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
                if not UserOptions.objects.filter(user=user).exists(): # si el usuario es nuevo se crean sus opciones que servirán para recuperar contraseña
                    newUserOp = UserOptions(user=user)
                    newUserOp.save()
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
        if email is None or email is "" or not User.objects.filter(email=email).exists():
            context = {"alert": "Correo no registrado o nulo"}
        else:
            newCode = str(uuid.uuid4().hex) # genera un códiog único
            if self.sendEmailPassword(email=email, newCode=newCode): #, develop=False): # usar esto en modo producción
                context = {"alert": "Hemos enviado a tu correo un código para poder crear una contraseña nueva, recomendamos revisar tu spam "}
                user = User.objects.filter(email=email)[0]
                userOp = UserOptions.objects.get(user=user)
                userOp.changePassCode = newCode
                userOp.save()
            else:
                context = {"alert": "Error. Si persiste, favor de contactar a el encargado "}
        return render(request, self.template_name, context)

    def sendEmailPassword(self, email, newCode , debug=True):
        mailText= 'El código para recuperar tu contraseña de Nornpeoplechallenge es: \n' + newCode + ' \n podrás cambiarla al inicio donde dice "olvidé mi contaseña" --> "¿Ya tienes el código?" \n si no has sido tu quien lo ha pedido haz caso omiso de este correo"'
        sender_email = "correosinsentidoquehiceparauntesteochallenge@outlook.com"
        email_subject = "Crear una nueva contraseña para NORNPEOPLECHALLENGE"
        if debug:
            smtp_server = "smtp.office365.com"
            port = 587
            sender_password = "notevoyadecirmipassword1"
            message = MIMEMultipart()
            message["Subject"] = email_subject
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
                    email_subject,
                    mailText,
                    sender_email,
                    [email],
                    fail_silently=False,
                )
                return True
            except:
                return False

'''
    Clase para cambiar la contraseña
'''
class ChangePassword(TemplateView):
    template_name = 'login/changePassword.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request):
        context = {"alert":""}
        newPass = request.POST.get("newPassword", "")
        newPassR = request.POST.get("newPasswordRep", "")
        if newPass is "" or newPassR is "":
            context = {"alert": "Los campos no pueden estar en blanco"}
        if newPass != newPassR:
            context = {"alert": "Las contraseñas no coinciden"}
        if context["alert"] != "":
            return render(request, self.template_name, context)
        if request.user.is_authenticated:
            oldPass = request.POST.get("oldPassword", "")
            username=request.user.username
            if oldPass is "":
                context = {"alert": "Los campos no pueden estar en blanco"}
            elif authenticate(request, username=username, password=oldPass) is None:
                context = {"alert": "La contraseña actual no es correcta, favor de volver a intentar"}
            else:
                user = User.objects.get(username=username)
                user.set_password(newPass)
                user.save()
                context = {"alert": "Tu contraseña ha sido cambiada"}
        else:
            codeChange = request.POST.get("codeChange","") 
            if codeChange is "" or not UserOptions.objects.filter(changePassCode=codeChange).exists():
                context = {"alert": "código incorrecto o nulo"}
            else:
                codeOptUser = UserOptions.objects.get(changePassCode=codeChange)
                user = User.objects.get(username=codeOptUser.user.username)
                user.set_password(newPass)
                user.save()
                codeOptUser.changePassCode = ""
                codeOptUser.save()
                context = {"alert": "Tu contraseña ha sido cambiada"}

        return render(request, self.template_name, context)
