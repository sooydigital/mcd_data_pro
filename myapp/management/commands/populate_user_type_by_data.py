from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from myapp.models import Votante

def get_amigos(lideres_id):
    hijos = Votante.objects.filter(lider__in=(lideres_id)).all()
    if len(hijos) == 0:
        return len(lideres_id)
    hijos_ids = [h.id for h in hijos]
    return get_amigos(hijos_ids)

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = Votante.objects.all()

        for user in users:
            user_id = user.id
            # contar hijos
            hijos = Votante.objects.filter(lider=user_id).all()
            hijos_ids = [h.id for h in hijos]
            user.num_referidos = len(hijos_ids)
            if len(hijos_ids) >= 5:
                amigos = get_amigos(hijos_ids)
                if amigos - len(hijos) >= 25:
                    user.type="DINAMIZADOR"
                else:
                    user.type="LIDER"
                user.num_referidos = amigos
            else:
                user.type="VOTANTE"

            user.save()