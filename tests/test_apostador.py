import json
from unicodedata import name
from unittest import TestCase

from faker import Faker
from faker.generator import random

from app import app

class TestApostador(TestCase):
    
    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()

        nuevo_usuario = {
            "usuario": self.data_factory.name(),
            "contrasena": self.data_factory.word()
        }

        solicitud_nuevo_usuario = self.client.post("/signin",
                                                   data=json.dumps(nuevo_usuario),
                                                   headers={'Content-Type': 'application/json'})

        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())

        self.token = respuesta_al_crear_usuario["token"]
        self.usuario_code = respuesta_al_crear_usuario["id"]
        
    def test_crear_apostador(self):
        nuevo_apostador = {
            "usuario": self.data_factory.name(), 
            "contrasena": self.data_factory.word(), 
            "nombre_apostador": self.data_factory.name(), 
            "apellido_apostador": self.data_factory.name(),
            "correo": self.data_factory.email(),
            "saldo": round(random.uniform(10000, 500000), 2)
        }
        endpoint_apostadores = "/apostadores"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_apostador = self.client.post(endpoint_apostadores,
                                                   data=json.dumps(nuevo_apostador),
                                                   headers=headers)

        respuesta_al_crear_apostador = json.loads(solicitud_nuevo_apostador.get_data())

        self.assertEqual(solicitud_nuevo_apostador.status_code, 200)
        self.assertEqual(respuesta_al_crear_apostador["usuario"], nuevo_apostador['usuario'])
        self.assertEqual(respuesta_al_crear_apostador["contrasena"], nuevo_apostador['contrasena'])
        self.assertEqual(respuesta_al_crear_apostador["nombre_apostador"], nuevo_apostador['nombre_apostador'])
        self.assertEqual(respuesta_al_crear_apostador["apellido_apostador"], nuevo_apostador['apellido_apostador'])
        self.assertEqual(respuesta_al_crear_apostador["correo"], nuevo_apostador['correo'])
        self.assertEqual(float(respuesta_al_crear_apostador["saldo"]), nuevo_apostador['saldo'])    
        
    def test_obtener_apostador_por_id(self):
        nuevo_apostador = {
            "usuario": self.data_factory.name(), 
            "contrasena": self.data_factory.word(), 
            "nombre_apostador": self.data_factory.name(), 
            "apellido_apostador": self.data_factory.name(),
            "correo": self.data_factory.email(),
            "saldo": round(random.uniform(10000, 500000), 2)
        }
        endpoint_apostadores = "/apostadores"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_apostador = self.client.post(endpoint_apostadores,
                                                   data=json.dumps(nuevo_apostador),
                                                   headers=headers)

        respuesta_al_crear_apostador = json.loads(solicitud_nuevo_apostador.get_data())
        id_apostador = respuesta_al_crear_apostador["id"]
        endpoint_apostadorId = "/apostador/{}".format(str(id_apostador))

        solicitud_consultar_apostador_por_id = self.client.get(endpoint_apostadorId, headers=headers)
        apostador_obtenido = json.loads(solicitud_consultar_apostador_por_id.get_data())

        self.assertEqual(solicitud_consultar_apostador_por_id.status_code, 200)
        self.assertEqual(apostador_obtenido, respuesta_al_crear_apostador)
        
    def test_obtener_apostadores(self):
        endpoint_apostadores = "/apostadores"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        nuevos_apostadores=0
        solicitud_consulta_todos_apostadores=self.client.get(endpoint_apostadores, headers=headers)
        lista_apostadores1 = json.loads(solicitud_consulta_todos_apostadores.get_data())
        total_apostadores1=len(json.loads(solicitud_consulta_todos_apostadores.get_data()))
        self.assertEqual(solicitud_consulta_todos_apostadores.status_code, 200)
        
        nuevo_apostador = {
            "usuario": self.data_factory.name(), 
            "contrasena": self.data_factory.word(), 
            "nombre_apostador": self.data_factory.name(), 
            "apellido_apostador": self.data_factory.name(),
            "correo": self.data_factory.email(),
            "saldo": round(random.uniform(10000, 500000), 2)
        }
        solicitud_nuevo_apostador = self.client.post(endpoint_apostadores,
                                                   data=json.dumps(nuevo_apostador),
                                                   headers=headers)
        if solicitud_nuevo_apostador.status_code==200:
            nuevos_apostadores=nuevos_apostadores+1
        respuesta_al_crear_apostador = json.loads(solicitud_nuevo_apostador.get_data())
        id_apostador = respuesta_al_crear_apostador["id"]

        nuevo_apostador1 = {
            "usuario": self.data_factory.name(), 
            "contrasena": self.data_factory.word(), 
            "nombre_apostador": self.data_factory.name(), 
            "apellido_apostador": self.data_factory.name(),
            "correo": self.data_factory.email(),
            "saldo": round(random.uniform(10000, 500000), 2)
        }
        solicitud_nuevo_apostador1 = self.client.post(endpoint_apostadores,
                                                   data=json.dumps(nuevo_apostador1),
                                                   headers=headers)
        if solicitud_nuevo_apostador1.status_code==200:
            nuevos_apostadores=nuevos_apostadores+1
        respuesta_al_crear_apostador1 = json.loads(solicitud_nuevo_apostador1.get_data())
        id_apostador1 = respuesta_al_crear_apostador1["id"]
        
        nuevo_apostador2 = {
            "usuario": self.data_factory.name(), 
            "contrasena": self.data_factory.word(), 
            "nombre_apostador": self.data_factory.name(), 
            "apellido_apostador": self.data_factory.name(),
            "correo": self.data_factory.email(),
            "saldo": round(random.uniform(10000, 500000), 2)
        }
        solicitud_nuevo_apostador2 = self.client.post(endpoint_apostadores,
                                                   data=json.dumps(nuevo_apostador2),
                                                   headers=headers)
        if solicitud_nuevo_apostador2.status_code==200:
            nuevos_apostadores=nuevos_apostadores+1
        respuesta_al_crear_apostador2 = json.loads(solicitud_nuevo_apostador2.get_data())
        id_apostador2 = respuesta_al_crear_apostador2["id"]

        solicitud_consulta_todos_apostadores2=self.client.get(endpoint_apostadores, headers=headers)
        lista_apostadores2 = json.loads(solicitud_consulta_todos_apostadores2.get_data())
        total_apostadores2=len(lista_apostadores2)
        self.assertEqual(solicitud_consulta_todos_apostadores.status_code, 200)
        self.assertEqual(total_apostadores1+nuevos_apostadores, total_apostadores2)
        
    def test_eliminar_apostador(self):
        nuevos_apostadores=0
        
        endpoint_apostadores = "/apostadores"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        nuevo_apostador = {
            "usuario": self.data_factory.name(), 
            "contrasena": self.data_factory.word(), 
            "nombre_apostador": self.data_factory.name(), 
            "apellido_apostador": self.data_factory.name(),
            "correo": self.data_factory.email(),
            "saldo": round(random.uniform(10000, 500000), 2)
        }
        solicitud_nuevo_apostador = self.client.post(endpoint_apostadores,
                                                   data=json.dumps(nuevo_apostador),
                                                   headers=headers)
        if solicitud_nuevo_apostador.status_code==200:
            nuevos_apostadores=nuevos_apostadores+1
            respuesta_al_crear_apostador = json.loads(solicitud_nuevo_apostador.get_data())
            id_apostador = respuesta_al_crear_apostador["id"]
        
        nuevo_apostador1 = {
            "usuario": self.data_factory.name(), 
            "contrasena": self.data_factory.word(), 
            "nombre_apostador": self.data_factory.name(), 
            "apellido_apostador": self.data_factory.name(),
            "correo": self.data_factory.email(),
            "saldo": round(random.uniform(10000, 500000), 2)
        }
        solicitud_nuevo_apostador1 = self.client.post(endpoint_apostadores,
                                                   data=json.dumps(nuevo_apostador1),
                                                   headers=headers)
        if solicitud_nuevo_apostador1.status_code==200:
            nuevos_apostadores=nuevos_apostadores+1
            respuesta_al_crear_apostador1 = json.loads(solicitud_nuevo_apostador1.get_data())
            id_apostador = respuesta_al_crear_apostador1["id"]
        
        
        solicitud_consulta_apostadores_antes = self.client.get(endpoint_apostadores, headers=headers)
        total_apostadores_antes = len(json.loads(solicitud_consulta_apostadores_antes.get_data()))

        endpoint_apostador = "/apostador/{}".format(str(id_apostador))
        solicitud_eliminar_apostador = self.client.delete(endpoint_apostador, headers=headers)
        
        solicitud_consulta_apostadores_despues = self.client.get(endpoint_apostadores, headers=headers)
        total_apostadores_despues = len(json.loads(solicitud_consulta_apostadores_despues.get_data()))

        self.assertLess(total_apostadores_despues, total_apostadores_antes)
        self.assertEqual(solicitud_eliminar_apostador.status_code, 204)
        
    def test_editar_apostador(self):
        endpoint_apostadores = "/apostadores"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        nuevo_apostador = {
            "usuario": self.data_factory.name(), 
            "contrasena": self.data_factory.word(), 
            "nombre_apostador": self.data_factory.name(), 
            "apellido_apostador": self.data_factory.name(),
            "correo": self.data_factory.email(),
            "saldo": round(random.uniform(10000, 500000), 2)
        }
        solicitud_nuevo_apostador = self.client.post(endpoint_apostadores,
                                                   data=json.dumps(nuevo_apostador),
                                                   headers=headers)
        respuesta_al_crear_apostador = json.loads(solicitud_nuevo_apostador.get_data())
        nombre_apostador_antes = respuesta_al_crear_apostador["nombre_apostador"]
        id_apostador = respuesta_al_crear_apostador["id"]

        endpoint_apostador = "/apostador/{}".format(str(id_apostador))
        print(endpoint_apostador)
        apostador_editado = {
            "usuario": "user1", 
            "contrasena": "12345", 
            "nombre_apostador": "Luis Edo", 
            "apellido_apostador": "Perez Guevara",
            "correo": "otromail@hot.com",
            "saldo": 2000000
        }
        print(endpoint_apostador)
        solicitud_editar_apostador = self.client.put(endpoint_apostador, data=json.dumps(apostador_editado), headers=headers)

        respuesta_al_editar_apostador = json.loads(solicitud_editar_apostador.get_data())
        nombre_apostador_despues = respuesta_al_editar_apostador["nombre_apostador"]

        self.assertEqual(solicitud_editar_apostador.status_code, 200)
        self.assertNotEqual(nombre_apostador_antes, nombre_apostador_despues)

