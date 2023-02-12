from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = [
            {
                'username': "yurs.ksf1@gmail.com",
                'first_name': "Yurley",
                'last_name': "Sanchez",
                'password': "admin",
                'role': "SUPER_ADMIN",
            },
            {
                'username': "miclickdigital@gmail.com",
                'first_name': "Mac",
                'last_name': "Herrera",
                'password': "admin",
                'role': "SUPER_ADMIN",
            },
            {
                'username': "supervisorb01@mail.com",
                'first_name': "Óscar",
                'last_name': "Miranda",
                'password': "admin",
                'municipio': "bucaramanga",
                'code': 'B01',
                'role': "SUPERVISOR",
            },
            {
                'username': "supervisorb02@mail.com",
                'first_name': "Ruth",
                'last_name': "Gualdrón",
                'password': "admin",
                'municipio': "bucaramanga",
                'code': 'B02',
                'role': "SUPERVISOR",
            },
            {
                'username': "supervisorb03@mail.com",
                'first_name': "Carlos",
                'last_name': "Niño",
                'password': "admin",
                'municipio': "bucaramanga",
                'code': 'B03',
                'role': "SUPERVISOR",
            },
            {
                'username': "supervisorb03@mail.com",
                'first_name': "Carlos",
                'last_name': "Ortiz",
                'password': "admin",
                'municipio': "bucaramanga",
                'code': 'B04',
                'role': "SUPERVISOR",
            },
            {
                'username': "supervisorf01@mail.com",
                'first_name': "Claudia",
                'last_name': "Hernández",
                'password': "admin",
                'municipio': "floridablanca",
                'code': 'F01',
                'role': "SUPERVISOR",
            },
            {
                'username': "supervisorp01@mail.com",
                'first_name': "Claudia",
                'last_name': "Reatiga",
                'password': "admin",
                'municipio': "piedecuesta",
                'code': 'P01',
                'role': "SUPERVISOR",
            },
            {
                'username': "supervisorg01@mail.com",
                'first_name': "Jovany",
                'last_name': "Riaño",
                'password': "admin",
                'municipio': "giron",
                'code': 'G01',
                'role': "SUPERVISOR",
            },
            {
                'username': "alimentadorG01_001@mail.com",
                'first_name': "Oscar",
                'last_name': "Reyez",
                'password': "admin",
                'code': 'G01_001',
                'role': "ALIMENTADOR"
            },
            {
                'username': "alimentadorG01_002@mail.com",
                'first_name': "Simona",
                'last_name': "Ramirez",
                'password': "admin",
                'code': 'G01_001',
                'role': "ALIMENTADOR"
            },
            {
                'username': "alimentadorG02_001@mail.com",
                'first_name': "Simona",
                'last_name': "Ramirez",
                'password': "admin",
                'code': 'G02_001',
                'role': "ALIMENTADOR"
            },
        ]

        for user in users:
            role = user.get('role')
            grupo = Group.objects.get(name=role)

            if not User.objects.filter(email=user['username']).exists():
                print(">>> User with username: '{}' created".format(user['username']))
                user_object = User(username=user['username'], email=user['username'], first_name=user['first_name'],
                                   last_name=user['last_name'])
                user_object.set_password(user['password'])
                user_object.save()
                user_object.groups.add(grupo)
                user_object.is_staff = True
                user_object.save()

        if not User.objects.filter(email='admin@mail.com').exists():
            user_object = User(username='admin', email='admin@mail.com', first_name='admin', last_name="super")
            user_object.set_password('admin')
            user_object.is_superuser = True
            user_object.is_staff = True

            user_object.save()

            print(">>> User with username: '{}' created".format('admin'))