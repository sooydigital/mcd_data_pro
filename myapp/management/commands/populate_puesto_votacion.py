from myapp.models import PuestoVotacion, Municipio, Departamento
from django.core.management.base import BaseCommand

PUESTOS = [
    ["COLEGIO MARIO MORALES DELGADO ", " VIA ZAPATOCA", "7.0305353", "-73.1650761"],
    ["COLEGIO SAN JUAN DE GIRON SEDE B ", " CRA 28 No 30-49 PARQUE PERALTA", "7.0678848", "-73.1734138"],
    ["COLEGIO VILLAS DE SAN JUAN ", " CALLE 10 B # 25-31 VILLAS DE SN JUAN", "7.0558548", "-73.1682062"],
    ["COLEGIO PORTAL CAMPESTRE NORTE ", " BULEVAR LA CEIBA NO 22A-15 PORTAL CAM", "7.0631597", "-73.1699424"],
    ["COL.SAN JUAN DE GIRON ", " CR 25 NO 31-08 CENTRO", "7.0681608", "-73.1711059"],
    ["SENA PALENQUE ", " KM 7 VIA PALENQUE", "7.0810032", "-73.1692327"],
    ["COLEGIO NUESTRA SEÑORA DE BELEN ", " CLL 13 C # 14-48 PUERTO MADERO", "7.0575429", "-73.1617198"],
    ["COLEGIO GABRIEL GARCIA MARQUEZ ", " TRANSV 20 # 10-20", "7.0575.677", "-73.1838494"],
    ["COL. LUIS CARLOS GALAN SEDE E ", " CRA. 19 # 13 A-19 RIO PRADO", "7.0566304", "-73.168843"],
    ["COLISEO CUBIERTO CIUDADELA VILLAMIL ", " DIAGONAL 16 PEATONAL #17 H-16 VILLAMIL", "7.0615131", "-73.167706"],
    ["COL.LUIS CARLOS GALAN/SEDE A ", " CLL 13A No 19A-50 RIO PRADO", "7.057573", "-73.1685286"],
    ["COL FACUNDO NAVAS SEDE D ", " DG 54A NO 23-25 SAN ANTONIO CARRIZAL", "7.0812966", "-73.1764833"],
    ["COLEGIO FACUNDO NAVAS MANTILLA ", " CARRERA 16F # 58A-57 LA ESMERALDA", "7.0847805", "-73.1715455"],
    ["COL.ROBERTO GARCIA PEÑA/SEDE A ", " CRA 15#36-01 RINCON DE GIRON", "7.0667512", "-73.1695452"],
    ["COL.LUIS CARLOS GALAN/SEDE B ", " CR.19 NO 13C-03 CONSUELO", "7.0572491", "-73.1739406"],
    ["COL JUAN CRISTOBAL MARTINEZ ", " CR 27 NO 18-27 SANTA CRUZ", "7.0610999", "-73.1733695"],
    ["COL.NIÑO JESUS DE PRAGA ", " CLL.32 NO 25-44 CENTRO", "7.0689224", "-73.1719384"],
    ["COL.SERRANO MUÑOZ/ SEDE B ", " CLL 36 NO 37-27 BELLAVISTA", "7.0764316", "-73.1837691"],
    ["COL SERRANO MUÑOZ SEDE C ", " CRA. 35 #45-25 PARAISO", "7.0759967", "-73.1877868"],
    ["COL.NIEVES CORTES PICON/SEDE A ", " CLL 49 NO 26-44 POBLADO", "7.0721388", "-73.1689447"],
    ["COLEGIO FRANCISCO SERRANO MUÑOZ SEDE A ", " CLL.31 NO 25-30 CENTRO", "7.068169", "-73.1714099"],
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        departamento_name = 'SANTANDER'
        municipio_name = 'GIRON'

        departamento_object = None
        municipio_object = None

        if not Departamento.objects.filter(name=departamento_name).exists():
            departamento_object = Departamento(name=departamento_name)
            departamento_object.save()

        else:
            departamento_object = Departamento.objects.filter(name=departamento_name).first()

        if not Municipio.objects.filter(name=municipio_name, departamento__name=departamento_name).exists():
            print(">>> Municipio with label: '{}' created".format(municipio_name))
            municipio_object = Municipio(name=municipio_name, departamento=departamento_object)
            municipio_object.save()
        else:
            municipio_object = Municipio.objects.filter(name=municipio_name).first()

        for puesto in PUESTOS:
            clean_puesto = puesto[0].strip()
            address = puesto[1].strip()
            latitude = puesto[2]
            longitude = puesto[3]
            if not PuestoVotacion.objects.filter(name=clean_puesto).exists():
                PuestoVotacion.objects.create(
                    name=clean_puesto,
                    address=address,
                    longitude=longitude,
                    latitude=latitude,
                    departamento=departamento_object,
                    municipio=municipio_object
                )
