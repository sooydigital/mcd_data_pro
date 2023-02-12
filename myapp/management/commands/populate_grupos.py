from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

ALL_GROUP = ['SUPER_ADMIN', 'ALIMENTADOR', 'SUPERVISOR']


class Command(BaseCommand):
    def handle(self, *args, **options):
        for group in ALL_GROUP:
            Group.objects.create(name=group)
