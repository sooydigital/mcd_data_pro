
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from django.http import FileResponse
from django.conf import settings
from myapp.controller import DataController
media_root = settings.MEDIA_ROOT

class DownloadController():

    @staticmethod
    def generate_document(hoja, data_mappings):
        encabezado = [
            "N.",
            "CÓDIGO",
            "PRE-CANDIDATO",
            "CÓDIGO",
            "LÍDER",
            "NOMBRES",
            "APELLIDOS",
            "CÉDULA",
            "CONTACTO",
            "CORREO",
            "DÍA",
            "MES",
            "AÑO",
            "18 - 28",
            "29 - 44",
            "45 - 59",
            "60 <",
            "GENERO",
            "DIRECCIÓN",
            "BARRIO",
            "MUNICIPIO",
            "NUIP",
            "DEPARTAMENTO",
            "MUNICIPIO",
            "PUESTO DE VOTACIÓN",
            "MESA",
            "DIRECCIÓN",
        ]
        hoja.append(encabezado)

        data = [
            "1",
            "G01",
            "MAC GRÉGOR HERRERA ANAYA",
            "G01_001",
            "ÓSCAR JESÚS REYES PEÑA",
            "Mac Grégor",
            "Herrera Anaya",
            "1095933743",
            "3002156687",
            "Macgregorherrera@gmail.com",
            "31",
            "8",
            "1993",
            "",
            "X",
            "",
            "",
            "Hombre",
            "Calle 49 N. 23 - 107 Apto 501",
            "El Poblado",
            "Girón",
            "1095933743",
            "SANTANDER",
            "GIRON",
            "COLEGIO GABRIEL GARCIA MARQUEZ",
            "12",
            "TRANSV 20 # 10-20",
            ""
        ]
        hoja.append(data)

        data = [
            "2",
            "G01",
            "MAC GRÉGOR HERRERA ANAYA",
            "G01_001",
            "ÓSCAR JESÚS REYES PEÑA",
            "Mac ",
            "Herrera ",
            "1095933732",
            "3002156632",
            "Macgregorherrera_1@gmail.com",
            "31",
            "8",
            "1993",
            "",
            "X",
            "",
            "",
            "Hombre",
            "Calle 49 N. 23 - 107 Apto 501",
            "El Poblado",
            "Girón",
            "1095933743",
            "SANTANDER",
            "GIRON",
            "COLEGIO GABRIEL GARCIA MARQUEZ",
            "12",
            "TRANSV 20 # 10-20",
            ""
        ]
        hoja.append(data)

        # TODO: check this
        votantes = data_mappings.get('votante_mapping')
        custom_user_mapping = data_mappings.get('custom_user_mapping')
        custom_user_super_visor_mapping = data_mappings.get('custom_user_super_visor_mapping')
        votante_profile_mapping = data_mappings.get('votante_profile_mapping')
        votante_puesto_votacion_mapping = data_mappings.get('votante_puesto_votacion_mapping')
        puesto_votacion_mapping = data_mappings.get('puesto_votacion_mapping')


        contador = 0
        for votante_id, votante_info in votantes.items():
            contador = contador + 1
            super_visor_code = ""
            super_visor_full_name = ""
            custom_user_code = ""
            custom_user_full_name = ""

            votante_profile_first_name = ""
            votante_profile_last_name = ""
            votante_profile_document_id = ""
            votante_profile_mobile_phone = ""
            votante_profile_email = ""
            votante_profile_birthday_day = ""
            votante_profile_birthday_month = ""
            votante_profile_birthday_year = ""
            # todo check range age
            votante_profile_gender = ""
            votante_profile_address = ""
            votante_profile_barrio = ""
            votante_profile_municipio = ""

            votante_puesto_votacion_departamento = ""
            votante_puesto_votacion_municipio = ""
            votante_puesto_votacion_puesto = ""
            votante_puesto_votacion_mesa = ""
            votante_puesto_votacion_direccion = ""

            custom_user_id = votante_info.get('custom_user')
            if custom_user_id:
                custom_user_data = custom_user_mapping.get(custom_user_id, {})
                if custom_user_data:
                    super_visor_id = custom_user_data.get('super_visor')
                    custom_user_code = custom_user_data.get("code", "")
                    custom_user_full_name = custom_user_data.get("full_name", "")
                    if super_visor_id:
                        super_visor_data = custom_user_super_visor_mapping.get(super_visor_id, {})
                        super_visor_code = super_visor_data.get("code", "")
                        super_visor_full_name = super_visor_data.get("full_name", "")
                else:
                    super_visor_data = custom_user_super_visor_mapping.get(custom_user_id, {})
                    super_visor_code = super_visor_data.get("code", "")
                    super_visor_full_name = super_visor_data.get("full_name", "")

            votante_profile_data = votante_profile_mapping.get(votante_id, {})
            if votante_profile_data:
                votante_profile_first_name = votante_profile_data.get('first_name', "")
                votante_profile_last_name = votante_profile_data.get('last_name', "")
                votante_profile_document_id = votante_info.get('document_id', "")
                votante_profile_mobile_phone = votante_profile_data.get('mobile_phone', "")
                votante_profile_email = votante_profile_data.get('email', "")
                birthday = votante_profile_data.get('birthday', None)
                if birthday:
                    votante_profile_birthday_day = birthday.day
                    votante_profile_birthday_month = birthday.month
                    votante_profile_birthday_year = birthday.year

                # todo check range age
                votante_profile_gender = votante_profile_data.get('gender', "")
                votante_profile_address = votante_profile_data.get('address', "")
                votante_profile_barrio = votante_profile_data.get('barrio', "")
                votante_profile_municipio = votante_profile_data.get('municipio', "")

            votante_puesto_votacion = votante_puesto_votacion_mapping.get(votante_id, {})
            if votante_puesto_votacion:
                votante_puesto_votacion_mesa = votante_puesto_votacion.get('mesa')
                votante_puesto_votacion_id = votante_puesto_votacion.get('puesto_votacion_id')
                puesto_votacion = puesto_votacion_mapping.get(votante_puesto_votacion_id)
                if puesto_votacion:
                    votante_puesto_votacion_departamento = puesto_votacion.get('departamento', '')
                    votante_puesto_votacion_municipio = puesto_votacion.get('municipio', '')
                    votante_puesto_votacion_puesto = puesto_votacion.get('name', '')
                    votante_puesto_votacion_direccion = puesto_votacion.get('address', '')

            data_base = [
                contador,
                super_visor_code,
                super_visor_full_name,
                custom_user_code,
                custom_user_full_name,

                votante_profile_first_name,
                votante_profile_last_name,
                votante_profile_document_id,
                votante_profile_mobile_phone,
                votante_profile_email,
                votante_profile_birthday_day,
                votante_profile_birthday_month,
                votante_profile_birthday_year,
                "","","","", # todo check range age
                votante_profile_gender,
                votante_profile_address,
                votante_profile_barrio,
                votante_profile_municipio,

                votante_profile_document_id,
                votante_puesto_votacion_departamento,
                votante_puesto_votacion_municipio,
                votante_puesto_votacion_puesto,
                votante_puesto_votacion_mesa,
                votante_puesto_votacion_direccion,
            ]

            hoja.append(data_base)


    @staticmethod
    def document_download():
        folder_name = 'generate_reports'
        file_name = 'votantes.xlsx'
        file_path = '{}/{}/{}'.format(media_root, folder_name, file_name)

        f = open("{}".format(file_path), "a")
        f.close()

        libro = Workbook()
        hoja = libro.active
        data_mappings = DataController.get_votantes_information_to_download()
        DownloadController.generate_document(hoja, data_mappings)
        libro.save(file_path)
        response = FileResponse(open(file_path, 'rb'))
        return response




