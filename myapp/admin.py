# admin.py

from django.contrib import admin
from myapp.models import Departamento, Municipio, Barrio, Comuna
from myapp.models import Votante, VotanteProfile, VotantePuestoVotacion, VotanteMessage
from myapp.models import PuestoVotacion, CustomUser, IntecionDeVoto
from myapp.models import CustomLink, EtiquetaVotante, Etiqueta
from myapp.models import Campaign
from datetime import date, timedelta

# filters
class RangeDayListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'rago de dias'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'range days'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('adulto_joven', 'Joven'),
            ('adulto', 'Adulto'),
            ('adulto_mayor', 'Adulto Mayor'),

        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        today = date.today()

        if self.value() == 'adulto_joven':
            date_delta_1 = today - timedelta(days=36*365)
            date_delta_2 = today - timedelta(days=18*365)
            return queryset.filter(
                birthday__gte=date_delta_1,
                birthday__lte=date_delta_2,
            )

        if self.value() == 'adulto':
            date_delta_1 = today - timedelta(days=55*365)
            date_delta_2 = today - timedelta(days=36*365)
            return queryset.filter(
                birthday__gte=date_delta_1,
                birthday__lte=date_delta_2,
            )

        if self.value() == 'adulto_mayor':
            date_delta = today - timedelta(days=55*365)
            return queryset.filter(
                birthday__lte=date_delta,
            )


# locations
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'departamento')
    list_filter = ('departamento',)
    search_fields = ('name',)


class ComunaAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'name', 'municipio')
    list_filter = ('municipio',)
    search_fields = ('number', 'name',)

class BarrioAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'municipio')
    list_filter = ('municipio',)
    search_fields = ('name',)

class IntecionDeVotoInline(admin.StackedInline):
    model = IntecionDeVoto
    extra = 0

# Puesto Votacion y User
class PuestoVotacionAdmin(admin.ModelAdmin):
    list_display = ('departamento', 'municipio', 'name', 'address', 'latitude', 'longitude')
    search_fields = ('name', 'address')
    list_filter = ('departamento', 'municipio')
    inlines = [IntecionDeVotoInline,]

class IntecionDeVotoAdmin(admin.ModelAdmin):
    list_display = ('puesto_votacion', 'intencion_de_voto')
    search_fields = ('puesto_votacion__name', 'puesto_votacion__municipio__name')
    list_filter = ('intencion_de_voto', 'puesto_votacion__municipio__name',)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('document_id',  'full_name', 'user', 'code', 'municipio', 'super_visor')
    search_fields = ('document_id', 'code', 'user__first_name', 'user__last_name')
    list_filter = ('municipio', 'super_visor',)

    def full_name(self, obj):
        return obj.full_name()


class EtiquetaVotanteInline(admin.StackedInline):
    model = EtiquetaVotante
    extra = 0


class VotanteAdmin(admin.ModelAdmin):
    list_display = ('document_id', 'full_name', 'status', 'custom_user')
    search_fields = ('document_id', )
    list_filter = ('status', 'custom_user')
    inlines = [EtiquetaVotanteInline,]

    def full_name(self, obj):
        return obj.full_name()

class VotanteProfileAdmin(admin.ModelAdmin):
    list_display = ('votante', 'first_name', 'last_name', 'email', 'mobile_phone', 'age', 'birthday', 'gender', 'address', 'barrio', 'municipio', 'latitude', 'longitude' )
    search_fields = ('votante__document_id', 'first_name', 'last_name')
    list_filter = (RangeDayListFilter, 'gender', 'municipio')


    def age(self, obj):
        return obj.age()

class VotantePuestoVotacionAdmin(admin.ModelAdmin):
    list_display = ('votante', 'full_name', 'mesa', 'puesto_votacion')
    search_fields = ('votante__document_id', 'mesa')
    list_filter = ('puesto_votacion__departamento', 'puesto_votacion__municipio')

    def full_name(self, obj):
        return obj.votante.full_name()

class VotanteMessageAdmin(admin.ModelAdmin):
    list_display = ('votante', 'message', )
    search_fields = ('votante__document_id','message')




# locations
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Barrio, BarrioAdmin)
admin.site.register(Comuna, ComunaAdmin)

# Puesto Votacion y User
admin.site.register(PuestoVotacion, PuestoVotacionAdmin)
admin.site.register(IntecionDeVoto, IntecionDeVotoAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

# votante info
admin.site.register(Votante, VotanteAdmin)
admin.site.register(VotanteProfile, VotanteProfileAdmin)
admin.site.register(VotantePuestoVotacion, VotantePuestoVotacionAdmin)
admin.site.register(VotanteMessage, VotanteMessageAdmin)

# etiquetas
admin.site.register(Etiqueta)
admin.site.register(EtiquetaVotante)
admin.site.register(CustomLink)

# campaing
admin.site.register(Campaign)