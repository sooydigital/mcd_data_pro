from datetime import datetime, timedelta

from myapp.models import Votante, VotanteProfile, VotantePuestoVotacion, VotanteMessage
from myapp.models import Municipio, Barrio, Departamento, PuestoVotacion
from myapp.models import CustomUser

from myapp.serializers import BarrioSerializer


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
                barrio=None,
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
    def store_reponses(data, user):
        document_id = clena_data_cc(get_data_from_post(data, "document_id"))
        if Votante.objects.filter(document_id=document_id).exists():
            return "Esta cedula ya existe"

        status = "PENDING"
        custom_user = user.customuser_set.first()
        votante = Votante(
            document_id=document_id,
            status=status,
            custom_user=custom_user
        )
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
        customer_user = CustomUser.objects.filter(user_id=customer_user_id).first()
        if customer_user:
            is_super_visor = not customer_user.super_visor_id
            if is_super_visor:
                alimentadores = customer_user.customuser_set.all()
                votantes = Votante.objects.filter(custom_user__in=alimentadores)
            else:
                votantes = Votante.objects.filter(custom_user=customer_user)
        else:
            votantes = Votante.objects

        today = datetime.today()
        return {
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
        data["custom_user_mapping"] = custom_user_mapping
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
                "custom_user": votante.custom_user_id
            }
        data["votante_mapping"] = votante_mapping

        votantes_profile = VotanteProfile.objects.all()
        votante_profile_mapping = {
        }

        for votante_profile in votantes_profile:
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
                "departamento": votante_profile.municipio.departamento.name,
                "municipio": votante_profile.municipio.name,
                "barrio": votante_profile.barrio.name,
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
                "barrio": puesto_votacion.barrio.name if puesto_votacion.barrio else "",
                "name": puesto_votacion.name,
                "address": puesto_votacion.address,
            }

        data["puesto_votacion_mapping"] = puesto_votacion_mapping

        print('data', data)
        return data

    @staticmethod
    def get_puestos_votacion_to_plot():
        data = {
            "lat": ["Lattitude"],
            "lon": ["Longitude"],
            "pv_text": [""],
            "pv_size": ["Size B"],
            "in_text": ["Votos"],
            "in_size": ["Size E"],
        }
        puesto_votaciones = PuestoVotacion.objects.all()
        for puesto_votacion in puesto_votaciones:
            num_votantes = len(puesto_votacion.votantepuestovotacion_set.all())
            intensidad = "0"
            if num_votantes:
                intensidad = str(10 + num_votantes)
            else:
                intensidad = "0"

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
