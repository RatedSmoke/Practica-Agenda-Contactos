from django.contrib import admin
from catalogos.models import Estado

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display  = ['clave', 'nombre', 'activo']
    search_fields = ['clave', 'nombre']
    ordering      = ['nombre']
    list_filter   = ['activo']
