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
            name = vontante_info.get("name")
            departamento = vontante_info.get("departamento")
            municipio = vontante_info.get("municipio")
            puesto = vontante_info.get("puesto")
            mesa = vontante_info.get("mesa")
            direccion = vontante_info.get("direccion")

            base_message = "*{name}* \n\n*LUGAR DE VOTACIÓN* 🗳️ \nDepartamento: \n*{departamento}* \nMunicipio: \n*{municipio}* \nPuesto: \n*{puesto}* \nMesa: \n*{mesa}* \nDirección: \n*{direccion}*<#>*Mi Click Digital* 🚀<#>Para consultar otra cédula escribe *0*".format(
                name=name.lstrip().rstrip(),
                departamento=departamento,
                municipio=municipio,
                puesto=puesto,
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
                        "message": '"*{message}*" no se encuentra en base de datos 💾🔍<#>Escribe otro número de cédula. \n*Ej: 1095933743* - _sin espacios ni puntos._'.format(
                            message=current_message
                        ),

                    }
                ]
            }

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


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def insert_multi_votantes(request):
    pass
    # if request.method == 'POST':
    #
    #     body = request.body
    #     data = json.loads(body)
    #     registro_obj = Registro.objects.first()
    #     registros = data.get('registros')
    #     for registro in registros:
    #         codigo = clean_data(registro.get('codigo'))
    #         nombre = registro.get('nombre')
    #         departamento = registro.get('departamento')
    #         municipio = registro.get('municipio')
    #         puesto = clean_data(registro.get('puesto'))
    #         mesa = clean_data(registro.get('mesa'))
    #         direccion = registro.get('direccion')
    #         is_valid = True
    #         if 'is_valid' in registro:
    #             is_valid = clean_data(registro.get('is_valid')) == 'True'
    #
    #         votante_obj = Votante.objects.filter(codigo=codigo).first()
    #         if not votante_obj:
    #             votante_obj = Votante.objects.create(
    #                 registro=registro_obj,
    #                 nombre=nombre,
    #                 codigo=codigo,
    #                 departamento=departamento,
    #                 municipio=municipio,
    #                 puesto=puesto,
    #                 mesa=mesa,
    #                 direccion=direccion,
    #                 is_valid=is_valid,
    #                 is_runned=True
    #             )
    #     response = {"message": "done!"}
    #     return JsonResponse(response)
    #
