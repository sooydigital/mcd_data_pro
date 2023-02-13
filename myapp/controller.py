
from myapp.models import Votante

class Controller():

    @staticmethod
    def validate_document_id(document_id):
        votante_validation = Votante.objects.filter(document_id=document_id).exists()
        return votante_validation

