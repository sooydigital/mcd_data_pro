import json
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes

from myapp.models import Votante
from myapp.controllers.controller import DataController


def clean_cc_data(message):
    message = message.replace(" ", "").replace(".", "").replace(",", "")
    return message


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def whatsapp_response(request):
    if request.method == 'POST':

        body = request.body
        data = json.loads(body)

        current_message = data.get('query').get('message')
        # here is the magic
        message = clean_cc_data(current_message)

        vontante_info = DataController.get_votante_info(message)
        context = {}
        if vontante_info:
            document_id = vontante_info.get("document_id")
            name = vontante_info.get("name")
            departamento = vontante_info.get("departamento")
            municipio = vontante_info.get("municipio")
            puesto = vontante_info.get("puesto")
            puesto_url = vontante_info.get("url")
            mesa = vontante_info.get("mesa")
            direccion = vontante_info.get("direccion")

            base_message = "*{name}* \nDocumento: *{document_id}* \n\n*Puesto de Votación* 🗳️ \n\nDepartamento: \n*{departamento}* \nMunicipio: \n*{municipio}* \nPuesto: \n*{puesto}* \nMesa: *{mesa}* \nDirección: *{direccion}*  \n\n¿Cómo llegar? 🗺️📍\nDa click en el enlace.👇🏻 \n\n{puesto_url}".format(
                document_id=document_id,
                name=name.lstrip().rstrip(),
                departamento=departamento,
                municipio=municipio,
                puesto=puesto,
                puesto_url=puesto_url,
                mesa=mesa,
                direccion=direccion
            )
            context = {
                "replies": [
                    {
                        "message": base_message,
                    }
                ]
            }
        else:
            context = {
                "replies": [
                    {
                        "message": '"*{message}*" Estamos consultando tu puesto de votación'.format(
                            message=current_message
                        ),

                    }
                ]
            }

        return JsonResponse(context)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def whatsapp_validate(request):
    if request.method == 'POST':
        body = request.body
        data = json.loads(body)

        current_message = data.get('query').get('message')
        create = data.get('query').get('create', True)
        # here is the magic
        message = clean_cc_data(current_message)

        vontante_info = DataController.validate_votante_exist(message, create)

        context = {
            "message": str(vontante_info)
        }

        return JsonResponse(context)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def whatsapp_add_user(request):
    if request.method == 'POST':

        body = request.body
        data = json.loads(body)

        document_id = data.get('query').get('document_id')
        first_name = data.get('query').get('first_name', "")
        last_name = data.get('query').get('last_name', "")
        gender = data.get('query').get('gender', "")
        mobile_phone = data.get('query').get('mobile_phone', "")
        if len(mobile_phone) > 10:
            mobile_phone = mobile_phone[-10:]

        # here is the magic
        document_id = clean_cc_data(document_id)
        data = dict(
            document_id=document_id,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            mobile_phone=mobile_phone
        )

        DataController.save_votante_info(data)
        context = {"message": "listo, ya lo guarde"}

        return JsonResponse(context)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_all_cc_registered(request):
    if request.method == 'GET':
        vontante_lista = DataController.get_all_registered()

        response = {
            "data": vontante_lista
        }
        return JsonResponse(response)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_all_cc_by_status(request):
    if request.method == 'GET':
        status = request.query_params.get('status')
        vontante_lista = DataController.get_all_cc_by_status(status)

        response = {
            "data": vontante_lista
        }
        return JsonResponse(response)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_all_cc_by_municipio(request):
    if request.method == 'GET':
        municipio = request.query_params.get('municipio')
        vontante_lista = DataController.get_all_cc_by_municipio(municipio)

        response = {
            "data": vontante_lista
        }
        return JsonResponse(response)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def insert_multi_votantes(request):
    if request.method == 'POST':
        body = request.body
        data = json.loads(body)
        registros = data.get('registros')
        for registro in registros:
            DataController.update_votantes_processsing(registro)

        response = {"message": "done!"}
        return JsonResponse(response)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def update_multi_profile_votantes(request):
    if request.method == 'POST':
        body = request.body
        data = json.loads(body)
        registros = data.get('registros')
        for registro in registros:
            DataController.update_profile_votantes(registro)

        response = {"message": "done!"}
        return JsonResponse(response)
    #

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def insert_only_cc_votante(request):
    if request.method == 'POST':
        body = request.body
        data = json.loads(body)
        registro = data.get('registro')
        DataController.insert_only_cc_votante(registro)

        response = {"message": "done!"}
        return JsonResponse(response)\

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_puesto_votation_by_cc(request):
    if request.method == 'POST':
        body = request.body
        data = json.loads(body)
        registros = data.get('registros')
        data_response = []
        for registro in registros:
            result = DataController.get_puesto_votation_by_cc(registro)
            data_response.append(result)

        response = {
            "message": "done!",
            "data": data_response
        }
        return JsonResponse(response)
