
from myapp.models import Votante, VotanteProfile,  Municipio, Barrio, Departamento
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
        return votante_validation

    @staticmethod
    def get_barrios_by_municipio(municipio_id):
        municipio = Municipio.objects.filter(id=municipio_id).first()
        barrios = municipio.barrio_set.all()
        barrios_data = BarrioSerializer(barrios).data
        return barrios_data

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