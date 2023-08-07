from datetime import datetime, timedelta
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from myapp.models import Votante, VotanteProfile, VotantePuestoVotacion, VotanteMessage
from myapp.models import Municipio, Barrio, Departamento, PuestoVotacion
from myapp.models import CustomUser, CustomLink
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
        if sub_link:
            sub_link_obj = CustomLink.objects.filter(sub_link=sub_link).first()
            if sub_link_obj:
                votante_lider = sub_link_obj.votante

        document_id = clena_data_cc(get_data_from_post(data, "document_id"))
        if Votante.objects.filter(document_id=document_id).exists():
            return "Esta cedula ya existe"

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
        else:
            custom_user = user.customuser_set.first()
            votante.custom_user = custom_user


        votante.save()

        first_name = get_data_from_post(data, "first_name")
        last_name = get_data_from_post(data, "last_name")
        email = get_data_from_post(data, "email")
        mobile_phone = get_data_from_post(data, "mobile_phone")
        birthday = get_data_from_post(data, "birthday")
        gender = get_data_from_post(data, "gender")
        address = get_data_from_post(data, "address")
        municipio = get_data_from_post(data, "municipio")
        barrio = get_data_from_post(data, "barrio")
        departamento_obj = Departamento.objects.first()

        municipio_obj = DataController.get_or_create_municipio(departamento_obj, municipio)
        barrio_obj = DataController.get_or_create_barrio(municipio_obj, barrio)

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

        return {
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

        print('data', data)
        return data

    @staticmethod
    def get_puestos_votacion_to_plot(municipio):
        data = {
            "ids": ["ID"],
            "lat": ["Lattitude"],
            "lon": ["Longitude"],
            "pv_text": [""],
            "pv_size": ["Size B"],
            "in_text": ["Votos"],
            "in_size": ["Size E"],
            "center": {"lat": 5.5368954, "lon": -73.3680772} # Tunja
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
        data = {
            "ids": ["ID"],
            "lat": ["Lattitude"],
            "lon": ["Longitude"],
            "pv_text": [""],
            "pv_size": ["Size B"],
            "in_text": ["Votos"],
            "in_size": ["Size E"],
            "center": {"lat": 5.5368954, "lon": -73.3680772} # Tunja
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
    def get_puestos_votacion_to_plot_by_votante(votante_id):
        data = {
            "ids": ["ID"],
            "lat": ["Lattitude"],
            "lon": ["Longitude"],
            "pv_text": [""],
            "pv_size": ["Size B"],
            "in_text": ["Votos"],
            "in_size": ["Size E"],
            "center": {"lat": 5.5368954, "lon": -73.3680772} # Tunja
        }
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

        votante = Votante.objects.filter(document_id=document_id).first()
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

            votante_profile.save()

    @staticmethod
    def insert_only_cc_votante(document_id):
        status = "PENDING"

        if not Votante.objects.filter(document_id=document_id).exists():
            votante = Votante(
                document_id=document_id,
                status=status
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

                    votante_data['show_mobile_phone'] = format_phone(
                        votante_profile.mobile_phone) if votante_profile.mobile_phone else ""
                    votante_data['mobile_phone'] = votante_profile.mobile_phone or ""
                    votante_data['age'] = votante_profile.age()

                votantes.append(
                    votante_data
                )

            data["votantes"] = votantes
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

            votantes = lider.votante_set.all()
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
            'puesto': ""
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
                    puesto_direccion = "{} - {}".format(puesto.name, puesto.address)
                    votante_data = {
                            "name": votante.full_name(),
                            "mesa": votante_puestovotacion.mesa if votante_puestovotacion else "",
                            "puesto": "{} - {}".format(puesto.name, puesto.address),
                    }
                    data["puesto"] = puesto_direccion
                    data["puesto_id"] = puesto.id
            has_customlink = votante.customlink_set.first()
            if has_customlink:
                votante_data['is_leader'] = True
                votante_data['custom_link'] = has_customlink.sub_link
            else:
                votante_data['is_leader'] = False

            if votante_profile:
                votante_data['mobile_phone'] = votante_profile.mobile_phone or ""
                votante_data['age'] = votante_profile.age()

            votantes_list.append(
                votante_data
            )
        data["votantes"] = votantes_list

        return data

    @staticmethod
    def get_all_leaders():
        custom_links = CustomLink.objects.all()
        votantes = []
        for custom_link in custom_links:
            votante = custom_link.votante
            votante_profile = votante.votanteprofile_set.first()

            votante_data = {
                "id": votante.id,
                "name": votante.full_name(),
                "referrals": len(votante.votante_set.all()),
                "document_id": votante.document_id
            }
            has_customlink = votante.customlink_set.first()
            if has_customlink:
                votante_data['is_leader'] = True
                votante_data['custom_link'] = has_customlink.sub_link
            else:
                votante_data['is_leader'] = False

            if votante_profile:
                votante_data['show_mobile_phone'] = format_phone(votante_profile.mobile_phone) if votante_profile.mobile_phone else ""
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