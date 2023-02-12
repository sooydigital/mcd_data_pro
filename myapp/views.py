from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myapp.download_controller import DownloadController
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
def formulario(request):
    context = {}

    return render(
        request,
        'dashboard.html',
        context
    )

@login_required
def votantes_download(request):
    response = DownloadController.document_download()
    return response
