from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone, dateformat
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
    if not request.session.get('color_principal'):
        request.session['color_principal'] = DataController.get_current_campaing().color_principal
        request.session['color_secondary'] = DataController.get_current_campaing().color_secondary

    if not request.session.get('longitude_principal'):
        request.session['longitude_principal'] = DataController.get_current_campaing().longitude_principal
        request.session['latitude_principal'] = DataController.get_current_campaing().latitude_principal
    context = {}
    customer_user_id = request.user.id
    summary = DataController.get_summary_by_user(customer_user_id)

    context.update(summary)
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
    context = {
        'days': [d for d in range(1,32)],
        'months': [
            (1,'Enero'), 
            (2,'Febrero'), 
            (3,'Marzo'), 
            (4,'Abril'), 
            (5,'Mayo'), 
            (6,'Junio'), 
            (7,'Julio'), 
            (8,'Agosto'), 
            (9,'Septiembre'), 
            (10,'Octubre'), 
            (11,'Noviembre'), 
            (12,'Diciembre'),
        ],
        'years': [str(y).replace('.','') for y in range(1900,2006)]
    }
    campaing_name = DataController.get_current_campaing().name
    if campaing_name == 'cartagena_agosto':
        context['custom_name'] = 'Profe Doria'
    
    if request.method == 'POST':
        respuesta = DataController.store_reponses(dict(request.POST), request.user)
        if type(respuesta) == str:
            messages.error(request, respuesta)
        else:
            messages.success(request, 'El votante se ha registrado correctamente en V-Data.')
        return redirect('app:insert_votante')

    return render(
        request,
        'insert_votante.html',
        context
    )


# Create your views here.
@login_required
def lista_puesto_votacion(request):
    context = {}
    puestos = DataController.get_puestos_information()
    context["puestos"] = puestos
    return render(
        request,
        'list_puesto_votacion.html',
        context
    )

def insert_votante_with_sub_link(request, sub_link):
    if not request.session.get('color_principal'):
        request.session['color_principal'] = DataController.get_current_campaing().color_principal
        request.session['color_secondary'] = DataController.get_current_campaing().color_secondary
    context = {
        'days': [d for d in range(1,32)],
        'months': [
            (1,'Enero'), 
            (2,'Febrero'), 
            (3,'Marzo'), 
            (4,'Abril'), 
            (5,'Mayo'), 
            (6,'Junio'), 
            (7,'Julio'), 
            (8,'Agosto'), 
            (9,'Septiembre'), 
            (10,'Octubre'), 
            (11,'Noviembre'), 
            (12,'Diciembre'),
        ],
        'years': [str(y).replace('.','') for y in range(1900,2006)]
    }
    campaing_name = DataController.get_current_campaing().name
    if campaing_name == 'cartagena_agosto':
        context['custom_name'] = 'Profe Doria'
    if request.method == 'POST':
        respuesta = DataController.store_reponses(dict(request.POST), request.user, sub_link=sub_link)
        if type(respuesta) == str:
            messages.error(request, respuesta)
        else:
            messages.success(request, 'El votante se ha registrado correctamente en V-Data.')
        return redirect('./'+sub_link)


    return render(
        request,
        'insert_votante.html',
        context
    )

# Create your views here.
@login_required
def geomapa(request):
    context = {}
    municpios = DataController.get_current_municipios()
    context["municpios"] = municpios
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
    )

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
def geomapa_detail_by_votante(request, votante_cc):
    context = {}
    info_puesto = DataController.get_info_puesto_by_votante(request, votante_cc)
    context.update(info_puesto)
    context['v_id'] = votante_cc
    return render(
        request,
        'geomapa_detail_by_votante.html',
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
def list_votantes(request):
    context = {}
    votantes = DataController.get_all_votantes()
    context.update(votantes)
    return render(
        request,
        'show_votantes.html',
        context
    )

@login_required
def list_barrios(request):
    context = {}
    data = DataController.get_barrio_votantes()
    context.update(data)
    return render(
        request,
        'show_barrios.html',
        context
    )

def votantes_by_barrio(request, barrio):
    context = {
        'barrio':barrio,
        'clean_barrio': barrio.replace(' ','')
    }
    data = DataController.get_votantes_by_barrio(request, barrio)
    context.update(data)
    return render(
        request,
        'show_votantes_by_barrio.html',
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
    get_direccion_votante = request.GET.get('direccion_votante', False)
    data = []
    if municipio:
        data = DataController.get_puestos_votacion_to_plot(municipio)
    leader = request.GET.get('leader')
    if leader:
        data = DataController.get_puestos_votacion_to_plot_by_leader(leader)

    votante = request.GET.get('votante')
    if votante:
        data = DataController.get_puestos_votacion_to_plot_by_votante(votante, get_direccion_votante)


    response = {
        "data": data
    }
    return JsonResponse(response)


@login_required
def get_barrio_votantes(request, barrio):
    if barrio:
        data = DataController.get_votantes_to_plot_by_barrio(request, barrio)


    response = {
        "data": data
    }
    return JsonResponse(response)


@login_required
def editar_votante(request, document_id):
    if not request.session.get('color_principal'):
        request.session['color_principal'] = DataController.get_current_campaing().color_principal
        request.session['color_secondary'] = DataController.get_current_campaing().color_secondary
    context = {
        'days': [d for d in range(1,32)],
        'months': [
            (1,'Enero'), 
            (2,'Febrero'), 
            (3,'Marzo'), 
            (4,'Abril'), 
            (5,'Mayo'), 
            (6,'Junio'), 
            (7,'Julio'), 
            (8,'Agosto'), 
            (9,'Septiembre'), 
            (10,'Octubre'), 
            (11,'Noviembre'), 
            (12,'Diciembre'),
        ],
        'years': [str(y).replace('.','') for y in range(1900,2006)]
    }
    votante_data = DataController.get_votante_info_to_edit(document_id)
    context.update(votante_data)
    if request.method == 'POST':
        respuesta = DataController.update_profile_votantes_custom(dict(request.POST), document_id)
        if type(respuesta) == str:
            messages.error(request, respuesta)
        else:
            messages.success(request, respuesta["message"])
        return redirect('app:show_votantes')
    return render(request, 'perfil_edit.html', context)


@login_required
def eliminar_votante(request, document_id):
    respuesta = DataController.get_votante_to_delete(document_id)
    if type(respuesta) == str:
        messages.error(request, respuesta)
    else:
        messages.success(request, respuesta["message"])
    return redirect('app:show_votantes')
        