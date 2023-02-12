from django.core.management.base import BaseCommand
from myapp.models import Municipio, Barrio, Comuna

class Command(BaseCommand):
    def handle(self, *args, **options):
        locations = {
            "BUCARAMANGA": {
                "COMUNA 1": [
                    'KENEDDY',
                    'TEJAR NORTE',
                    'BETANIA',
                    'CAFÉ MADRID',
                    'MIN DE DIOS',
                    'COLORADOS ',
                    'VILLA ROSA',
                ],
                "COMUNA 2": [
                    'SAN CRISTOBAL',
                    'REGADERO',
                    'VILLA HELENA',
                    'BOSCONIA',
                    'LA JUVENTUD',
                    'TRANSICION',
                    'LA INDEPENDENCIA',
                    'ESPERANZAS',
                ],
                "COMUNA 3": [
                    "LA UNIVERSIDAD",
                    "SAN FCO",
                    "COMUNEROS",
                    "MUTUALIDAD",
                    "SAN RAFAEL",
                ],
                "COMUNA 4": ["GIRARDOT",
                            "GAITAN",
                            "SANTANDER",
                            "LA FERIA",
                            "GRANADA",
                            ],
                "COMUNA 5": [
                    "LA JOYA",
                    "CAMPOHERMOSO",
                    "ALFONSO LOPEZ",
                ],
                "COMUNA 6": [
                    "LA CONCORDIA",
                    "LA VICTORIA",
                    "SAN MIGUEL",
                    "RICAURTE",
                ],
                "COMUNA 7": [
                    "CIUDADELA REAL DE MINAS",
                ],
                "COMUNA 8": [
                    "LOS CANELOS ",
                    "PABLO VI",
                    "BUCARAMANGA",
                ],
                "COMUNA 9": [
                    "LA LIBERTAD",
                    "SAN MARTIN",
                    "EL DIAMANTE",
                ],
                "COMUNA 10": [
                    "PROVENZA",
                    "DIAMANTE II",
                    "SAN LUIS",
                    "FONTANA",
                ],
                "COMUNA 11": [
                    "EL PORVENIR",
                    "DELICIAS ALTAS",
                    "MANUELA BELTRAN",
                    "EL ROCIO ",
                    "DANGON",
                    "TOLEDO PLATA ",
                ],
                "COMUNA 12": [
                    "NUEVO SOTOMAYOR",
                    "CONUCOS",
                    "EL JARDIN ",
                    "SOTOMAYOR",
                    "CABECERA DEL LLANO ",
                    "TERRAZAS",
                    "PAN DE AZUCAR",
                ],
                "COMUNA 13": [
                    "SAN ALONSO",
                    "ALARCON ",
                    "LA AURORA",
                    "ALVAREZ",
                    "BOLIVAR",
                    "ANTONIA SANTOS",
                    "MEJORAS PUBLICAS",
                    "EL PRADO",
                ],
                "COMUNA 14": [
                    "ALBANIA",
                    "MIRAFLORES",
                    "MORRORICO",
                    "BUENOS AIRES",
                ],
                "COMUNA 15": [
                    "GARCIA ROVIRA",
                    "EL CENTRO",
                ],
                "COMUNA 16": [
                    "EL TEJAR",
                    "LAGOS DEL CAZIQUE",
                ],
                "COMUNA 17": [
                    "MUTIS",
                    "ESTORAQUES",
                    "MONTERREDONDO",
                ],
                "RURAL": [
                    "VIJAGUAL",
                    "LA CAPILLA MONSERRATE",
                ]
            },
            "FLORIDABLANCA": {
                "ALTAMIRA Y CASCO ANTIGUO": ["FLORIDA CENTRO",
                                             "JARDIN DE LIMONCITO",
                                             "LIMONCITO ",
                                             "ALTAMIRA",
                                             "VILLAS DE SAN FCO ",
                                             "VILLA PIEDRA DEL SOL ",
                                             "LA PAZ",
                                             ],
                "CAÑAVERAL": [
                    "CAÑAVERAL",
                ],
                "BUCARICA": [
                    "BUCARICA",
                    "SIMON BOLIVAR",
                    "CARACOLI",
                ],
                "CALDAS Y REPOSO": [
                    "CALDAS",
                    "SAN BERNARDO",
                    "VILLALUZ",
                    "LAURELES",
                    "EL DORADO",
                    "HACIENDA SAN JUAN ",
                    "ALTOVIENTO 1,2",
                    "ZAPAMANGA 1,2,3,4,5,6,7",
                ],
                "BOSQUE MOLINOS": [
                    "BOSQUE ",
                    "MOLINOS",
                    "NIZA",
                    "VILLA ESPAÑA",
                    "PALOMITAS",
                    "PARQUE SAN AGUSTIN ",
                    "VILLAS DE MEDITERRANEO",
                ],
                "LAGOS-BELLAVISTA": [
                    "LAGOS 1, 2,3,4 Y 5",
                    "BELLAVISTA",
                    "ALTOS DE BELLAVISTA",
                ],
                "CIUDAD VALENCIA-SANTANA": [
                    "CIUDAD VALENCIA",
                    "SANTANA ",
                    "ROSALES",
                    "PRADOS DEL SUR",
                    "GUANATA",
                ],
                "CUMBRE-CARMEN ": [
                    "EL CARMEN 1, 2, 3, 4",
                    "VILLA ALCAZAR",
                    "LA CUMBRE",
                    "GARCIA ECHEVERRY ",
                    "SURATOQUE ",
                ]
            },
            "GIRON": {
                "COMUNA FAKE": [
                    "NUEVO GIRON",
                    "RIBERAS DEL RIO ",
                    "BAHONDO",
                    "MIRADOR DE ARENALES",
                    "ARENALES",
                    "ARENALES CAMPESTRE",
                    "VILLAS DE SAN JUAN",
                    "LA MESETA",
                    "RIO PRADO",
                    "CONSUELO",
                    "CAMBULOS ",
                    "VILLAS DE DON JUAN ",
                    "VILLAMPIS",
                    "PUERTO MADERO",
                    "BRISAS DEL CAMPO",
                    "CIUDADELA VILLAMIL",
                    "SAN JORGE",
                    "PORTAL CAMPESTRE",
                    "VILLA CAMPESTRE",
                    "SANTA CRUZ",
                    "RIO DE ORO ",
                    "GALLINERAL",
                    "EL TEJAR",
                    "LA PLAYA",
                    "SAGRADO CORAZON ",
                    "LA CAMPIÑA",
                    "ELOY VALENZUELA",
                    "ALDEA ALTA",
                    "ALDEA BAJA",
                    "PARAISO",
                    "CORVIANDI 2",
                    "GIRALUZ",
                    "BELLAVISTA",
                    "GIRON CENTRO",
                    "POBLADO ",
                    "MURALLAS",
                    "SAN JUAN",
                    "EL CARRIZAL",
                    "PALENQUE",
                    "LA ESMERALDA",
                    "RINCON DE GIRON ",
                ]
            },
            "LEBRIJA": {
                "COMUNA FAKE 2": [
                    "SANTA BARBARA",
                    "LA LOMA",
                    "VILLA CLAUDIA",
                    "EL CHIRILI BRISAS N.AMAN",
                    "VILLA ESPERANZA",
                    "LOS PINOS",
                    "MARIA PAZ",
                    "CAMPESTRE REAL",
                    "CAMPO ALEGRE",
                    "SAN DIEGO",
                    "BRISAS DE CAMPO ALEGRE",
                    "EL PESEBRE",
                    "CIUDADELA DEL RIO",
                    "SAN JORGE",
                    "LAURELES",
                    "ESMERALDA",
                    "LOS ROSALES",
                    "EL PRADO",
                    "ASOVICOL",
                    "LA POPA",
                    "VILLA PARAISO",
                    "LA CIUDADELA RIOS CORTEZ",
                    "CENTRO "
                ]
            },
            "PIEDECUESTA": {
                "COMUNA FAKE 3": [
                    "QUINTA GRANADA",
                    "SAN CARLOS",
                    "SAN FRANCISCO",
                    "SAN CRISTOBAL ",
                    "CABECERA",
                    "LA COLINA ",
                    "EL MOLINO",
                    "PALERMO",
                    "REFUGIO ",
                    "PAYSANDU",
                    "DIVINO NIÑO ",
                    "PARAISO",
                    "NUEVA COLOMBIA",
                    "SAN LUIS",
                    "ARGENTINA ",
                    "SAN TELMO ",
                    "BUENOS AIRES",
                    "VILLA NAVARRA",
                    "BARILOCHE",
                    "CAMPO VERDE",
                    "EL TRAPICHE",
                    "LA TACHUELA",
                    "CHACARITA",
                    "LA FERIA",
                    "LA CANTERA",
                    "SAN RAFAEL ",
                    "CENTRO",
                    "HOYO GRANDE",
                    "HOYO CHIQUITO",
                    "LA CASTELLANA",
                    "LA CANDELARIA ",
                    "PASEO DEL PUENTE ",
                    "PORTAL DEL VALLE",
                    "PUERTO MADERO",
                    "BARRO BLANCO ",
                    "LOS CISNES ",
                ]
            }
        }

        for municipio, comunas in locations.items():
            # create municipo
            if not Municipio.objects.filter(name=municipio).exists():
                print(">>> Municipio with label: '{}' created".format(municipio))
                municipio_object = Municipio(name=municipio)
                municipio_object.save()
                for comuna, barrios in comunas.items():
                    if not Comuna.objects.filter(name=comuna).exists():
                        print(">>>> Comuna with label: '{}' created".format(comuna))
                        comuna_object = Comuna(municipio=municipio_object, name=comuna)
                        comuna_object.save()
                        for barrio in barrios:
                            if not Barrio.objects.filter(name=barrio, comuna__municipio__name=municipio).exists():
                                print(">>>>> Barrio with label: '{}' created".format(barrio))
                                barrio_object = Barrio(comuna=comuna_object, name=barrio)
                                barrio_object.save()