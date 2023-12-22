from django.contrib import admin
from .models import Cidade, DiasVisita, Horario, Imagem, Imovel, Visita
from django.utils.html import format_html

# Register your models here.


@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ("rua", "valor", "quartos", "tamanho", "cidade", "tipo")
    list_editable = ("valor", "tipo")
    list_filter = ("cidade", "tipo")


@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")


admin.site.register(DiasVisita)
admin.site.register(Horario)
admin.site.register(Imagem)


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    def foto_preview(self, obj):
        return format_html(
            f"<img src='{{self.imovel.imagens.all.0}} width=30px height=30px'/>"
        )


# admin.site.register(Visita)
