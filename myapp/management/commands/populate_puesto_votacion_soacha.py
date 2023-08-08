from myapp.models import PuestoVotacion, Municipio, Departamento
from django.core.management.base import BaseCommand

PUESTOS = [
    ["I. E. SANTA ANA - ANTONIO NARIÑO", "CR. 11 D No. 17 A - 44 SUR SANTA ANA", "4.5694487", "-74.2369882"],
    ["I.E. COMPARTIR", "TR. 17 No. 5 B - 10 SUR COMPARTIR", "4.5711535", "-74.2397182"],
    ["I.E. CIUDAD LATINA", "CLL. 37 A SUR No. 15 i - 21", "4.5765466 ", "-74.2477584"],
    ["IE. NUEVO COMPARTIR", "CRA 14 No 29 - 80 SUR COMPARTIR", "4.570828", "-74.23594"],
    ["CONCENTRACION ESCOLAR SAN NICOLAS", "CLL. 40 SUR No. 7 D - 15 SAN NICOLAS", " 4.5604336", "-74.2428946"],
    ["I.E. COMPARTIR PRIMARIA", "CR. 15 A NO. 5 C - 16 SUR", "4.5711699", "-74.2395781"],
    ["COLEGIO MILITAR ALMIRANTE PADILLA", "TR. 11 C No. 5 - 02 SUR SALITRE", "4.5676849", "-74.2291616"],
    ["COLEGIO COLSUBSIDIO - MAIPORE", "CR. 2 No. 10 - 157 SUR", "4.57634", "-74.2024486"],
    ["I.E. PAZ Y ESPERANZA", "CLL 9 A SUR No 15 A - 285", "4.5784658", "-74.2345799"],
    ["SALON COMUNAL VILLA ITALIA", "CRA 16 D No 21 - 18 SUR", "4.5782215", "-74.2404886"],
    ["COLEGIO MILITAR LICEO SOCIAL COMPARTIR", "CLL 18 SUR NRO 9F 24 COMPARTIR", "4.5663854", "-74.2373281"],
    ["I.E. GENERAL SANTANDER", "CR. 9 NO. 14 - 10 CENTRO", "4.5837135", "-74.2187141"],
    ["IE GENERAL SANTANDER SD MI TIERNA EDAD", "CLL. 14 NO. 8 - 25 CENTRO", "4.5832067", "-74.2187936"],
    ["I.E. INTEGRADO DE SOACHA", "CR. 10 NO. 12 - 61 CENTRO", "4.5953383", "-74.1890455"],
    ["COLISEO GENERAL SANTANDER", "CLL. 15 NO. 8 - 53", "4.5835836", "-74.2179"],
    ["CONCENTRACION CAMILO TORRES", "CLL. 24 NO. 8 - 15", "4.6676589", "-74.1216614"],
    ["I E GENERAL SANTANDER SEDE LA VEREDITA", "CLL. 5 SUR No. 18 C - 34", "4.5867635", "-74.2293942"],
    ["SALON COMUNAL CIUDAD SATELITE", "CRA 6A No 8 - 39 SATELITE", "4.5803715", "-74.2225532"],
    ["UNIVER. DE CUNDINAMARCA EXTENSION SOACHA", "DIAG. 9 No. 4 B - 85", "4.5787419", "-74.2235145"],
    ["CENTRO DE DESARROLLO INFANTIL COMPENSAR", "CLL. 1 No. 18 F - 50 HOGARES", "4.5881225", "-74.2258148"],
    ["I.E. VIDA NUEVA", "CRA 19 A No 4 - 90 SUR", "4.5913516", "-74.2287993"],
    ["CDI JARDIN SOCIAL SOL Y LUNA", "CLL 1 No 4G-78", "4.576451", "-74.2261665"],
    ["ESCUE NORMAL SUPERIOR MARIA AUXILIADORA", "CALLE 12 NRO 7 53 CENTRO", "4.5820212", "-74.2204693"],
    ["IE LUIS HENRIQUEZ", "CRA 19A No 5 51 SUR", "4.5915205", "-74.2298077"],
    ["COLEGIO COOPERATIVO EUGENIO DIAZ CASTRO", "Cl. 17A  10 30 CENTRO", "4.5857245", "-74.2162274"],
    ["I.E. LA DESPENSA", "CR. 7 No. 58 - 22 LA DESPENSA", "4.5954866", "-74.187486"],
    ["I.E. MANUELA BELTRAN", "CLL. 56 NO. 10 - 07 LA DESPENSA", "4.5954186", "-74.1894645"],
    ["I.E. LEON XIII", "CR. 8 NO. 5 - 83 LEON XIII", "4.5978607", "-74.1939998"],
    ["CENTRO COMERCIAL GRAN PLAZA", "CRA 7 No 30B - 139", "4.5871605", "-74.2062329"],
    ["COLISEO LEON XIII", "CLL 48 No 9-05 LEON XIII", "4.5950806", "-74.1941814"],
    ["I.E. LA DESPENSA - CIUDAD VERDE", "TR. 37 No. 18-85 CIUDAD VERDE", "4.6091605", "-74.2207929"],
    ["I.E. LEON XIII - CHILOE", "DIAG. 28 No. 28 - 99 CIUDAD VERDE", "4.604289", "-74.2141094"],
    ["I.E. LA DESPENSA - MARCO FIDEL SUAREZ", "CR. 20 No. 45 A - 36", "4.5972262", "-74.1985489"],
    ["I.E. SOACHA AVANZA LA UNIDAD", "CRA 38 No 14 - 72", "4.6099618", "-74.2240982"],
    ["COLEGIO MINUTO DE DIOS CIUDAD VERDE", "CALLE 38 No 31  141 CIUDAD VERDE", "4.6061996", "-74.2132812"],
    ["IE BENEDICTO XVI", "CRA 8 No 5 17 LEON XIII", "4.5930197", "-74.1940019"],
    ["CENTRO COMERCIAL MERCURIO", "CRA 7 NRO 32 35", "4.5881981", "-74.2037484"],
    ["I.E. LUIS CARLOS GALAN", "CLL. 44 No. 27 B - 20 ESTE", "4.5791374", "-74.1830493"],
    ["I.E. CIUDADELA SUCRE", "CRA 33 B ESTE CON CLL. 38", "4.5732258", "-74.1815618"],
    ["I.E. LA ISLA", "CR. 33 C ESTE No. 40 - 195", "4.5732258", "-74.1815618"],
    ["I E JULIO CESAR TURBAY AYALA", "TV 9 ESTE No 45A- 80", "4.5843012", "-74.1904487"],
    ["I. E. GABRIEL GARCIA MARQUEZ", "TRANSVERSAL 6 A ESTE No 11 B - 107", "4.5840038", "-74.1867299"],
    ["IE LUIS C. GALAN-SD VILLAS DE CASALOMA", "CLL 59 B No 15 - 60 E", "4.5879688", "-74.1826665"],
    ["BIBLIOTECA MUNICIPAL LA ISLA", "CALLE 40 C No 33 C  21 E", "4.5729984", "-74.181218"],
    ["IE BUENOS AIRES SEDE A", "CRA 50 ESTE NRO 51 57", "4.5651028", "-74.1882965"],
    ["CENTRO COMERCIAL VENTURA TERREROS", "CRA 1 NRO 38  89 SOACHA", "4.5879878", "-74.1951394"],
    ["I.E. EL BOSQUE", "CLL. 32 CON CR 19 ESTE", "4.5755591", "-74.197187"],
    ["I.E. SAN MATEO SEDE A", "CR. 5 B ESTE No. 26  - 04", "4.5789912", "-74.2045204"],
    ["I.E. SAN MATEO SEDE B", "CR. 5 B ESTE No. 26  - 04", "4.5841875", "-74.0725156"],
    ["I.E. LICEO MAYOR DE SOACHA", "CLL. 38 No. 6 A - 55 ESTE", "4.582575", "-74.1945716"],
    ["CENTRO CIVICO DEPORTIVO SOACHA", "CALLE 38 No 6A  47 ESTE", "4.5831257", "-74.1955139"],
    ["I.E. LAS VILLAS- SEDE BARON DEL SOL", "CLL 13 No 1-03 SAN HUMBERTO", "4.5757399", "-74.2154599"],
    ["I.E. LAS VILLAS - SEDE LIBERTADORES", "CR. 8 ESTE No. 15 - 06", "4.5831414", "-74.2176463"],
    ["I.E. SOL NACIENTE", "CLL 15 A No. 1B - 12", "4.5812442", "-74.210985"],
    ["I.E. SAN MATEO - MARISCAL SUCRE", "CLL. 26 C No. 2 - 06 MARISCAL SUCRE", "4.5835158", "-74.2074837"],
    ["I E EDUARDO SANTOS SEDE PANAMERICANA", "CLL. 6 No. 2 C - 55 EL ALTICO", "4.5706345", "-74.2177372"],
    ["I.E. SOACHA PARA VIVIR MEJOR", "CLL. 7 D No. 2 A - 05", "4.5733724", "-74.220823"],
    ["SALON COMUNAL ALTOS DE LA FLORIDA", "CLL 5 No 6A-03 BARRIO SAN MARTIN", "4.5682197", "-74.2214562"],
    ["LICEO CRISTIANO VIDA NUEVA", "CRA 3 No  19 A 47 BARRIO EL SOL", "4.5810393", "-74.2129764"],
    ["IE EDUARDO SANTOS", "CALLE 10A No 2A 41 BARRIO SAN BERNARDINO", "4.5758647", "-74.2195226"],
    ["COLEGIO BOLIVAR PRIMARIA", "CR. 6 NO. 12 - 49 CENTRO", "4.5802918", "-74.2193661"],
    ["I. E. EUGENIO DIAZ CASTRO SEDE CHACUA", "CRA 1 ESTE No 2-37 VEREDA CHACUA", "4.529054", "-74.2244689"],
    ["I. E. EUGENIO DIAZ CASTRO SAN JORGE", "VEREDA SAN JORGE", "4.5027061", "-74.1963561"],
    ["SALON COMUNAL VEREDA FUSUNGA", "VEREDA FUSUNGA", "4.5335207", "-74.2022343"],
    ["I. E. EUGENIO DIAZ CASTRO SEDE PRIMARIA", "VEREDA EL CHARQUITO", "4.5439274", "-74.275619"],
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        departamento_name = 'CUNDINAMARCA'
        municipio_name = 'SOACHA'

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
