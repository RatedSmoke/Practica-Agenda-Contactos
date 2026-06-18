from django.contrib import admin
from .models import Contacto, Direccion, Telefono

class DireccionInline(admin.StackedInline):
    model = Direccion
    extra = 1

class TelefonoInline(admin.TabularInline):
    model = Telefono
    extra = 1

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'apellidos', 'fecha_nacio', 'activo']
    search_fields = ['nombre', 'apellidos']
    ordering      = ['apellidos', 'nombre']
    list_filter   = ['activo']
    inlines       = [DireccionInline, TelefonoInline]

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display  = ['contacto', 'calle', 'numero_exterior', 'municipio', 'estado', 'activo']
    search_fields = ['calle', 'colonia', 'municipio']
    list_filter   = ['activo']

@admin.register(Telefono)
class TelefonoAdmin(admin.ModelAdmin):
    list_display  = ['contacto', 'tipo', 'alias', 'numero', 'activo']
    search_fields = ['numero', 'alias']
    list_filter   = ['tipo', 'activo']
