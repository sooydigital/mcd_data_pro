from django.urls import path, include

# importing views from views..py
from myapp import views
from django.views.generic import TemplateView
from django.urls import path

app_name = "app"
urlpatterns = [
    path('', views.home, name='home'),
    path('formulario', views.formulario, name='formulario'),
    # path('api/dates_records', views.get_date_records, name='get_date_records'),
    # path('api/barrio_by_date/<str:date>', views.get_barrios_by_date, name='barrios_date'),
    # path('api/colaboradores_by_date_and_barrio/<str:date>/<int:barrio>', views.colaboradores_by_date_and_barrio, name='colaboradores_by_date_and_barrio'),
    # path('api/registro', views.registro, name='registro'),
    # path('api/whatsapp-response/', views.whatsapp_response, name='whatsapp_response'),
    # path('api/insert-registros/', views.insert_registros, name='insert_registros'),
    # path('api/insert-multi-registros/', views.insert_multi_registros, name='insert_multi_registros'),
    # path('api/insert-votante/', views.insert_votante, name='insert_votante'),
    # path('api/insert-multi-votantes/', views.insert_multi_votantes, name='insert_multi_votantes'),
    # path('api/get_all_cc_registered/', views.get_all_cc_registered, name='get_all_cc_registered'),
    # path('api/', include(router.urls)),
    # path('test/', TemplateView.as_view(template_name="modal_form.html")),
    path(
        route='acciones_bloque/votantes/download',
        view=views.votantes_download,
        name='votantes_download'
    ),
]
