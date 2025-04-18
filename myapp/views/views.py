from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from myapp.controllers.download_controller import DownloadController
from myapp.controllers.controller import DataController
from django.http import JsonResponse


# Create your views here.

def has_role(user, names):
    role_names = names.split(',')
    if hasattr(user, 'groups'):
        if user.groups.filter(name__in=role_names).exists():
            return True
    return False


# Create your views here.
@login_required
def home(request):
    context = {}

    return render(
        request,
        'home.html',
        context
    )

# Create your views here.
@login_required
def test(request):
    from myapp.models import VotantePuestoVotacion, PuestoVotacion

    if request.method == "POST":
        lat_lon = request.POST.get('lat_lon')
        data = lat_lon.split(',')
        lat = data[0]
        lon = data[1]
        puesto_id = request.POST.get('puesto_id')
        puesto = PuestoVotacion.objects.filter(id=puesto_id).first()
        if puesto:
            puesto.longitude = lon
            puesto.latitude = lat
            puesto.save()

        pass

    puesto_votacion = PuestoVotacion.objects.filter(municipio__name__in=(["GIRON", "BUCARAMANGA", "FLORIDABLANCA"])).order_by('municipio').all()
    votante_no_profile = []
    for puesto in puesto_votacion:
        if not puesto.longitude:
            votante_no_profile.append(puesto)
    context = {
        "puesto_votacion": votante_no_profile
    }


    return render(
        request,
        'test.html',
        context
    )


# Create your views here.
@login_required
def summary(request):
    context = {}
    customer_user_id = request.user.id
    summary = DataController.get_summary_by_user(customer_user_id)

    context.update(summary)
    return render(
        request,
        'summary.html',
        context
    )


# Create your views here.
@login_required
def insert_votante(request):
    context = {}
    if request.method == 'POST':
        respuesta = DataController.store_reponses(dict(request.POST), request.user)
        if type(respuesta) == str:
            messages.error(request, respuesta)
        else:
            messages.success(request, 'el registro se a guardado exitosamente')
        return redirect('app:home')


    return render(
        request,
        'insert_votante.html',
        context
    )

def insert_votante_with_sub_link(request, sub_link):
    context = {}
    if request.method == 'POST':
        respuesta = DataController.store_reponses(dict(request.POST), request.user, sub_link=sub_link)
        if type(respuesta) == str:
            messages.error(request, respuesta)
        else:
            messages.success(request, 'el registro se a guardado exitosamente')
        return redirect('app:insert_votante_confirm')


    return render(
        request,
        'insert_votante.html',
        context
    )

# Create your views here.
@login_required
def geomapa(request):
    context = {}

    return render(
        request,
        'geomapa.html',
        context
    )

@login_required
def geomapa_detail(request, puesto_id=None):
    context = {}
    info_puesto = DataController.get_info_puesto_by_id(puesto_id)
    context.update(info_puesto)
    return render(
        request,
        'geomapa_detail.html',
        context
    )\

@login_required
def geomapa_detail_by_leader(request, leader_id):
    context = {}
    info_puesto = DataController.get_info_puesto_by_leader(request, leader_id)
    context.update(info_puesto)
    return render(
        request,
        'geomapa_detail_by_leader.html',
        context
    )

@login_required
def leaders(request):
    context = {}
    info_puesto = DataController.get_all_leaders()
    context.update(info_puesto)
    return render(
        request,
        'leaders.html',
        context
    )


@login_required
def votantes_download(request):
    response = DownloadController.document_download()
    return response


# @login_required
def validate_cc(request, document_id):
    document_validation = DataController.validate_document_id(document_id)

    response = {
        "data": document_validation
    }
    return JsonResponse(response)

# @login_required
def get_barrio_by_municipio(request, municipio_id):
    barrios = DataController.get_barrios_by_municipio(municipio_id)

    response = {
        "data": barrios
    }
    return JsonResponse(response)

@login_required
def get_mapa_puestos(request):
    municipio = request.GET.get('municipio')
    data = []
    if municipio:
        data = DataController.get_puestos_votacion_to_plot(municipio)
    leader = request.GET.get('leader')
    if leader:
        data = DataController.get_puestos_votacion_to_plot_by_leader(leader)


    response = {
        "data": data
    }
    return JsonResponse(response)
