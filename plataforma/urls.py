from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home_url"),
    path("imovel/<str:id>", views.imovel, name="imovel_url"),
    path("agendar_visita/<str:id>", views.visita, name="visita_url"),
    path("agendamentos/", views.agendamentos, name="agendamentos_url"),
    path(
        "cancelar_agendamento/<str:id>",
        views.cancelar_agendamento,
        name="cancelar_agendamento_url",
    ),
]
