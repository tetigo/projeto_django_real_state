from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import DiasVisita, Horario, Imovel, Cidade, Visita
from django.contrib.messages import constants
from django.contrib import messages

# Create your views here.


@login_required(login_url="/auth/login/")
def home(req):
    if req.method == "GET":
        imoveis = Imovel.objects.filter(status="D")
        cidades = Cidade.objects.all()
        return render(
            req, "home.html", context={"imoveis": imoveis, "cidades": cidades}
        )
    if req.method == "POST":
        preco_minimo = req.POST.get("preco_minimo")
        preco_maximo = req.POST.get("preco_maximo")
        cidade = int(req.POST.get("cidade"))
        tipo = req.POST.getlist("tipo")

        print(">>>", tipo)

        if not preco_minimo:
            preco_minimo = 0
        if not preco_maximo:
            preco_maximo = 999999999
        if not tipo:
            tipo = ["A", "C"]

        imoveis = (
            Imovel.objects.filter(valor__gte=preco_minimo)
            .filter(valor__lte=preco_maximo)
            .filter(tipo_imovel__in=tipo)
        )
        if not cidade == 0:
            imoveis = imoveis.filter(cidade=cidade)

        cidades = Cidade.objects.all()
        return render(
            req, "home.html", context={"imoveis": imoveis, "cidades": cidades}
        )


@login_required(login_url="/auth/login/")
def imovel(req, id):
    imovel = get_object_or_404(Imovel, id=id)
    sugestoes = Imovel.objects.filter(cidade=imovel.cidade).exclude(id=id)[0:2]
    return render(
        req, "imovel.html", context={"imovel": imovel, "sugestoes": sugestoes, "id": id}
    )


@login_required(login_url="/auth/login/")
def visita(req, id):
    if req.method == "GET":
        ...
    if req.method == "POST":
        try:
            choices_status = (
                ("A", "Agendado"),
                ("F", "Finalizado"),
                ("C", "Cancelado"),
            )

            usuario = req.user
            dia = req.POST.get("dia")
            horario = req.POST.get("horario")
            id_imovel = req.POST.get("id_imovel")

            imovel = Imovel.objects.get(id=id_imovel)

            if not imovel:
                messages.add_message(req, constants.ERROR, "Imóvel não localizado")
                return redirect("imovel_url", id=id)

            visita = Visita()
            visita.imovel = imovel
            visita.usuario = usuario
            visita.dia = dia
            visita.horario = horario
            visita.status = "A"
            visita.save()

            return redirect("/agendamentos")

        except Exception as e:
            messages.add_message(req, constants.ERROR, f"{e}")
            messages.add_message(
                req,
                constants.ERROR,
                "Erro interno do sistema. Tente novamente",
            )
            return redirect("imovel_url", id=id)


@login_required(login_url="/auth/login/")
def agendamentos(req):
    visitas = Visita.objects.filter()
    return render(req, "agendamentos.html", context={"visitas": visitas})


@login_required(login_url="/auth/login/")
def cancelar_agendamento(req, id):
    visita = Visita.objects.get(id=id)
    visita.status = "C"
    visita.save()
    return redirect("/agendamentos")
