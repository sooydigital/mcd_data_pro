
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from django.http import FileResponse
from django.conf import settings
media_root = settings.MEDIA_ROOT

class DownloadController():

    @staticmethod
    def generate_document(hoja, votantes):
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
        for poll_response in votantes:
            data_base = [
                poll_response.created_at.strftime("%y-%m/%d %H:%M"),
                poll_response.id,
                "{} {}".format(poll_response.interviewer.first_name, poll_response.interviewer.last_name),
                "{}, {}".format(poll_response.latitude, poll_response.longitude),
                poll_response.gender,
                poll_response.range_age,
                poll_response.municipio.name,
                poll_response.barrio.name,
            ]
            answers = poll_response.answer_set.all()
            for answer in answers:
                data_answer = [
                    answer.question.label,
                    answer.response
                ]
                hoja.append(data_base + data_answer)


    @staticmethod
    def document_download():
        folder_name = 'generate_reports'
        file_name = 'votantes.xlsx'
        file_path = '{}/{}/{}'.format(media_root, folder_name, file_name)

        f = open("{}".format(file_path), "a")
        f.close()

        libro = Workbook()
        hoja = libro.active
        votantes = []
        DownloadController.generate_document(hoja, votantes)
        libro.save(file_path)
        response = FileResponse(open(file_path, 'rb'))
        return response


