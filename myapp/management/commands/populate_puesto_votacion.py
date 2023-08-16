from myapp.models import PuestoVotacion, Municipio, Departamento
from django.core.management.base import BaseCommand

PUESTOS = [
    ["COL BALBINO GARCIA SEDE A","CLL 8 NO 9-50 CENTRO","6.9877778","-73.051205"],
    ["INST LUIS CARLOS GALAN SEDE D","CRA 4 No. 17-20","6.9916137","-73.0541874"],
    ["LUIS CARLOS GALAN SEDE B","CRA 1W # 24D-40","6.9705743","-73.0503406"],
    ["ESC NORMAL SUPERIOR","CLL 5 NO 15-60 SAN CRISTOBAL","6.9926687","-73.0464727"],
    ["COL CABELLANO","CLL 7 No 16-20","6.9907495","-73.0438264"],
    ["COL CAVIREY","CR 19  NO  2-30 SAN FRANCISCO","6.9948921","-73.0439523"],
    ["COL CEDECO","CRA 8 No 9-25 CENTRO","6.9866551","-73.0490011"],
    ["INST LUIS CARLOS GALAN SEDE A","DG 14 NO 11-72 NUEVA CANDELARIA","6.9916552","-73.0542795"],
    ["ESC BALBINO GARCIA SEDE C - MA","CR 13 NO 10-50 SAN ANTONIO","6.9870887","-73.0454673"],
    ["COLEGIO LUIS CARLOS GALAN SEDE C","CIUDADELA BARRO BLANCO","6.9723205","-73.0598482"],
    ["COL HUMBERTO GOMEZ NIGRINIS","CLL 6 NO 13-42 SAN RAFAEL","6.990424","-73.0466254"],
    ["ESCENARIO DEPORTIVO MARIE POUSSEPIN","CARRERA 6A No 5 49 BARRIO HOYO CHIQUITO","6.9916712","-73.0596122"],
    ["ESC BALBINO GARCIA SEDE B","CR 4 NO 10-38 LA FERIA","6.9877932","-73.048926"],
    ["COLEGIO CARLOS VICENTE REY SEDE D","CRA 10 No 1 A - 35 LA CASTELLANA 2","7.0007823","-73.0516343"],
    ["COLEGIO CEDECO SEDE B","CALLE 10 # 10 05","6.9840212","-73.0484659"],
    ["COL VICTOR FELIX GOMEZ SEDE A","CR 3A No 1B-16 CAMPO VERDE","6.9914952","-73.0563765"],
    ["COL PROMOCION SOCIAL","CRA 2W No 6N-50 KM 2 VIA GUATIGUARA","6.9963612","-73.0648031"],
    ["COL VICTOR FELIX GOMEZ SEDE B","CRA 4 No 2AN-46 EL REFUGIO","6.9961486","-73.0588778"],
    ["CAIF CAMINO A BELEN","CALLE 6N No 4 - 40 JUNIN","6.9981895","-73.0586879"],
    ["CENTRO TABACALERO","CLL 11 NO 2-39 LA FERIA","6.9836801","-73.053702"],
    ["INST TEC CRECER Y CONSTRUIR","CLL 2A NO 3-07 EL TRAPICHE","6.989968","-73.0560916"],
    ["CTRO INTEGRACIÓN COMUNITARIA - LA DIVA","KM 7 VIA GUATIGUARA","6.9912432","-73.0364588"],
    ["RESTAURANTE ESCOLAR TABACALERO","CALLE 11 No 2  39","6.9825405","-73.0545772"],
    ["SALON COMUNAL BARILOCHE","DIAGONAL 3N # 2 51","7.1445256","-73.1354704"],
    ["BUENOS AIRES","ESC RUR BUENOS AIRES MESA DE RUITOQUE","7.0086943","-73.1023322"],
    ["CUROS","ESC RUR CUROS","6.9334008","-73.0167211"],
    ["CRISTALES","ESC RUR CRISTALES","6.991647","-73.0541693"],
    ["GRANADILLO","ESC RUR  EL GRANADILLO","6.3725855","-74.8930573"],
    ["LA ESPERANZA","ESC RUR LA ESPERANZA MESA DE LOS SANTOS","7.0051716","-73.0282219"],
    ["LA COLINA","ESC RUR LA COLINA MESA DE RUITOQUE","7.0149363","-73.0953775"],
    ["SAN FRANCISCO","ESC RUR SAN FRANCISCO","6.9972373","-73.0468118"],
    ["SAN ISIDRO","ESC RUR SAN ISIDRO","7.0033394","-72.9477459"],
    ["MESITAS DE SAN JAVIER","ESC RUR MESITAS DE SAN JAVIER","6.9231175","-73.0675215"],
    ["MANZANARES","ESC MADRE CARIDAD  KM 17  VIA  PIEDECUESTA","7.022404","-73.0621393"],
    ["MIRAFLORES","ESC RUR MIRAFLORES","6.9731333","-72.9957461"],
    ["MENZULI ALTO Y MENZULI BAJO","ESC RUR  MENZULY CHIQUITO ENTRADA FRENTE SEMINARIO","7.0389229","-73.0470552"],
    ["PESCADERO","ESC RUR PESCADERO","6.8263107","-73.0032385"],
    ["PLANADAS","ESC RUR PLANADAS","7.5774534","-73.1734442"],
    ["SEVILLA","ESC RUR SEVILLA","6.9887172","-73.0345099"],
    ["SANTA RITA","ESC RUR SANTA RITA KM 43 VIA PAMPLONA","7.1087798","-72.9884252"],
    ["UMPALA","ESC RUR UMPALA","6.8417926","-72.9783412"],
    ["LA VEGA","ESC RUR LA VEGA","6.9980776","-73.0630198"],
    
    
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        departamento_name = 'SANTANDER'
        municipio_name = 'PIEDECUESTA'

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
