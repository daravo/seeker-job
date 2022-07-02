from atexit import register
from django.contrib import admin
from .models import *
# Register your models here.
class CanalMensajeInline(admin.TabularInline):
    model=CanalMensaje
    extra=1

class CanalUsuarioInline(admin.TabularInline):
    model=CanalUsuario
    extra=1

class CanalAdmin(admin.ModelAdmin):
    inlines=[CanalMensajeInline, CanalUsuarioInline]

    class Meta:
        model=Canal

admin.site.register(Empresa)
admin.site.register(OfertaEmpleo)
admin.site.register(Usuario)
admin.site.register(Canal, CanalAdmin)
admin.site.register(CanalUsuario)
admin.site.register(CanalMensaje)
admin.site.register(PuestoDeTrabajo)
admin.site.register(EstudiosMinimos)
admin.site.register(JornadaLaboral)
admin.site.register(TipoContrato)
admin.site.register(Presencialidad)
admin.site.register(Titulos)
admin.site.register(IdiomaNiveles)
admin.site.register(Idiomas)
admin.site.register(ExperienciaLaboral)