
from myapp.models import Votante, Municipio, Barrio
from myapp.serializers import BarrioSerializer


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
