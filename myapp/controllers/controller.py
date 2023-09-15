from datetime import datetime, timedelta
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils import timezone, dateformat

from myapp.models import Etiqueta, Votante, VotanteProfile, VotantePuestoVotacion, VotanteMessage, EtiquetaVotante
from myapp.models import Municipio, Barrio, Departamento, PuestoVotacion
from myapp.models import CustomUser, CustomLink
from myapp.models import Campaign, Evento
import math

from myapp.serializers import BarrioSerializer

import re


def format_phone(str_phone, use_dash=True):
    """
    Format the phone int dash separated format
    :param str_phone: String, phone to be formatted. Ex: 123456789
    :return: String, formatted phone. Ex: 123-456-789
    """
    try:
        if not str_phone:
            return ""
        
        if len(str_phone) < 10:
            return str_phone

        formatted_number = (
            re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1-", "%s" % str_phone[:-1])
            + str_phone[-1]
        )

        numbers = formatted_number.split("-")
        return "{0}{1}{2}".format(numbers[0], numbers[1], numbers[2])

    except Exception as e:
        message = "Error while formatting phone: {}".format(e)
        raise Exception(message)
def format_number_with_spaces(number):
    # Convierte el número a una cadena
    number_str = str(number)

    # Utiliza una expresión regular para agregar espacios cada tres dígitos
    formatted_number = re.sub(r'\B(?=(\d{3})+(?!\d))', ' ', number_str)
    return formatted_number
def get_data_from_post(data_dict, name):
    data = ""
    if data_dict.get(name):
        data = data_dict.get(name)
        if type(data) == list:
            data = data[0]
    else:
        data = ""
    return data


def clena_data_cc(message):
    message = message.replace(" ", "").replace(".", "").replace(",", "")
    return message


class DataController():

    @staticmethod
    def save_votante_info(data):
        # TODO: revisar si necsito mensaje de error o validaciones...
        document_id = data.get('document_id')
        if not document_id:
            return None

        votante = Votante.objects.filter(document_id=document_id).first()
        vp = VotanteProfile.objects.filter(votante=votante).first()
        if not vp:
            first_name = data.get('first_name', "")
            mobile_phone = data.get('mobile_phone', "")
            municipio = data.get('municipio', "")
            gender = "OTRO" 

            vp = VotanteProfile()
            vp.votante = votante
            vp.first_name = first_name
            vp.mobile_phone = mobile_phone
            vp.municipio = municipio
            vp.gender = gender

            vp.save()


    @staticmethod
    def validate_votante_exist(document_id, create=False):
        votante_exist = Votante.objects.filter(document_id=document_id).exists()
        if not votante_exist and create:
            v = Votante()
            v.document_id = document_id
            v.status = "PENDING"
            v.save()

        return votante_exist
    
    
    @staticmethod
    def get_current_campaing():
        campaign = Campaign.objects.filter(is_active=True).first()
        return campaign

    @staticmethod
    def get_current_municipios():
        campaign = DataController.get_current_campaing()
        municipios = campaign.municipios.all()
        return municipios

    @staticmethod
    def validate_document_id(document_id):
        votante_validation = Votante.objects.filter(document_id=document_id).exists()
        return not votante_validation

    @staticmethod
    def get_or_create_votante_profile(votante):
        votante_profile_obj = None
        if VotanteProfile.objects.filter(votante=votante).exists():
            votante_profile_obj = VotanteProfile.objects.filter(votante=votante).first()
        else:
            votante_profile_obj = VotanteProfile(
                votante=votante
            )
            votante_profile_obj.save()
        return votante_profile_obj

    @staticmethod
    def get_or_create_puesto_votacion(departamento, municipio, name, address):
        departamento_obj = DataController.get_or_create_departamento(departamento)
        municipio_obj = DataController.get_or_create_municipio(departamento_obj, municipio)

        puesto_obj = None
        if PuestoVotacion.objects.filter(departamento=departamento_obj, municipio=municipio_obj, name=name).exists():
            puesto_obj = PuestoVotacion.objects.filter(departamento=departamento_obj, municipio=municipio_obj, name=name).first()
        else:
            puesto_obj = PuestoVotacion(
                departamento=departamento_obj,
                municipio=municipio_obj,
                name=name,
                address=address,
                longitude="",
                latitude="",
            )
            puesto_obj.save()
        return puesto_obj

    @staticmethod
    def get_barrios_by_municipio(municipio_id):
        municipio = Municipio.objects.filter(name=municipio_id).first()
        barrios_data = []
        if municipio:
            barrios = municipio.barrio_set.order_by("name").all()
            # barrios_data = BarrioSerializer(data=barrios, many=True)
            for barrio in barrios:
                barrios_data.append(
                    {
                        "id": barrio.id,
                        "name": barrio.name,
                    }
                )

        return barrios_data

    @staticmethod
    def get_or_create_departamento(departamento):
        departamento_obj = None
        if Departamento.objects.filter(name=departamento).exists():
            departamento_obj = Departamento.objects.filter(name=departamento).first()
        else:
            departamento_obj = Departamento(
                name=departamento,
            )
            departamento_obj.save()
        return departamento_obj

    @staticmethod
    def get_or_create_municipio(departamento, municipio):
        municipio_obj = None
        if Municipio.objects.filter(departamento=departamento, name=municipio).exists():
            municipio_obj = Municipio.objects.filter(departamento=departamento, name=municipio).first()
        else:
            municipio_obj = Municipio(
                departamento=departamento,
                name=municipio,
            )
            municipio_obj.save()
        return municipio_obj

    @staticmethod
    def get_or_create_barrio(municipio, barrio):
        barrio_obj = None
        if Barrio.objects.filter(municipio=municipio, name=barrio).exists():
            barrio_obj = Barrio.objects.filter(municipio=municipio, name=barrio).first()
        else:
            barrio_obj = Barrio(
                municipio=municipio,
                name=barrio,
            )
            barrio_obj.save()
        return barrio_obj

    @staticmethod
    def store_reponses(data, user, sub_link=None):
        votante_lider = None
        votante_custom = None
        votante_coordinador = None
        if sub_link:
            sub_link_obj = CustomLink.objects.filter(sub_link=sub_link).first()
            if sub_link_obj:
                votante_custom = sub_link_obj.votante

        document_id = clena_data_cc(get_data_from_post(data, "document_id"))

        if Votante.objects.filter(document_id=document_id).exists():
            return "Esta cedula ya existe"

        if votante_custom != None:
            etiqueta_votante = EtiquetaVotante.objects.filter(votante=votante_custom)
            etiqueta_id = etiqueta_votante.values()[0]['etiqueta_id']

            if etiqueta_id == 1:
                votante_lider = votante_custom

            elif etiqueta_id == 3:
                votante_coordinador = votante_custom

        status = "PENDING"
        custom_user = None
        votante = Votante(
            document_id=document_id,
            status=status,
        )



        if votante_lider:
            votante.lider = votante_lider
            custom_user = votante_lider.custom_user
            votante.custom_user = custom_user
            etiqueta = None
        elif votante_coordinador:
            votante.coordinador = votante_coordinador
            custom_user = votante_coordinador.custom_user
            votante.custom_user = custom_user
            etiqueta = "LIDER"
        else:
            custom_user = user.customuser_set.first()
            votante.custom_user = custom_user
            etiqueta = None


        votante.save()

        first_name = get_data_from_post(data, "first_name")
        last_name = get_data_from_post(data, "last_name")
        email = "null"
        mobile_phone = get_data_from_post(data, "mobile_phone")
        day = get_data_from_post(data, "day")
        month = get_data_from_post(data, "month")
        year = get_data_from_post(data, "year")
        birthday = str(year+'-'+month+'-'+day)
        gender = get_data_from_post(data, "gender")
        address = get_data_from_post(data, "address")
        municipio = get_data_from_post(data, "municipio")
        barrio = get_data_from_post(data, "barrio")
        departamento_obj = Departamento.objects.first()

        municipio_obj = DataController.get_or_create_municipio(departamento_obj, municipio)
        barrio_obj = DataController.get_or_create_barrio(municipio_obj, barrio)

        try:
            votante_profile = VotanteProfile(
                votante=votante,
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile_phone=mobile_phone,
                birthday=birthday,
                gender=gender,
                address=address,
                municipio=municipio_obj,
                barrio=barrio_obj,
            )

            votante_profile.save()
            mensaje = f"Felicidades se ha agregado a {first_name} {last_name} satisfactoriamente"

            print(etiqueta)
            if etiqueta == "COORDINADOR" or etiqueta == "LIDER":
                print('es aca')
                campain_url = DataController.get_current_campaing().url
                etiqueta_instance = Etiqueta.objects.filter(name=etiqueta).first()
                etiqueta_v = EtiquetaVotante(
                    votante = votante,
                    etiqueta = etiqueta_instance
                )
                etiqueta_v.save()

                link_v = CustomLink(
                    votante = votante,
                    sub_link = document_id,
                )
                link_v.save()
                mensaje = f"Felicidades {first_name} {last_name} se ha creado como {etiqueta} correctamente, su link es: {campain_url}/iv/{document_id}"
                
        except Exception as e:
            print(e)
            return "Woops hubo un error, por favor verifica que estés enviando información correcta"
        
        
        return {
            "mensaje": mensaje,
            "votante": votante,
            "votante_profile": votante_profile
        }

    @staticmethod
    def get_summary_by_user(customer_user_id):
        number_lideres = 0
        customer_user = CustomUser.objects.filter(user_id=customer_user_id).first()
        if customer_user:
            is_super_visor = not customer_user.super_visor_id
            if is_super_visor:
                alimentadores = customer_user.customuser_set.all()
                votantes = Votante.objects.filter(custom_user__in=alimentadores)
                number_lideres = len(CustomLink.objects.filter(votante__custom_user__in=alimentadores).all())

            else:
                votantes = Votante.objects.filter(custom_user=customer_user)
                number_lideres = len(CustomLink.objects.filter(votante__custom_user=customer_user).all())

        else:
            votantes = Votante.objects
            number_lideres = len(CustomLink.objects.all())

        today = datetime.today()
        return {
            "num_lideres": number_lideres,
            "votante_error": len(votantes.filter(status="ERROR").all()),
            "votante_pending_proceess": len(votantes.filter(status="PENDING").all()),
            "votante_proceess": len(votantes.filter(status="PROCESSED").all()),

            "num_encuestas_total": len(votantes.all()),
            # todo: agregar filtro por mes, semana, dia
            "num_encuestas_mes": len(votantes.filter(
                created_at__gte=(today - timedelta(days=today.day)),
                created_at__lte=today,
            ).all()),
            "num_encuestas_semana": len(votantes.filter(
                created_at__gte=(
                        today - timedelta(hours=today.hour, minutes=today.minute, seconds=today.second) - timedelta(
                    days=today.weekday())),
                created_at__lte=today + timedelta(days=1),
            ).all()),
            "num_encuestas_hoy": len(votantes.filter(
                created_at__gte=today.replace(hour=0, minute=0, second=0, microsecond=0),
                created_at__lte=today,
            ).all()),
        }
    

    @staticmethod
    def get_summary_api():
        votantes = Votante.objects.all()
        total_votantes = votantes.count()
        number_lideres = len(EtiquetaVotante.objects.filter(etiqueta=1).all())
        number_coordinadores = len(EtiquetaVotante.objects.filter(etiqueta=3).all())

        data = {}
        today = datetime.today()

        data["num_votantes"] = total_votantes
        data["num_lideres"] = number_lideres
        data["num_coordinadores"] = number_coordinadores

        data["votante_error"] = len(votantes.filter(status="ERROR").all())
        data["votante_pending_proceess"] = len(votantes.filter(status="PENDING").all())
        data["votante_proceess"] = len(votantes.filter(status="PROCESSED").all())

        # todo: agregar filtro por mes, semana, dia
        data["num_votantes_mes"] = len(votantes.filter(
            created_at__gte=(today - timedelta(days=today.day)),
            created_at__lte=today,
        ).all())
        data["num_votantes_semana"] = len(votantes.filter(
            created_at__gte=(
                    today - timedelta(hours=today.hour, minutes=today.minute, seconds=today.second) - timedelta(
                days=today.weekday())),
            created_at__lte=today + timedelta(days=1),
        ).all())
        
        data["num_votantes_hoy"] = len(votantes.filter(
            created_at__gte=(today.replace(hour=0, minute=0, second=0, microsecond=0) ),
            created_at__lte=today,
        ).all())
        data["num_votantes_ayer"] = len(votantes.filter(
            created_at__gte=(today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)),
            created_at__lte=today.replace(hour=0, minute=0, second=0, microsecond=0),
        ).all())
        data["num_votantes_dos_dias_atras"] = len(votantes.filter(
            created_at__gte=(today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=2)),
            created_at__lte=today.replace(hour=0, minute=0, second=0, microsecond=0),
        ).all())
        data["num_votantes_tre_dias_atras"] = len(votantes.filter(
            created_at__gte=(today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=3)),
            created_at__lte=today.replace(hour=0, minute=0, second=0, microsecond=0),
        ).all())
        data["num_votantes_tre_cuatro_atras"] = len(votantes.filter(
            created_at__gte=(today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=4)),
            created_at__lte=today.replace(hour=0, minute=0, second=0, microsecond=0),
        ).all())
        data["num_votantes_tre_cinco_atras"] = len(votantes.filter(
            created_at__gte=(today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=5)),
            created_at__lte=today.replace(hour=0, minute=0, second=0, microsecond=0),
        ).all())
        data["num_votantes_tre_seis_atras"] = len(votantes.filter(
            created_at__gte=(today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=6)),
            created_at__lte=today.replace(hour=0, minute=0, second=0, microsecond=0),
        ).all())


        return data

    @staticmethod
    def get_votantes_information_to_download():
        data = {}
        custom_users = CustomUser.objects.exclude(super_visor=None).all()

        custom_user_mapping = {
        }

        for custom_user in custom_users:
            custom_user_mapping[custom_user.id] = {
                "code": custom_user.code,
                "full_name": custom_user.full_name(),
                "super_visor": custom_user.super_visor_id
            }
        lider_custom_link_users = CustomLink.objects.all()
        lider_user_mapping = {
        }
        for lider_custom_link_user in lider_custom_link_users:
            lider_id = lider_custom_link_user.votante
            lider_user_mapping[lider_id.id] = {
                "lider_full_name": lider_id.full_name(),
                "lider_cutom_link": lider_custom_link_user.sub_link
            }

        data["custom_user_mapping"] = custom_user_mapping
        data["lider_user_mapping"] = lider_user_mapping
        custom_users_super_visor = CustomUser.objects.filter(super_visor=None).all()
        custom_user_super_visor_mapping = {
        }

        for custom_user in custom_users_super_visor:
            custom_user_super_visor_mapping[custom_user.id] = {
                "code": custom_user.code,
                "full_name": custom_user.full_name(),
            }
        data["custom_user_super_visor_mapping"] = custom_user_super_visor_mapping

        votantes = Votante.objects.all()
        votante_mapping = {
        }

        for votante in votantes:
            votante_mapping[votante.id] = {
                "document_id": votante.document_id,
                "status": votante.status,
                "custom_user": votante.custom_user_id,
                "lider_user": votante.lider_id
            }
        data["votante_mapping"] = votante_mapping

        votantes_profile = VotanteProfile.objects.all()
        votante_profile_mapping = {
        }

        for votante_profile in votantes_profile:
            barrio = ""
            if votante_profile.barrio:
                barrio = votante_profile.barrio.name

            municipio = ""
            departamento = ""
            if votante_profile.municipio:
                municipio = votante_profile.municipio.name
                if votante_profile.municipio.departamento:
                    departamento = votante_profile.municipio.departamento.name

            if votante_profile.municipio:
                departamento = votante_profile.municipio.name

            votante_profile_mapping[votante_profile.votante_id] = {
                "votante_id": votante_profile.votante_id,
                "first_name": votante_profile.first_name,
                "last_name": votante_profile.last_name,
                "email": votante_profile.email,
                "mobile_phone": votante_profile.mobile_phone,
                "birthday": votante_profile.birthday,
                "age": votante_profile.age(),
                "gender": votante_profile.gender,
                "address": votante_profile.address,
                "departamento": departamento,
                "municipio": municipio,
                "barrio": barrio,
            }

        data["votante_profile_mapping"] = votante_profile_mapping

        votantes_puesto_votacion = VotantePuestoVotacion.objects.all()
        votante_puesto_votacion_mapping = {
        }

        for votante_puesto_votacion in votantes_puesto_votacion:
            votante_puesto_votacion_mapping[votante_puesto_votacion.votante_id] = {
                "votante_id": votante_puesto_votacion.votante_id,
                "mesa": votante_puesto_votacion.mesa,
                "puesto_votacion_id": votante_puesto_votacion.puesto_votacion_id,
            }

        data["votante_puesto_votacion_mapping"] = votante_puesto_votacion_mapping


        puestos_votacion = PuestoVotacion.objects.all()
        puesto_votacion_mapping = {
        }

        for puesto_votacion in puestos_votacion:
            puesto_votacion_mapping[puesto_votacion.id] = {
                "departamento": puesto_votacion.departamento.name,
                "municipio": puesto_votacion.municipio.name,
                "name": puesto_votacion.name,
                "address": puesto_votacion.address,
            }

        data["puesto_votacion_mapping"] = puesto_votacion_mapping

        return data

    @staticmethod
    def get_puestos_votacion_to_plot(municipio):
        current_campaing = DataController.get_current_campaing()
        center = {"lat": current_campaing.latitude_principal, "lon": current_campaing.longitude_principal} # location

        data = {
            "ids": ["ID"],
            "lat": ["Lattitude"],
            "lon": ["Longitude"],
            "pv_text": [""],
            "pv_size": ["Size B"],
            "in_text": ["Votos"],
            "in_size": ["Size E"],
            "center": center
        }
        puesto_votaciones_query = PuestoVotacion.objects
        if not municipio == "ALL":
            puesto_votaciones_query = puesto_votaciones_query.filter(municipio__name=municipio)
            municipio_obj = Municipio.objects.filter(name=municipio).first()
            if municipio_obj and municipio_obj.longitude:
                data["center"] = {
                    "lat": municipio_obj.latitude,
                    "lon": municipio_obj.longitude
                }


        puesto_votaciones = puesto_votaciones_query.all()
        for puesto_votacion in puesto_votaciones:
            num_votantes = len(puesto_votacion.votantepuestovotacion_set.all())
            intensidad = "0"
            if num_votantes:
                log_10 = math.log2(num_votantes) * 2
                intensidad = str(10 + log_10)
            else:
                intensidad = "0"

            data["ids"].append(puesto_votacion.id)

            data["lat"].append(puesto_votacion.latitude)
            data["lon"].append(puesto_votacion.longitude)
            data["pv_text"].append(puesto_votacion.name)
            data["pv_size"].append("10")

            data["in_text"].append(str(num_votantes))
            data["in_size"].append(intensidad)



        return data

    @staticmethod
    def get_puestos_votacion_to_plot_by_leader(leader_id):

        current_campaing = DataController.get_current_campaing()
        center = {"lat": current_campaing.latitude_principal, "lon": current_campaing.longitude_principal} # location
        data = {
            "ids": ["ID"],
            "lat": ["Lattitude"],
            "lon": ["Longitude"],
            "pv_text": [""],
            "pv_size": ["Size B"],
            "in_text": ["Votos"],
            "in_size": ["Size E"],
            "center": center
        }
        puesto_votaciones_query = PuestoVotacion.objects
        puesto_votaciones_query = puesto_votaciones_query.filter(votantepuestovotacion__votante__lider_id=leader_id)

        puesto_votaciones = puesto_votaciones_query.all()
        for puesto_votacion in puesto_votaciones:
            num_votantes = len(puesto_votacion.votantepuestovotacion_set.all())
            intensidad = "0"
            if num_votantes:
                log_10 = math.log2(num_votantes) * 2
                intensidad = str(10 + log_10)
            else:
                intensidad = "0"

            data["ids"].append(puesto_votacion.id)

            data["lat"].append(puesto_votacion.latitude)
            data["lon"].append(puesto_votacion.longitude)
            data["pv_text"].append(puesto_votacion.name)
            data["pv_size"].append("10")

            data["in_text"].append(str(num_votantes))
            data["in_size"].append(intensidad)

        return data
    

    @staticmethod
    def get_puestos_votacion_to_plot_by_votante(votante_id, get_direccion_votante=False):
        current_campaing = DataController.get_current_campaing()
        center = {"lat": current_campaing.latitude_principal, "lon": current_campaing.longitude_principal} # location

        data = {
            "ids": ["ID"],
            "lat": ["Lattitude"],
            "lon": ["Longitude"],
            "pv_text": [""],
            "pv_size": ["Size B"],
            "in_text": ["Votos"],
            "in_size": ["Size E"],
            "center": center
        }
        if get_direccion_votante:
            data["direccion_votantes"] = {
                "ids": ["ID"],
                "lat": ["Lattitude"],
                "lon": ["Longitude"],
                "address": ["Dirección"],
            }
            votante_profile = VotanteProfile.objects.filter(votante_id=votante_id).first()
            if votante_profile:
                lat = votante_profile.latitude
                lon = votante_profile.longitude
                if lat and lon:
                    data["direccion_votantes"]["lat"].append(lat)
                    data["direccion_votantes"]["lon"].append(lon)
                    data["direccion_votantes"]["address"].append(votante_profile.address)


        puesto_votaciones_query = PuestoVotacion.objects
        puesto_votaciones_query = puesto_votaciones_query.filter(votantepuestovotacion__votante_id=votante_id)

        puesto_votaciones = puesto_votaciones_query.all()
        for puesto_votacion in puesto_votaciones:
            num_votantes = len(puesto_votacion.votantepuestovotacion_set.all())
            intensidad = "0"
            if num_votantes:
                log_10 = math.log2(num_votantes) * 2
                intensidad = str(10 + log_10)
            else:
                intensidad = "0"

            data["ids"].append(puesto_votacion.id)

            data["lat"].append(puesto_votacion.latitude)
            data["lon"].append(puesto_votacion.longitude)
            data["pv_text"].append(puesto_votacion.name)
            data["pv_size"].append("10")

            data["in_text"].append(str(num_votantes))
            data["in_size"].append(intensidad)

        return data
    

    @staticmethod
    def get_votantes_to_plot_by_barrio(request, barrio):
        current_campaing = DataController.get_current_campaing()
        center = {"lat": current_campaing.latitude_principal, "lon": current_campaing.longitude_principal} # location

        
        data = {
            "center": center,
            "pv_size": 12,
        }
        
        
        data["direccion_votantes"] = {
            "lat": ["Lattitude"],
            "lon": ["Longitude"],
            "address": ["Dirección"],
        }
        votantes = Votante.objects.all()
        for votante in votantes:
            votante_profile = votante.votanteprofile_set.first()
            if votante_profile:
                if str(votante_profile.barrio).upper().strip().replace(' ', '') == barrio:
                    lat = votante_profile.latitude
                    lon = votante_profile.longitude
                    if lat and lon:
                        data["direccion_votantes"]["lat"].append(lat)
                        data["direccion_votantes"]["lon"].append(lon)
                        data["direccion_votantes"]["address"].append(votante_profile.address)

                    

        return data
    

    @staticmethod
    def get_votante_info(document_id):
        votante = Votante.objects.filter(document_id=document_id).first()
        if not votante:
            return None
        if votante.status == "PROCESSED":
            votante_perfil = votante.votanteprofile_set.first()
            if not votante_perfil:
                return None

            votante_puesto = votante.votantepuestovotacion_set.first()
            if not votante_puesto:
                return None

            puesto = votante_puesto.puesto_votacion

            data = {
                "name": votante_perfil.full_name(),
                "departamento": votante_perfil.municipio.departamento.name,
                "municipio": votante_perfil.municipio.name,
                "puesto": puesto.name,
                "mesa": votante_puesto.mesa,
                "direccion": puesto.address,
            }

            return data

    @staticmethod
    def get_all_registered():
        votantes = Votante.objects.all()
        lista = [
            votante.document_id for votante in votantes
        ]
        return lista

    @staticmethod
    def get_all_cc_by_status(status):
        votantes = Votante.objects.filter(
            status=status
        ).all()

        lista = [
            votante.document_id for votante in votantes
        ]
        return lista

    @staticmethod
    def get_all_cc_by_municipio(municipio):
        votantes_puesto = VotantePuestoVotacion.objects.filter(
            puesto_votacion__municipio__name__iexact=municipio
        ).all()

        lista = [
            votante_puesto.votante.document_id for votante_puesto in votantes_puesto
        ]
        return lista

    @staticmethod
    def update_votantes_processsing(registro):

        document_id = registro.get("codigo")
        status = registro.get("status")
        message = registro.get("message")
        departamento = registro.get("departamento")
        municipio = registro.get("municipio")
        name = registro.get("puesto")
        address = registro.get("direccion")
        mesa = registro.get("mesa")

        new_status = "PROCESSED"
        if status == "ERROR":
            new_status = "ERROR"

        votante = Votante.objects.filter(document_id=document_id).first()
        if not votante:
            return None

        if votante.status == "PROCESSED":
            return None

        votante.status = new_status
        votante.save()

        if status == "ERROR":
            votante_message = VotanteMessage(
                votante=votante,
                message=message
            )
            votante_message.save()

        else:
            puesto_votacion = DataController.get_or_create_puesto_votacion(
                departamento=departamento,
                municipio=municipio,
                name=name,
                address=address,
            )
            votante_puesto_votacion = VotantePuestoVotacion(
                votante=votante,
                mesa=mesa,
                puesto_votacion=puesto_votacion
            )
            votante_puesto_votacion.save()

    @staticmethod
    def update_profile_votantes(registro):
        document_id = registro.get("codigo")
        first_name = registro.get("first_name")
        last_name = registro.get("last_name")
        email = registro.get("email")
        mobile_phone = registro.get("mobile_phone")
        birthday = registro.get("birthday")
        gender = registro.get("gender")
        address = registro.get("address")
        municipio = registro.get("municipio")
        barrio = registro.get("barrio")
        etiqueta = registro.get("etiqueta")
        lider_id = registro.get("lider")

        lider_instance = Votante.objects.filter(document_id = lider_id).first()


        votante = Votante.objects.filter(document_id=document_id).first()
        votante.lider = lider_instance
        if votante:
            votante_profile = DataController.get_or_create_votante_profile(votante)
            if first_name:
                votante_profile.first_name = first_name

            if last_name:
                votante_profile.last_name = last_name

            if email:
                votante_profile.email = email

            if mobile_phone:
                votante_profile.mobile_phone = mobile_phone

            if birthday:
                votante_profile.birthday = birthday

            if gender:
                votante_profile.gender = gender

            if address:
                votante_profile.address = address

            if municipio:
                departamento_name = "SANTANDER"
                departamento_obj = DataController.get_or_create_departamento(departamento_name)
                municipio_obj = DataController.get_or_create_municipio(departamento_obj, municipio)
                votante_profile.municipio = municipio_obj

                if barrio:
                    barrio = DataController.get_or_create_barrio(municipio_obj, barrio)
                    votante_profile.barrio = barrio

            votante.save()
            votante_profile.save()

            if etiqueta != None and etiqueta != "none":
                etiqueta_instance = Etiqueta.objects.filter(name=etiqueta).first()
                etiqueta_v = EtiquetaVotante(
                    votante = votante,
                    etiqueta = etiqueta_instance
                )
                    
                etiqueta_v.save()
                
            
            

    @staticmethod
    def insert_only_cc_votante(document_id):
        status = "PENDING"


        if not Votante.objects.filter(document_id=document_id).exists():
            votante = Votante(
                document_id=document_id,
                status=status,
            )

            votante.save()


    @staticmethod
    def get_puesto_votation_by_cc(document_id):
        data = {}
        votante = Votante.objects.filter(document_id=document_id).first()
        if votante:
            votante_puesto = VotantePuestoVotacion.objects.filter(votante=votante).first()
            if votante_puesto:
                puesto = votante_puesto.puesto_votacion
                if puesto:
                    data["document_id"] = votante.document_id
                    data["mesa"] = votante_puesto.mesa
                    data["departamento"] = puesto.departamento.name
                    data["municipio"] = puesto.municipio.name
                    data["direccion"] = puesto.address
                    data["puesto"] = puesto.name
                profile = VotanteProfile.objects.filter(votante=votante).first()
                if profile:
                    data["name"] = profile.full_name()
            else:
                votante_message = VotanteMessage.objects.filter(votante=votante).first()
                if votante_message:
                    data["message"] = votante_message.message

        return data

    @staticmethod
    def get_info_puesto_by_id(puesto_id):
        data = {
            "nombre": "",
            'intencion_voto': 0,
            'intencion_voto_percentage': 0
        }

        puesto = PuestoVotacion.objects.filter(id=puesto_id).first()
        intencion_voto = puesto.inteciondevoto_set.first()

        if puesto:
            num_puestos =  len(puesto.votantepuestovotacion_set.all())
            data["name"] = puesto.name
            data["departamento"] = puesto.departamento.name
            data["municipio"] = puesto.municipio.name
            data["address"] = puesto.address
            data["longitude"] = puesto.longitude
            data["latitude"] = puesto.latitude
            data["num_puestos"] = num_puestos

            if intencion_voto and num_puestos:
                data['intencion_voto'] = intencion_voto.intencion_de_voto
                if  num_puestos >= intencion_voto.intencion_de_voto:
                    data['intencion_voto_percentage'] = 100
                else:
                    data['intencion_voto_percentage'] = num_puestos*100/intencion_voto.intencion_de_voto


            votantes_puestovotacion = puesto.votantepuestovotacion_set.all()
            votantes = []
            for votante_puestovotacion in votantes_puestovotacion:
                votante = votante_puestovotacion.votante
                votante_profile = votante.votanteprofile_set.first()
                votante_data = {
                        "id": votante.id,
                        "document_id": votante.document_id,
                        "name": votante.full_name(),
                        "mesa": votante_puestovotacion.mesa,
                }
                has_customlink = votante.customlink_set.first()
                if has_customlink:
                    votante_data['is_leader'] = True
                    votante_data['custom_link'] = has_customlink.sub_link
                else:
                    votante_data['is_leader'] = False
                    votante_data['lider_id'] = votante.lider_id

                if votante_profile:
                    print('votante_profile.mobile_phone', votante_profile.mobile_phone)
                    votante_data['show_mobile_phone'] = votante_profile.mobile_phone if votante_profile.mobile_phone else ""
                    votante_data['mobile_phone'] = votante_profile.mobile_phone or ""
                    votante_data['age'] = votante_profile.age()

                votantes.append(
                    votante_data
                )

            data["votantes"] = votantes
        return data


    @staticmethod
    def get_leaders_by_coordinador(request, coordinador_id):
        data = {
            "coordinador_id": coordinador_id,
            "nombre": "",
        }
        coordinador = Votante.objects.filter(id=coordinador_id).first()
        votantes_list = []
        if coordinador:
            has_link = coordinador.customlink_set.first()
            if has_link:

                url = reverse("app:insert_votante_sub_link", args=[has_link.sub_link])
                full_url = request.build_absolute_uri(url)
                data["link"] = full_url

            referidos = list(Votante.objects.filter(coordinador_id=coordinador_id))
            referidos += list(Votante.objects.filter(lider_id=coordinador_id))

            for votante in referidos:
                votante_profile = votante.votanteprofile_set.first()
                votante_data = {
                    "id": votante.id,
                    "name": votante.full_name(),
                    "document_id": votante.document_id,
                    "mesa": "",
                    "puesto_nombre": "",
                    "puesto_municipio": "",
                    "status": votante.status,
                    "lideres_count": len(Votante.objects.filter(lider_id=votante.id))
                }

                has_customlink = votante.customlink_set.first()
                if has_customlink:
                    votante_data['is_coordinador'] = True
                    votante_data['custom_link'] = has_customlink.sub_link
                else:
                    votante_data['is_coordinador'] = False

                if votante_profile:
                    votante_data['show_mobile_phone'] = format_phone(
                        votante_profile.mobile_phone) if votante_profile.mobile_phone else ""
                    votante_data['mobile_phone'] = votante_profile.mobile_phone or ""
                    votante_data['age'] = votante_profile.age()

                votantes_list.append(
                    votante_data
                )
            votantes_list = sorted(votantes_list, key=lambda k: k['name'])
        data["votantes"] = votantes_list
        data["nombre"] = coordinador.full_name()
        lider_profile = coordinador.votanteprofile_set.first()
        if lider_profile:
            data["mobile_phone"] = lider_profile.mobile_phone or ""

        return data


    @staticmethod
    def get_info_puesto_by_leader(request, leader_id):
        data = {
            "leader_id": leader_id,
            "nombre": "",
            "link": "",
            'intencion_voto': 0,
            'intencion_voto_percentage': 0
        }
        lider = Votante.objects.filter(id=leader_id).first()
        votantes_list = []
        if lider:
            has_link = lider.customlink_set.first()
            if has_link:

                url = reverse("app:insert_votante_sub_link", args=[has_link.sub_link])
                full_url = request.build_absolute_uri(url)
                data["link"] = full_url

            votantes = Votante.objects.filter(lider_id=leader_id)
            for votante in votantes:
                votante_profile = votante.votanteprofile_set.first()
                votante_puestovotacion = votante.votantepuestovotacion_set.first()
                votante_data = {
                    "name": votante.full_name(),
                    "document_id": votante.document_id,
                    "mesa": "",
                    "puesto_nombre": "",
                    "puesto_municipio": "",
                    "status": votante.status
                }

                if votante_puestovotacion:
                    votante_data["mesa"] = votante_puestovotacion.mesa if votante_puestovotacion else ""
                    puesto = votante_puestovotacion.puesto_votacion
                    votante_data["puesto_id"] = puesto.id if puesto else ""
                    votante_data["puesto_nombre"] = puesto.name if puesto else ""
                    votante_data["puesto_municipio"] = puesto.municipio.name if puesto and puesto.municipio else ""

                has_customlink = votante.customlink_set.first()
                if has_customlink:
                    votante_data['is_leader'] = True
                    votante_data['custom_link'] = has_customlink.sub_link
                else:
                    votante_data['is_leader'] = False

                if votante_profile:
                    votante_data['show_mobile_phone'] = format_phone(
                        votante_profile.mobile_phone) if votante_profile.mobile_phone else ""
                    votante_data['mobile_phone'] = votante_profile.mobile_phone or ""
                    votante_data['age'] = votante_profile.age()

                votantes_list.append(
                    votante_data
                )
            votantes_list = sorted(votantes_list, key=lambda k: k['name'])
        data["votantes"] = votantes_list
        data["nombre"] = lider.full_name()
        lider_profile = lider.votanteprofile_set.first()
        if lider_profile:
            data["mobile_phone"] = lider_profile.mobile_phone or ""

        return data
    

    @staticmethod
    def get_info_puesto_by_votante(request, votante_cc):
        data = {
            "mapa_votante_id": 1,
            "has_lider": None,
            "nombre": "",
            "link": "",
            'intencion_voto': 0,
            'intencion_voto_percentage': 0,
            'puesto': "",
            'address': "",
            'address_puesto': "",
            'municipio': "",
            'departamento': "",
        }
        votante = Votante.objects.filter(document_id=votante_cc).first()
        votantes_list = []
        if votante:
            data["nombre"] = votante.full_name()
            data["mapa_votante_id"] = votante.id

            has_lider = votante.lider
            if has_lider:
                data['has_lider'] = has_lider
            votante_data = {}
            votante_profile = votante.votanteprofile_set.first()
            votante_puestovotacion = votante.votantepuestovotacion_set.first()
            if votante_puestovotacion:
                puesto = votante_puestovotacion.puesto_votacion
                if puesto:
                    votante_data = {
                            "name": votante.full_name(),
                            "mesa": votante_puestovotacion.mesa if votante_puestovotacion else "",
                            "puesto": "{} - {}".format(puesto.name, puesto.address),
                    }
                    data["puesto"] = puesto.name
                    data["address_puesto"] = puesto.address
                    data["departamento"] = puesto.municipio.departamento.name
                    data["municipio"] = puesto.municipio.name or "none"
                    data["puesto_id"] = puesto.id
            has_customlink = votante.customlink_set.first()
            if has_customlink:
                votante_data['is_leader'] = True
                votante_data['custom_link'] = has_customlink.sub_link
            else:
                votante_data['is_leader'] = False

            if votante_profile:
                votante_data['mobile_phone'] = votante_profile.mobile_phone or ""
                votante_data['email'] = votante_profile.email or ""
                votante_data['address'] = votante_profile.address or ""
                votante_data['gender'] = votante_profile.gender or ""
                votante_data['birthday'] = votante_profile.birthday or ""
                votante_data['age'] = votante_profile.age()
                votante_data['departamento'] = ""
                if votante_profile.municipio:
                    votante_data['departamento'] = votante_profile.municipio.departamento.name
                votante_data['municipio'] = ""
                if votante_profile.municipio:
                    votante_data['municipio'] = votante_profile.municipio.name
                votante_data['barrio'] = ""
                if votante_profile.barrio:
                    votante_data['barrio'] = votante_profile.barrio.name

            votantes_list.append(
                votante_data
            )
        data["votantes"] = votantes_list

        return data

    @staticmethod
    def get_all_leaders():
        etiquetas = EtiquetaVotante.objects.filter(etiqueta=1).all()
        votantes = []
        for etiqueta in etiquetas:
            votante = etiqueta.votante
            votante_profile = votante.votanteprofile_set.first()
            votante_data = {
                "id": votante.id,
                "name": votante.full_name(),
                "referrals": len(Votante.objects.filter(lider_id=votante.id)),
                "document_id": votante.document_id
            }
            has_customlink = votante.customlink_set.first()
            if has_customlink:
                votante_data['is_leader'] = True
                votante_data['custom_link'] = has_customlink.sub_link
            else:
                votante_data['is_leader'] = False

            if votante_profile:
                votante_data['show_mobile_phone'] = str(votante_profile.mobile_phone).replace(' ','') if votante_profile.mobile_phone else ""
                votante_data['mobile_phone'] = votante_profile.mobile_phone or ""
                votante_data['age'] = votante_profile.age()


            votantes.append(
                votante_data
            )

        votantes = sorted(votantes, key=lambda x: x["referrals"], reverse=True)

        return {
            "leaders": votantes
        }
    

    @staticmethod
    def get_all_coordinadores():
        etiquetas = EtiquetaVotante.objects.filter(etiqueta=3).all()
        votantes = []
        for etiqueta in etiquetas:
            votante = etiqueta.votante
            votante_profile = votante.votanteprofile_set.first()
            votante_data = {
                "id": votante.id,
                "name": votante.full_name(),
                "referrals": len(Votante.objects.filter(coordinador_id=votante.id)) + len(Votante.objects.filter(lider_id=votante.id)),
                "document_id": votante.document_id,
            }
            has_customlink = votante.customlink_set.first()
            if has_customlink:
                votante_data['is_coordinador'] = True
                votante_data['custom_link'] = has_customlink.sub_link
            else:
                votante_data['is_coordinador'] = False

            if votante_profile:
                votante_data['show_mobile_phone'] = str(votante_profile.mobile_phone).replace(' ','') if votante_profile.mobile_phone else ""
                votante_data['mobile_phone'] = votante_profile.mobile_phone or ""
                votante_data['age'] = votante_profile.age()


            votantes.append(
                votante_data
            )
        votantes = sorted(votantes, key=lambda x: x["referrals"], reverse=True)
        return {
            "coordinadores": votantes
        }


    @staticmethod
    def get_all_votantes_api():
        all_votantes = Votante.objects.all()
        votantes = []
        for votante in all_votantes:
            votante_profile = votante.votanteprofile_set.first()

            votante_data = {
                "id": votante.id,
                "name": votante.full_name().strip(),
                "document_id": votante.document_id,
            }
            has_customlink = votante.customlink_set.first()
            if has_customlink:
                votante_data['is_leader'] = True
                votante_data['custom_link'] = has_customlink.sub_link
            else:
                votante_data['is_leader'] = False
            
            if votante_profile:
                votante_data['municipio'] = str(votante_profile.municipio)
                votante_data['mobile_phone'] = votante_profile.mobile_phone if votante_profile.mobile_phone else ""
                votante_data['age'] = votante_profile.age()
                votante_data['barrio'] = str(votante_profile.barrio)
                #listar barrios

            votante_puestovotacion = votante.votantepuestovotacion_set.first()
            if votante_puestovotacion:
                puesto = votante_puestovotacion.puesto_votacion
                if puesto:
                    votante_data['municipio'] = str(puesto.municipio.name)

            votantes.append(
                votante_data
            )

        votantes = sorted(votantes, key=lambda x: x["name"])
        
        return votantes
    
    
    @staticmethod
    def get_barrio_votantes():
        all_votantes = Votante.objects.all()
        lista_barrios = []
        cantidad = []
        temp = []
        counted_barrios = []
        barrios_data = {}
        for votante in all_votantes:
            votante_profile = votante.votanteprofile_set.first()
            
            if votante_profile:
                lista_barrios.append(str(votante_profile.barrio).upper().strip())

        for barrio in lista_barrios:
            cantidad.append(lista_barrios.count(barrio))

        for barrio, cantidad in zip(lista_barrios, cantidad):
            if barrio == '' or barrio == '.':
                barrio == "default"
            else:
                barrios_data = {
                    'barrio': barrio,
                    'cantidad': cantidad,
                    'clean_barrio': barrio.replace(' ', ''),
                }
                if barrio not in temp:
                    temp.append(barrio)
                    counted_barrios.append(barrios_data)
        
        counted_barrios = sorted(counted_barrios, key=lambda k: k['barrio'])


        return {
            'barrios' : counted_barrios
        }
    

    @staticmethod
    def get_votantes_by_barrio(request, barrio):
        data = {}
        votantes = Votante.objects.all()
        votantes_list = []
        for votante in votantes:
            votante_profile = votante.votanteprofile_set.first()
            if votante_profile:
                if str(votante_profile.barrio).upper().strip() == barrio:
                    votante_data = {
                        "id": votante.id,
                        "name": votante.full_name().strip(),
                        "document_id": votante.document_id,
                    }

                    votante_data['show_mobile_phone'] = format_phone(
                        votante_profile.mobile_phone) if votante_profile.mobile_phone else ""
                    votante_data['mobile_phone'] = votante_profile.mobile_phone or ""
                    votante_data['barrio'] = votante_profile.barrio
                    votantes_list.append(
                        votante_data
                    )
                    votante_puestovotacion = votante.votantepuestovotacion_set.first()
                    if votante_puestovotacion:
                        puesto = votante_puestovotacion.puesto_votacion
                        if puesto:
                            votante_data['municipio'] = puesto.municipio.name

        votantes_list = sorted(votantes_list, key=lambda k: k['name'])

        data["votantes"] = votantes_list


        return data
    

    @staticmethod
    def get_puestos_information():
        puestos = PuestoVotacion.objects.order_by("name").all()
        lista_puestos = []
        for p in puestos:
            lista_puestos.append({
                "id": p.id,
                "name": p.name,
                "address": p.address,
                "municipio": p.municipio.name,
                "departamento": p.municipio.departamento.name,
                "num_votantes": len(p.votantepuestovotacion_set.all()),
            })
        return lista_puestos


    @staticmethod
    def get_votante_info_to_edit(document_id):
        votante = Votante.objects.filter(document_id=document_id).first()
        if not votante:
            return None
        
        etiqueta_votante = EtiquetaVotante.objects.filter(votante=votante).first()
        etiqueta = "Seleccione..."
        if etiqueta_votante:
            etiqueta = str(etiqueta_votante.etiqueta)

        Custom_Link = CustomLink.objects.filter(votante=votante).first()
        link = ''
        if Custom_Link:
            link = Custom_Link.sub_link

        
        
        votante_perfil = votante.votanteprofile_set.first()
        
        first_name = str(votante_perfil.first_name)
        last_name = str(votante_perfil.last_name)
        date = str(votante_perfil.birthday)
        day = {
                'value':1,
                'text':'Seleccione...',
            }
        month = {
            'value':1,
            'text':'Seleccione...',
        }
        year = {
            'value':2023,
            'text':'Seleccione...',
        }
        if date != 'None':
            date = date.split('-')
            day = {
                'value':date[2],
                'text':date[2],
            }
            month = {
                'value':date[1],
                'text':date[1],
            }
            year = {
                'value':date[0],
                'text':date[0],
            }


        data = {
            "document_id": votante.document_id,
            "leader": votante.lider,
            "first_name": first_name,
            "last_name": last_name,
            "mobile_phone": votante_perfil.mobile_phone,
            "day": day,
            "month": month,
            "year": year,
            "gender": votante_perfil.gender,
            "municipio": votante_perfil.municipio,
            "barrio": votante_perfil.barrio,
            "address": votante_perfil.address,
            "etiqueta": etiqueta,
            "link": link,
        }

        return data


    @staticmethod
    def update_profile_votantes_custom(data, document_id):
        first_name = get_data_from_post(data, "first_name")
        last_name = get_data_from_post(data, "last_name")
        email = "null"
        mobile_phone = get_data_from_post(data, "mobile_phone")
        day = get_data_from_post(data, "day")
        month = get_data_from_post(data, "month")
        year = get_data_from_post(data, "year")
        birthday = str(str(year).replace('.','')+'-'+month+'-'+day)
        gender = get_data_from_post(data, "gender")
        address = get_data_from_post(data, "address")
        municipio = get_data_from_post(data, "municipio")
        barrio = get_data_from_post(data, "barrio")
        etiqueta = get_data_from_post(data,"etiqueta")
        link = get_data_from_post(data,"link")
        lider = get_data_from_post(data,"lider")

        departamento_obj = Departamento.objects.first()

        municipio_obj = DataController.get_or_create_municipio(departamento_obj, municipio)
        barrio_obj = DataController.get_or_create_barrio(municipio_obj, barrio)


        votante = Votante.objects.filter(document_id=document_id).first()
        if votante:

            if lider:
                votante_instance = Votante.objects.filter(document_id=lider).first()
                votante.lider = votante_instance
            
            votante_profile = DataController.get_or_create_votante_profile(votante)
            if first_name:
                votante_profile.first_name = first_name

            if last_name:
                votante_profile.last_name = last_name

            if email:
                votante_profile.email = email

            if mobile_phone:
                votante_profile.mobile_phone = mobile_phone

            if birthday:
                votante_profile.birthday = birthday

            if gender:
                votante_profile.gender = gender

            if address:
                votante_profile.address = address
            
            if municipio:
                votante_profile.municipio = municipio_obj

            if barrio:
                barrio = DataController.get_or_create_barrio(municipio_obj, barrio)
                votante_profile.barrio = barrio_obj

            try:
                votante.save()
                votante_profile.save()
                campain_url = DataController.get_current_campaing().url
                mensaje = f"Felicidades {first_name} {last_name} se ha actualizado correctamente"

                if etiqueta == "LIDER" or etiqueta == "COORDINADOR":
                    etiqueta_instance = Etiqueta.objects.filter(name=etiqueta).first()
                    etiqueta_votante = EtiquetaVotante.objects.filter(votante = votante).first()
                    if etiqueta_votante:
                        etiqueta_votante.etiqueta = etiqueta_instance
                    else:
                        etiqueta_votante = EtiquetaVotante(
                            votante = votante,
                            etiqueta = etiqueta_instance
                        )

                    etiqueta_votante.save()

                    if link != None and link != "none":
                        c_link = CustomLink.objects.filter(votante = votante).first()

                        if c_link:
                            c_link.sub_link = link
                            mensaje = f"Felicidades el líder {first_name} {last_name} se ha actualizado correctamente, su link es: {campain_url}/iv/{link}"
                        else:
                            c_link = CustomLink(
                                votante = votante,
                                sub_link = link,
                            )
                            mensaje = f"Felicidades {first_name} {last_name} se ha convertido en {etiqueta} correctamente, su link es: {campain_url}/iv/{link}"

                        c_link.save()
                            
                return {"message":mensaje}
            except Exception as e:
                return f"Lo sentimos hubo un error al intentar actualizar a {first_name} {last_name}"

    
    @staticmethod
    def get_votante_to_delete(document_id):
        votante = Votante.objects.filter(document_id=document_id).first()
        try:
            votante.delete()
        except Exception as e:
            return "Upss! Ocurrio un error inesperado al intentar eliminar este votante"
        
        return {"message": f"La persona identificada con cc: {document_id} se ha eliminado correctamente"}
    

    @staticmethod
    def store_votante_as_leader(data):

        document_id = clena_data_cc(get_data_from_post(data, "document_id"))

        if Votante.objects.filter(document_id=document_id).exists():
            return "Esta cedula ya existe"

        status = "PENDING"
        votante = Votante(
            document_id=document_id,
            status=status,
        )

        votante.save()

        first_name = get_data_from_post(data, "first_name")
        last_name = get_data_from_post(data, "last_name")
        email = "null"
        mobile_phone = get_data_from_post(data, "mobile_phone")
        day = get_data_from_post(data, "day")
        month = get_data_from_post(data, "month")
        year = get_data_from_post(data, "year")
        birthday = str(year+'-'+month+'-'+day)
        gender = get_data_from_post(data, "gender")
        address = get_data_from_post(data, "address")
        municipio = get_data_from_post(data, "municipio")
        barrio = get_data_from_post(data, "barrio")
        departamento_obj = Departamento.objects.first()
        etiqueta = get_data_from_post(data,"etiqueta")
        if get_data_from_post(data,"link"):
            link = get_data_from_post(data,"link")
        else:
            link = document_id

        municipio_obj = DataController.get_or_create_municipio(departamento_obj, municipio)
        barrio_obj = DataController.get_or_create_barrio(municipio_obj, barrio)

        try:
            votante_profile = VotanteProfile(
                votante=votante,
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile_phone=mobile_phone,
                birthday=birthday,
                gender=gender,
                address=address,
                municipio=municipio_obj,
                barrio=barrio_obj,
            )
            votante_profile.save()
            campain_url = DataController.get_current_campaing().url
            if etiqueta != None and etiqueta != "none":
                etiqueta_instance = Etiqueta.objects.filter(name=etiqueta).first()
                etiqueta_v = EtiquetaVotante(
                    votante = votante,
                    etiqueta = etiqueta_instance
                )
                etiqueta_v.save()
                if link != None and link != "none":
                    link_v = CustomLink(
                        votante = votante,
                        sub_link = link,
                    )
                elif link == '':
                    link_v = CustomLink(
                        votante = votante,
                        sub_link = document_id,
                    )
                link_v.save()
                
                mensaje = f"Felicidades {first_name} {last_name} se ha creado como lider correctamente, su link es: {campain_url}/iv/{link}"
                            
            return {"message":mensaje}
        except Exception as e:
            return "Woops hubo un error, por favor verifica que estés enviando información correcta"
        

    @staticmethod
    def store_votante_as_coordinador(data):

        document_id = clena_data_cc(get_data_from_post(data, "document_id"))
        
        if Votante.objects.filter(document_id=document_id).exists():
            return "Esta cedula ya existe"

        status = "PENDING"
        votante = Votante(
            document_id=document_id,
            status=status,
        )

        votante.save()

        first_name = get_data_from_post(data, "first_name")
        last_name = get_data_from_post(data, "last_name")
        email = "null"
        mobile_phone = get_data_from_post(data, "mobile_phone")
        day = get_data_from_post(data, "day")
        month = get_data_from_post(data, "month")
        year = get_data_from_post(data, "year")
        birthday = str(year+'-'+month+'-'+day)
        gender = get_data_from_post(data, "gender")
        address = get_data_from_post(data, "address")
        municipio = get_data_from_post(data, "municipio")
        barrio = get_data_from_post(data, "barrio")
        departamento_obj = Departamento.objects.first()
        etiqueta = get_data_from_post(data,"etiqueta")
        if get_data_from_post(data,"link"):
            link = get_data_from_post(data,"link")
        else:
            link = document_id

        municipio_obj = DataController.get_or_create_municipio(departamento_obj, municipio)
        barrio_obj = DataController.get_or_create_barrio(municipio_obj, barrio)

        try:
            votante_profile = VotanteProfile(
                votante=votante,
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile_phone=mobile_phone,
                birthday=birthday,
                gender=gender,
                address=address,
                municipio=municipio_obj,
                barrio=barrio_obj,
            )
            votante_profile.save()
            campain_url = DataController.get_current_campaing().url
            if etiqueta != None and etiqueta != "none":
                etiqueta_instance = Etiqueta.objects.filter(name=etiqueta).first()
                etiqueta_v = EtiquetaVotante(
                    votante = votante,
                    etiqueta = etiqueta_instance
                )
                etiqueta_v.save()
                if link != None and link != "none":
                    link_v = CustomLink(
                        votante = votante,
                        sub_link = link,
                    )
                elif link == '':
                    link_v = CustomLink(
                        votante = votante,
                        sub_link = document_id,
                    )
                link_v.save()
                
                mensaje = f"Felicidades {first_name} {last_name} se ha creado como Coordinador correctamente, su link es: {campain_url}/iv/{link}"
                            
            return {"message":mensaje}
        
        except Exception as e:
            return "Woops hubo un error, por favor verifica que estés enviando información correcta"
        

    @staticmethod
    def store_event(data):
        document_id = clena_data_cc(get_data_from_post(data, "responsable"))

        votante_instance = Votante.objects.filter(document_id = document_id).first()
        name = get_data_from_post(data, "nombre")
        try:
            evento = Evento(
            name=name,
            responsable=votante_instance
            )
            evento.save()
            mensaje = f"El evento {name} se ha creado satisfactoriamente"

            return {"message":mensaje}
        
        except Exception as e:
            return "Ocurrio un error al intentar crear tu evento, por favor asegurate que estas introduciendo datos correctos."
        

    @staticmethod
    def list_events():
        events = Evento.objects.all()

        eventos = []
        for event in events:
            count_lideres = 0
            count_referidos = 0
            votante = event.responsable
            link = votante.customlink_set.first()
            event_data = {
                "id": votante.id,
                'event_name': event.name,
                "votante_name": votante.full_name().strip(),
                "document_id": votante.document_id,
                "custom_link": link.sub_link
            }
            lideres = Votante.objects.filter(coordinador_id=votante.id).all()

            for lider in lideres:
                count_lideres += 1
                count_referidos += len(Votante.objects.filter(lider_id=lider.id))

            event_data['lideres'] = count_lideres
            event_data['referidos'] = count_referidos

            eventos.append(event_data)
        
        return {'events': eventos}