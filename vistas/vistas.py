from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from modelos import db, Apuesta, ApuestaSchema, Usuario, UsuarioSchema, Carrera, CarreraSchema, CompetidorSchema, \
    Competidor, ReporteSchema, Apostador, ApostadorSchema

apuesta_schema = ApuestaSchema()
carrera_schema = CarreraSchema()
competidor_schema = CompetidorSchema()
usuario_schema = UsuarioSchema()
reporte_schema = ReporteSchema()
apostador_schema = ApostadorSchema()


class VistaApostadores(Resource):
    @jwt_required()
    def get(self):
        return [apostador_schema.dump(apos) for apos in Apostador.query.all()]
    
    #@jwt_required()
    def post(self):
        print("Vista Apostadores POST")
        print(request.json)
        nuevo_apostador=Apostador(nombre_apostador=request.json["nombre_apostador"],
                                  apellido_apostador=request.json["apellido_apostador"],
                                  usuario=request.json["usuario"],
                                  contrasena=request.json.get("contrasena", '12345'),
                                  correo=request.json["correo"],
                                  saldo=request.json.get("saldo", '0')
                                  )
        print(nuevo_apostador.nombre_apostador)
        print(nuevo_apostador.apellido_apostador)
        db.session.add(nuevo_apostador)
        print("antes commit")
        db.session.commit()
        print("Antes del return")
        return apostador_schema.dump(nuevo_apostador)

class VistaApostador(Resource):
    @jwt_required()
    def get(self, id_apostador):
        return apostador_schema.dump(Apostador.query.get_or_404(id_apostador))
    
    jwt_required()
    def put(self, id_apostador):
        print(request)
        print(request.json)
        print("Inicio Put")
        apostador = Apostador.query.get_or_404(id_apostador)
        print("Consulta Put")
        apostador.nombre_apostador = request.json.get("nombre_apostador", apostador.nombre_apostador)
        print(apostador.nombre_apostador)
        apostador.apellido_apostador = request.json.get("apellido_apostador", apostador.apellido_apostador)
        print(apostador.apellido_apostador)
        apostador.usuario = request.json.get("usuario", apostador.usuario)
        print(apostador.usuario)
        apostador.contrasena=request.json.get("contrasena", apostador.contrasena)
        print(apostador.contrasena)
        apostador.correo = request.json.get("correo", apostador.correo)
        print(apostador.correo)
        print("Antes de Saldo Put")
        apostador.saldo = request.json.get("saldo", apostador.saldo)
        print(apostador.saldo)
        print("Despues de Saldo Put")
        db.session.commit()
        print("Despues COMMIT Put")
        return apostador_schema.dump(apostador)
    
    @jwt_required()
    def delete(self, id_apostador):
        apostador = Apostador.query.get_or_404(id_apostador)
        db.session.delete(apostador)
        db.session.commit()
        return '', 204

class VistaSignInApostador(Resource):    
    def post(self):
        nuevo_apostador = Apostador(usuario=request.json["usuario"], contrasena=request.json["contrasena"], 
                                    nombre_apostador=request.json["nombre_apostador"], apellido_apostador=request.json["apellido_apostador"], 
                                    correo=request.json["correo"], saldo=request.json["saldo"]
                                    )
        db.session.add(nuevo_apostador)
        db.session.commit()
        token_de_acceso = create_access_token(identity=nuevo_apostador.id)
        return {"mensaje": "apostador creado exitosamente", "token": token_de_acceso, "id": nuevo_apostador.id}

    def put(self, id_apostador):
        apostador = Apostador.query.get_or_404(id_apostador)
        apostador.contrasena = request.json.get("contrasena", apostador.contrasena)
        db.session.commit()
        return apostador_schema.dump(apostador)

    def delete(self, id_apostador):
        apostador = Apostador.query.get_or_404(id_apostador)
        db.session.delete(apostador)
        db.session.commit()
        return '', 204

class VistaLogInApostador(Resource):
    
    def post(self):
        apostador = Apostador.query.filter(Apostador.usuario == request.json["usuario"],
                                       Apostador.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if apostador is None:
            return "El apostador no existe", 404
        else:
            token_de_acceso = create_access_token(identity=apostador.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}
        
class VistaSignIn(Resource):

    def post(self):
        nuevo_usuario = Usuario(usuario=request.json["usuario"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity=nuevo_usuario.id)
        return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso, "id": nuevo_usuario.id}

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204


class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                       Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}


class VistaCarrerasUsuario(Resource):

    @jwt_required()
    def post(self, id_usuario):
        nueva_carrera = Carrera(nombre_carrera=request.json["nombre"])
        for item in request.json["competidores"]:
            cuota = round((item["probabilidad"] / (1 - item["probabilidad"])), 2)
            competidor = Competidor(nombre_competidor=item["competidor"],
                                    probabilidad=item["probabilidad"],
                                    cuota=cuota,
                                    id_carrera=nueva_carrera.id)
            nueva_carrera.competidores.append(competidor)
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.carreras.append(nueva_carrera)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un carrera con dicho nombre', 409

        return carrera_schema.dump(nueva_carrera)

    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [carrera_schema.dump(carrera) for carrera in usuario.carreras]


class VistaCarrera(Resource):

    @jwt_required()
    def get(self, id_carrera):
        return carrera_schema.dump(Carrera.query.get_or_404(id_carrera))

    @jwt_required()
    def put(self, id_carrera):
        carrera = Carrera.query.get_or_404(id_carrera)
        carrera.nombre_carrera = request.json.get("nombre", carrera.nombre_carrera)
        carrera.competidores = []

        for item in request.json["competidores"]:
            probabilidad = float(item["probabilidad"])
            cuota = round((probabilidad / (1 - probabilidad)), 2)
            competidor = Competidor(nombre_competidor=item["competidor"],
                                    probabilidad=probabilidad,
                                    cuota=cuota,
                                    id_carrera=carrera.id)
            carrera.competidores.append(competidor)

        db.session.commit()
        return carrera_schema.dump(carrera)

    @jwt_required()
    def delete(self, id_carrera):
        carrera = Carrera.query.get_or_404(id_carrera)
        db.session.delete(carrera)
        db.session.commit()
        return '', 204


class VistaApuestas(Resource):

    @jwt_required()
    def post(self):
        print("NOMBRE: ")
        print(request.json["nombre_apostador"])
        apostador=Apostador.query.get_or_404(request.json["id_apostador"])
        nueva_apuesta = Apuesta(valor_apostado=request.json["valor_apostado"],
                                nombre_apostador=apostador.nombre_apostador,
                                id_competidor=request.json["id_competidor"], 
                                id_carrera=request.json["id_carrera"], 
                                id_apostador=request.json["id_apostador"] )
        db.session.add(nueva_apuesta)
        db.session.commit()
        return apuesta_schema.dump(nueva_apuesta)

    @jwt_required()
    def get(self):
        return [apuesta_schema.dump(ca) for ca in Apuesta.query.all()]


class VistaApuesta(Resource):

    @jwt_required()
    def get(self, id_apuesta):
        return apuesta_schema.dump(Apuesta.query.get_or_404(id_apuesta))

    @jwt_required()
    def put(self, id_apuesta):
        apostador=Apostador.query.get_or_404(request.json["id_apostador"])
        apuesta = Apuesta.query.get_or_404(id_apuesta)
        apuesta.valor_apostado = request.json.get("valor_apostado", apuesta.valor_apostado)
        apuesta.nombre_apostador = apostador.nombre_apostador  #request.json.get("nombre_apostador", apuesta.nombre_apostador)
        apuesta.id_competidor = request.json.get("id_competidor", apuesta.id_competidor)
        apuesta.id_carrera = request.json.get("id_carrera", apuesta.id_carrera)
        apuesta.id_apostador = request.json.get("id_apostador", apuesta.id_apostador)
        db.session.commit()
        return apuesta_schema.dump(apuesta)

    @jwt_required()
    def delete(self, id_apuesta):
        apuesta = Apuesta.query.get_or_404(id_apuesta)
        db.session.delete(apuesta)
        db.session.commit()
        return '', 204


class VistaTerminacionCarrera(Resource):

    def put(self, id_competidor):
        competidor = Competidor.query.get_or_404(id_competidor)
        competidor.es_ganador = True
        carrera = Carrera.query.get_or_404(competidor.id_carrera)
        carrera.abierta = False

        for apuesta in carrera.apuestas:
            if apuesta.id_competidor == competidor.id:
                apuesta.ganancia = apuesta.valor_apostado + (apuesta.valor_apostado/competidor.cuota)
            else:
                apuesta.ganancia = 0

        db.session.commit()
        return competidor_schema.dump(competidor)


class VistaReporte(Resource):

    @jwt_required()
    def get(self, id_carrera):
        carreraReporte = Carrera.query.get_or_404(id_carrera)
        ganancia_casa_final = 0

        for apuesta in carreraReporte.apuestas:
            ganancia_casa_final = ganancia_casa_final + apuesta.valor_apostado - apuesta.ganancia

        reporte = dict(carrera=carreraReporte, ganancia_casa=ganancia_casa_final)
        schema = ReporteSchema()
        return schema.dump(reporte)
