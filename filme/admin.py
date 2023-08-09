from django.contrib import admin
from .models import Filme, Epsodio, Usuario
from django.contrib.auth.admin import UserAdmin

# só existe para que o campo filmes_vistos apareça no admin
campos = list(UserAdmin.fieldsets)
campos.append(
    (
        "Histórico de Filmes",
        {
            "fields": (
                "filmes_vistos",
            )
        },
    )
)
UserAdmin.fieldsets = tuple(campos)



# Register your models here.
admin.site.register(Filme)
admin.site.register(Epsodio)
admin.site.register(Usuario, UserAdmin)