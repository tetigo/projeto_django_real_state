from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html

# Create your models here.


class Imagem(models.Model):
    img = models.ImageField(upload_to="img")

    def __str__(self) -> str:
        return self.img.url


class Cidade(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.nome


class DiasVisita(models.Model):
    choices = (
        ("SEG", "Segunda"),
        ("TER", "Terça"),
        ("QUA", "Quarta"),
        ("QUI", "Quinta"),
        ("SEX", "Sexta"),
        ("SAB", "Sábado"),
        ("DOM", "Domingo"),
    )

    dia = models.CharField(max_length=20, choices=choices)

    def __str__(self) -> str:
        return self.dia


class Horario(models.Model):
    horario = models.TimeField()

    def __str__(self):
        return f"{self.horario}"


class Imovel(models.Model):
    choices = (
        ("V", "Venda"),
        ("A", "Aluguel"),
    )
    choices_imovel = (
        ("A", "Apartamento"),
        ("C", "Casa"),
    )
    choices_status = (
        ("D", "Disponível"),
        ("I", "Indisponível"),
    )
    imagens = models.ManyToManyField(Imagem)
    valor = models.FloatField()
    quartos = models.IntegerField()
    tamanho = models.FloatField()
    cidade = models.ForeignKey(Cidade, on_delete=models.DO_NOTHING)
    rua = models.CharField(max_length=50)
    tipo = models.CharField(max_length=1, choices=choices)
    tipo_imovel = models.CharField(max_length=1, choices=choices_imovel)
    numero = models.IntegerField()
    descricao = models.TextField()
    dias_visita = models.ManyToManyField(DiasVisita)
    horarios = models.ManyToManyField(Horario)
    status = models.CharField(max_length=12, choices=choices_status, default="D")

    def __str__(self) -> str:
        return self.rua


class Visita(models.Model):
    choices_status = (
        ("A", "Agendado"),
        ("F", "Finalizado"),
        ("C", "Cancelado"),
    )

    imovel = models.ForeignKey(Imovel, on_delete=models.DO_NOTHING, default=None)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=choices_status)
    dia = models.CharField(max_length=20)
    horario = models.TimeField()

    def __str__(self) -> str:
        return f"{self.dia} às {self.horario} : {self.imovel.rua}"
