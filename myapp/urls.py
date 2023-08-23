from django.urls import path, include

# importing views from views..py
from myapp.views import views, api_views
from django.views.generic import TemplateView
from django.urls import path

app_name = "app"
urlpatterns = [
    path('', views.home, name='home'),
    path('test', views.test, name='test'),
    path('summary', views.summary, name='summary'),
    path('insert_votante', views.insert_votante, name='insert_votante'),
    path('iv/<str:sub_link>', views.insert_votante_with_sub_link, name='insert_votante_sub_link'),
    path('iv_confirm', TemplateView.as_view(template_name='insert_votante_confirm.html'), name='insert_votante_confirm'),
    path('lista_puesto_votacion', views.lista_puesto_votacion, name='lista_puesto_votacion'),


    path('geomapa', views.geomapa, name='geomapa'),
    path('geomapa/detail/', views.geomapa_detail, name='geomapa_detail'),
    path('geomapa/detail/<str:puesto_id>', views.geomapa_detail, name='geomapa_detail_id'),
    path('geomapa/detail_by_leader/<str:leader_id>', views.geomapa_detail_by_leader, name='geomapa_detail_by_leader'),
    path('geomapa/detail_by_votante/<str:votante_cc>', views.geomapa_detail_by_votante, name='geomapa_detail_by_votante'),

    path('leaders', views.leaders, name='leaders'),
    path('votantes', views.list_votantes, name='show_votantes'),
    path('votante/editar/<str:document_id>', views.editar_votante, name='editar_votante'),
    path('votante/eliminar/<str:document_id>', views.eliminar_votante, name='eliminar_votante'),
    path('dinamizadores', views.list_dinamizadores, name='show_dinamizadores'),


    path('api/validate_cc/<str:document_id>', views.validate_cc, name='validate_cc'),
    path('api/get_barrio_by_municipio/<str:municipio_id>', views.get_barrio_by_municipio, name='get_barrio_by_municipio'),
    path('api/mapa_puestos/', views.get_mapa_puestos,
         name='mapa_puestos'),

    # integracion para programa de Registraduria y WebWhatsapp
    path('api/whatsapp-response/', api_views.whatsapp_response, name='whatsapp_response'),
    path('api/whatsapp-validate/', api_views.whatsapp_validate, name='whatsapp_validate'),
    path('api/whatsapp-add-user/', api_views.whatsapp_add_user, name='whatsapp_add_user'),

    path('api/insert-multi-votantes/', api_views.insert_multi_votantes, name='insert_multi_votantes'),
    path('api/update-multi-profile-votantes/', api_views.update_multi_profile_votantes, name='update_multi_profile_votantes'),
    path('api/get_all_cc_registered/', api_views.get_all_cc_registered, name='get_all_cc_registered'),
    path('api/get_all_cc_by_status/', api_views.get_all_cc_by_status, name='get_all_cc_by_status'),
    path('api/get_all_cc_by_municipio/', api_views.get_all_cc_by_municipio, name='get_all_cc_by_municipio'),
    path('api/insert_only_cc_votante/', api_views.insert_only_cc_votante, name='insert_only_cc_votante'),
    path('api/get_puesto_votation_by_cc/', api_views.get_puesto_votation_by_cc, name='get_puesto_votation_by_cc'),
    path('api/get_all_votantes/', views.get_votantes_api, name='get_votantes'),


    path(
        route='acciones_bloque/votantes/download',
        view=views.votantes_download,
        name='votantes_download'
    ),
]
