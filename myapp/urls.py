from django.urls import path, include

# importing views from views..py
from myapp.views import views, api_views
from django.views.generic import TemplateView
from django.urls import path

app_name = "app"
urlpatterns = [
    path('', views.home, name='home'),
    path('summary', views.summary, name='summary'),
    path('insert_votante', views.insert_votante, name='insert_votante'),
    path('geomapa', views.geomapa, name='geomapa'),

    path('api/validate_cc/<str:document_id>', views.validate_cc, name='validate_cc'),
    path('api/get_barrio_by_municipio/<str:municipio_id>', views.get_barrio_by_municipio, name='get_barrio_by_municipio'),
    path('api/mapa_puestos/', views.get_mapa_puestos,
         name='mapa_puestos'),

    # integracion para programa de Registraduria y WebWhatsapp
    path('api/whatsapp-response/', api_views.whatsapp_response, name='whatsapp_response'),

    path('api/insert-multi-votantes/', api_views.insert_multi_votantes, name='insert_multi_votantes'),
    path('api/get_all_cc_registered/', api_views.get_all_cc_registered, name='get_all_cc_registered'),
    path('api/get_all_cc_by_status/', api_views.get_all_cc_by_status, name='get_all_cc_by_status'),

    path(
        route='acciones_bloque/votantes/download',
        view=views.votantes_download,
        name='votantes_download'
    ),
]
