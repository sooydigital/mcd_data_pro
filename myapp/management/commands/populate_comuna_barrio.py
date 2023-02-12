from myapp.models import Comuna, Barrio
from django.core.management.base import BaseCommand

ALL_COMUNA = [
    ['1', 'Norte'],
    ['2', 'Nororiental'],
    ['3', 'San Francisco'],
    ['4', 'Occidental'],
    ['5', 'García Rovira'],
    ['6', 'La Concordia'],
    ['7', 'La Ciudadela'],
    ['8', 'Sur Occidente'],
    ['9', 'La Pedregosa'],
    ['10', 'Provenza'],
    ['11', 'Sur'],
    ['12', 'Cabecera '],
    ['13', 'Oriental'],
    ['14', 'Morrorico'],
    ['15', 'Centro'],
    ['16', 'Lagos del Cacique'],
    ['17', 'Mutis']
]

ALL_Barrio = {
    '1': [
            "El Rosal",
            "Colorados",
            "Café Madrid",
            "Las Hamacas",
            "Altos del Kennedy",
            "Kennedy",
            "Balcones del Kennedy",
            "Las Olas",
            "Villa Rosa (sectores I",
            "II y III)",
            "Omagá (sectores I y II)",
            "Minuto de Dios",
            "Tejar Norte (sectores I y II)",
            "Miramar",
            "Miradores del Kennedy",
            "El Pablón (Villa Lina",
            "La Torre",
            "Villa Patricia",
            "Sector Don Juan",
            "Pablón Alto y Bajo"
        ],
    '2': [
        "Los Angeles",
        "Villa Helena I y II",
        "José María Córdoba",
        "Esperanza I, II y III",
        "Lizcano I y II",
        "Regadero Norte",
        "San Cristóbal",
        "La Juventud",
        "Transición I, II, III, IV y V",
        "La Independencia",
        "Villa Mercedes",
        "Bosque Norte"
        ],
}
class Command(BaseCommand):
    def handle(self, *args, **options):
        for comuna in ALL_COMUNA:
            comuna_id = comuna[0]
            comuna_nombre = comuna[1]
            if not Comuna.objects.filter(id=comuna_id, nombre=comuna_nombre).exists():
                Comuna.objects.create(id=comuna_id, nombre=comuna_nombre)
        for comuna, barrios in ALL_Barrio.items():
            comuna_obj = Comuna.objects.get(id=comuna)
            for barrio in barrios:
                if comuna_obj and not Barrio.objects.filter(comuna=comuna_obj, nombre=barrio).exists():
                    Barrio.objects.create(comuna=comuna_obj, nombre=barrio)

