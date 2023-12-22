from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth


# Create your views here.
def cadastro(req):
    if req.user.is_authenticated:
        return redirect("/")
    if req.method == "GET":
        return render(request=req, template_name="cadastro.html", context={})
    if req.method == "POST":
        username = req.POST.get("username")
        email = req.POST.get("email")
        senha = req.POST.get("senha")

        if (
            len(username.strip()) == 0
            or len(email.strip()) == 0
            or len(senha.strip()) == 0
        ):
            messages.add_message(
                req, constants.ERROR, "Todos os campos precisam ser preenchidos"
            )
            return redirect("/auth/cadastro/")

        user = User.objects.filter(username=username)

        if len(user) > 0:
            messages.add_message(req, constants.ERROR, "Usuário já existe")
            return redirect("/auth/cadastro/")

        try:
            user = User.objects.create_user(
                username=username, email=email, password=senha
            )
            user.save()
            messages.add_message(
                req, constants.SUCCESS, "Usuário cadastrado com sucesso"
            )
            return redirect("/auth/login/")
        except:
            messages.add_message(req, constants.ERROR, "Erro interno do sistema")
            return redirect("auth/cadastro/")


def login(req):
    if req.user.is_authenticated:
        return redirect("/")
    if req.method == "GET":
        return render(req, "login.html", context={})
    if req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("senha")

        user = auth.authenticate(req, username=username, password=password)

        if not user:
            messages.add_message(req, constants.ERROR, "Username ou Senha inválidos")
            return redirect("/auth/login/")

        auth.login(req, user=user)
        return redirect("/")


def logout(req):
    auth.logout(req)
    return redirect("/auth/login/")
