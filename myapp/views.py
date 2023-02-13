from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myapp.download_controller import DownloadController
from myapp.controller import Controller
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
def summary(request):
    context = {}

    return render(
        request,
        'summary.html',
        context
    )


# Create your views here.
@login_required
def insert_votante(request):
    context = {}

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
def votantes_download(request):
    response = DownloadController.document_download()
    return response


@login_required
def validate_cc(request, document_id):
    document_validation = Controller.validate_document_id(document_id)

    response = {
        "data": document_validation
    }
    return JsonResponse(response)
