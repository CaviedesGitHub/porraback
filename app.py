from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from modelos import db
from vistas import VistaApuestas, VistaApuesta, VistaSignIn, VistaLogIn, VistaCarrerasUsuario, \
    VistaCarrera, VistaTerminacionCarrera, VistaReporte
from vistas import VistaApostadores, VistaApostador
from vistas import VistaLogInApostador, VistaSignInApostador

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/laporra'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eporra.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaSignInApostador, '/signinApostador')
api.add_resource(VistaLogInApostador, '/loginApostador')
api.add_resource(VistaCarrerasUsuario, '/usuario/<int:id_usuario>/carreras')
api.add_resource(VistaCarrera, '/carrera/<int:id_carrera>')
api.add_resource(VistaApuestas, '/apuestas')
api.add_resource(VistaApuesta, '/apuesta/<int:id_apuesta>')
api.add_resource(VistaTerminacionCarrera, '/carrera/<int:id_competidor>/terminacion')
api.add_resource(VistaReporte, '/carrera/<int:id_carrera>/reporte')

api.add_resource(VistaApostadores, '/apostadores')
api.add_resource(VistaApostador, '/apostador/<int:id_apostador>')

jwt = JWTManager(app)
