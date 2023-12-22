from django.urls import path
from . import views

urlpatterns = [
    path("cadastro/", views.cadastro, name="cadastro_url"),
    path("login/", views.login, name="login_url"),
    path("logout/", views.logout, name="logout_url"),
]
