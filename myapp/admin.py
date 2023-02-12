# admin.py

from django.contrib import admin
from myapp.models import Departamento, Municipio, Barrio

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'departamento')
    list_filter = ('departamento',)
    search_fields = ('name',)


class BarrioAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'municipio')
    list_filter = ('municipio',)
    search_fields = ('name',)


admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Barrio, BarrioAdmin)