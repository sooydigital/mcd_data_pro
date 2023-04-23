host = "http://miclickdigital.pythonanywhere.com"
# host = "http://127.0.0.1:8000"
configuration_api = {
    "host": host,
    "user": "admin",
    "password": "admin",
    "get_all_cc_unprocessed": "{}/api/get_all_cc_by_status/?status=PENDING".format(host),
    "get_all_cc_processed": "{}/api/get_all_cc_by_status/?status=PROCESSED".format(host),
    "get_all_cc_error": "{}/api/get_all_cc_by_status/?status=ERROR".format(host),

    "get_all_cc_registered": "{}/api/get_all_cc_registered/".format(host),
    "update_profile_votante": "{}/api/update-multi-profile-votantes/".format(host),
    "insert_multi_votante": "{}/api/insert-multi-votantes/".format(host),

    "insert_only_cc_votante": "{}/api/insert_only_cc_votante/".format(host),
    "get_puesto_votation_by_cc": "{}/api/get_puesto_votation_by_cc/".format(host),
}

import json
import requests


class CALL_API_MCD():
    def __init__(self, configuration_api=configuration_api):
        self.session = requests.Session()
        self.session.auth = (configuration_api.get("user"), configuration_api.get("password"))

    def get_all_cc(self):
        print('call get_all_cc method')
        response = self.session.get(configuration_api.get("get_all_cc_registered"))
        result = json.loads(response.text)
        print('result', result)
        return result['data']

    def update_votantes(self, data):
        print('call update_votantes method')
        print('data', data)

        response = self.session.post(
            configuration_api.get("insert_multi_votante"),
            data=json.dumps(data),
        )
        result = json.loads(response.text)
        print('result', result)
        return result

    def update_profile_votantes(self, data):
        print('call update_votantes method')
        print('data', data)

        response = self.session.post(
            configuration_api.get("update_profile_votante"),
            data=json.dumps(data),
        )
        result = json.loads(response.text)
        print('result', result)
        return result

    def insert_only_cc_votante(self, data):
        print('call insert_only_cc_votante method')
        print('data', data)

        response = self.session.post(
            configuration_api.get("insert_only_cc_votante"),
            data=json.dumps(data),
        )
        result = json.loads(response.text)
        print('result', result)
        return result

    def get_cc_unprocessed(self):
        print('call get all cc unprocessed method')
        response = self.session.get(configuration_api.get("get_all_cc_unprocessed"))
        result = json.loads(response.text)
        print('result', result)
        return result['data']

    def get_cc_processed(self):
        response = self.session.get(configuration_api.get("get_all_cc_processed"))
        result = json.loads(response.text)
        return result['data']

    def get_cc_error(self):
        response = self.session.get(configuration_api.get("get_all_cc_error"))
        result = json.loads(response.text)
        return result['data']

    def get_cc_processed_and_error(self):
        cc_processed = self.get_cc_processed()
        cc_error = self.get_cc_error()
        return cc_processed + cc_error

    def get_puesto_de_votacion_by_cc(self, data):
        print('call get_puesto_de_votacion_by_cc ')
        print('data', data)

        response = self.session.post(
            configuration_api.get("get_puesto_votation_by_cc"),
            data=json.dumps(data),
        )
        result = json.loads(response.text)
        print('result', result)
        return result

if __name__ == "__main__":
    cam = CALL_API_MCD(configuration_api)
    # all_cc = cam.get_all_cc()
    # print('all_cc', all_cc)
    #
    # all_cc_unprocessed = cam.get_cc_unprocessed()
    # print('all_cc_unprocessed', all_cc_unprocessed)
    #
    # all_cc_processed = cam.get_cc_processed()
    # print('all_cc_processed', all_cc_processed)
    #
    # all_cc_error = cam.get_cc_error()
    # print('all_cc_error', all_cc_error)
    #
    # cc_processed_and_error = cam.get_cc_processed_and_error()
    # print('cc_processed_and_error', cc_processed_and_error)
    #
    # data = [{'codigo': '1007775718', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'IE CAFÉ MADRID', 'direccion': 'CR 8B # 35AN-45 BARRIO CAFÉ MADRID', 'mesa': '19', 'status': 'SUCCESS'}, {'codigo': '1005331477', 'departamento': 'SANTANDER', 'municipio': 'FLORIDABLANCA', 'puesto': 'COLEGIO JOSE ELIAS PUYANA SEDE B', 'direccion': 'CALLE 5 No. 14 -15 ALTAMIRA', 'mesa': '14', 'status': 'SUCCESS'}, {'codigo': '1098707186', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'I.E. ORIENTE MIRAFLORES SEDE A', 'direccion': 'KM 2 VIA PAMPLONA 50 - 46 BARRIO ALBANIA', 'mesa': '21', 'status': 'SUCCESS'}, {'codigo': '91283926', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'ESC NORMAL SUPERIOR SEDE A', 'direccion': 'CLL 30 # 27-163 BARRIO AURORA', 'mesa': '34', 'status': 'SUCCESS'}, {'codigo': '91228006', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'I.E. JOSE CELESTINO MUTIS', 'direccion': 'CR 3W # 57 - 14 BARRIO MUITS', 'mesa': '25', 'status': 'SUCCESS'}, {'codigo': '91536155', 'departamento': 'SANTANDER', 'municipio': 'FLORIDABLANCA', 'puesto': 'INSTITUTO LA TRINIDAD SEDE B', 'direccion': 'CARRERA 18B No. 61-55 LA TRINIDAD', 'mesa': '6', 'status': 'SUCCESS'}, {'codigo': '91493167', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'INST DE PROM SOC DEL NORTE SEDE A', 'direccion': 'CR 22B # 1-61 BARRIO SAN CRISTOBAL', 'mesa': '16', 'status': 'SUCCESS'}, {'codigo': '91234251', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'INST TEC SALESIANO ELOY VALENZ', 'direccion': 'AV QUEBRADA SECA # 11-85 BARRIO GIRARDOT', 'mesa': '20', 'status': 'SUCCESS'}, {'codigo': '13742461', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'I.E. LAS AMERICAS', 'direccion': 'CLL 33 # 36 - 16 BARRIO ALVAREZ', 'mesa': '3', 'status': 'SUCCESS'}, {'codigo': '13359771', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'UNIVERSIDAD COOP DE COLOMBIA', 'direccion': 'CLL 30A # 33 - 51 BARRIO QUINTADANIA', 'mesa': '3', 'status': 'SUCCESS'}]
    #
    # cam.update_votantes({"registros": data})
    #
    data = [{'codigo': '', 'departamento': '', 'municipio': '', 'puesto': '', 'direccion': '', 'mesa': '', 'status': 'SUCCESS'}, {'codigo': '1098740134', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'COOP ESPECIALIZ DE EDUC DE COMFENALCO', 'direccion': 'CLL 37 #21-34 PARQUE BOLIVAR', 'mesa': '22', 'status': 'SUCCESS'}, {'codigo': '1005280668', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'EFORSALUD', 'direccion': 'CLL 48 # 27 - 64 BARRIO SOTOMAYOR', 'mesa': '8', 'status': 'SUCCESS'}, {'codigo': '1005258389', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'COL DE LAS AMERICAS', 'direccion': 'CLL 51 # 24 - 20 BARRIO NUEVO SOTOMAYOR', 'mesa': '9', 'status': 'SUCCESS'}, {'codigo': '27926767', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'ESC NORMAL SUPERIOR SEDE A', 'direccion': 'CLL 30 # 27-163 BARRIO AURORA', 'mesa': '10', 'status': 'SUCCESS'}, {'codigo': '13810911', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'COL SAN PEDRITO', 'direccion': 'CLL 63 # 32 - 76 BARRIO CONUCOS', 'mesa': '2', 'status': 'SUCCESS'}, {'codigo': '1098661896', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'CENTRAL DE ABASTOS', 'direccion': 'VIA PALENQUE CAFE MADRID # 44 - 96', 'mesa': '7', 'status': 'SUCCESS'}, {'codigo': '13748885', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'ESC NORMAL SUPERIOR SEDE A', 'direccion': 'CLL 30 # 27-163 BARRIO AURORA', 'mesa': '5', 'status': 'SUCCESS'}, {'codigo': '63498457', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'I.E. SANTO ANGEL', 'direccion': 'CLL 9N # 18C - 04 BARRIO VILLA ROSA', 'mesa': '1', 'status': 'SUCCESS'}, {'codigo': '37831623', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'INST CALDAS', 'direccion': 'CIRCUNV 35 # 92 - 135 BARRIO TEJAR MODERNO', 'mesa': '9', 'status': 'SUCCESS'}, {'codigo': '63341402', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'UNIDADES TECNOLOGICAS DE SANT', 'direccion': 'AV LOS ESTUDIANTES # 9-82 BARRIO REAL DE MINAS', 'mesa': '7', 'status': 'SUCCESS'}, {'codigo': '1026555623', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'COL COOPERATIVO DE BUCARAMANGA', 'direccion': 'CLL 45 # 0-160 BARRIO CAMPO HERMOSO', 'mesa': '24', 'status': 'SUCCESS'}, {'codigo': '1098682029', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'COL TEC EMPRESARIAL JOSE MARIA', 'direccion': 'CLL 51 #13-97 BARRIO SAN MIGUEL', 'mesa': '12', 'status': 'SUCCESS'}, {'codigo': '27950691', 'departamento': 'SANTANDER', 'municipio': 'LEBRIJA', 'puesto': 'LA AGUADA DE CEFERINO', 'direccion': 'ESCUELA.', 'mesa': '1', 'status': 'SUCCESS'}, {'codigo': '5645526', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'COL SAN PEDRITO', 'direccion': 'CLL 63 # 32 - 76 BARRIO CONUCOS', 'mesa': '1', 'status': 'SUCCESS'}, {'codigo': '63479472', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'INST DE PROM SOC DEL NORTE SEDE A', 'direccion': 'CR 22B # 1-61 BARRIO SAN CRISTOBAL', 'mesa': '11', 'status': 'SUCCESS'}, {'codigo': '28247167', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'INST DE PROM SOC DEL NORTE SEDE A', 'direccion': 'CR 22B # 1-61 BARRIO SAN CRISTOBAL', 'mesa': '5', 'status': 'SUCCESS'}, {'codigo': '1098724341', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'ORDEN DE LOS CLÉRIGOS REG SOMASCOS', 'direccion': 'CR 26 # 11N-30 BARRIO REGADERO NORTE', 'mesa': '18', 'status': 'SUCCESS'}, {'codigo': '1095923905', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'ORDEN DE LOS CLÉRIGOS REG SOMASCOS', 'direccion': 'CR 26 # 11N-30 BARRIO REGADERO NORTE', 'mesa': '15', 'status': 'SUCCESS'}, {'codigo': '63339351', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'ORDEN DE LOS CLÉRIGOS REG SOMASCOS', 'direccion': 'CR 26 # 11N-30 BARRIO REGADERO NORTE', 'mesa': '6', 'status': 'SUCCESS'}, {'codigo': '63483930', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'CORP UNIVERSITARIA UNICIENCIA', 'direccion': 'CLL 37 # 11 - 58 BARRIO EL CENTRO', 'mesa': '15', 'status': 'SUCCESS'}, {'codigo': '63337281', 'departamento': 'SANTANDER', 'municipio': 'BUCARAMANGA', 'puesto': 'I.E. LA JUVENTUD SEDE A', 'direccion': 'CLL 5 N # 19 A - 12 BARRIO LA JUVENTUD', 'mesa': '1', 'status': 'SUCCESS'}]
    cam.update_votantes({"registros": data})
    # response = cam.get_puesto_de_votacion_by_cc({"registros": ['63362102']})
    # print(response)
    #
    # data = "9126869"
    # cam.insert_only_cc_votante({"registro": data})