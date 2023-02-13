# admin.py

from django.contrib import admin
from myapp.models import Departamento, Municipio, Barrio
from myapp.models import Votante, VotanteProfile, VotantePuestoVotacion, VotanteMessage
from myapp.models import PuestoVotacion, CustomUser

# locations
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

# Puesto Votacion y User
class PuestoVotacionAdmin(admin.ModelAdmin):
    list_display = ('departamento', 'municipio', 'barrio', 'name', 'address', 'longitude', 'latitude')
    search_fields = ('name', 'address')
    list_filter = ('municipio', 'barrio')


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('document_id',  'user', 'code', 'municipio', 'super_visor')
    search_fields = ('document_id', 'code')
    list_filter = ('municipio', 'super_visor',)


class VotanteAdmin(admin.ModelAdmin):
    list_display = ('document_id', 'status', 'custom_user')
    search_fields = ('document_id', )
    list_filter = ('status', 'custom_user')


class VotanteProfileAdmin(admin.ModelAdmin):
    list_display = ('votante', 'first_name', 'last_name', 'email', 'mobile_phone', 'birthday', 'gender', 'address', 'barrio', 'municipio' )
    search_fields = ('votante__document_id', 'first_name', 'last_name')
    list_filter = ('gender', 'birthday', 'municipio')

class VotantePuestoVotacionAdmin(admin.ModelAdmin):
    list_display = ('votante', 'mesa', 'puesto_votacion')
    search_fields = ('votante__document_id',)

class VotanteMessageAdmin(admin.ModelAdmin):
    list_display = ('votante', 'message', )
    search_fields = ('votante__document_id',)




# locations
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Barrio, BarrioAdmin)

# Puesto Votacion y User
admin.site.register(PuestoVotacion, PuestoVotacionAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

# votante info
admin.site.register(Votante, VotanteAdmin)
admin.site.register(VotanteProfile, VotanteProfileAdmin)
admin.site.register(VotantePuestoVotacion, VotantePuestoVotacionAdmin)
admin.site.register(VotanteMessage, VotanteMessageAdmin)
