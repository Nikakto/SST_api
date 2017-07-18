from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# create app and api
app = Flask(__name__)
api = Api(app)

# config database and create models
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
from SST_api import models

from SST_api.resources.signature import *
from SST_api.resources.solar_system import *
# add api resources

    # region

    # solar system
api.add_resource(SolarSystemList, '/api/solar_system', '/api/solar_system/')
api.add_resource(SolarSystemId, '/api/solar_system/<int:solar_system_id>')
api.add_resource(SolarSystemName, '/api/solar_system/<string:solar_system_name>')

    # signature
api.add_resource(SignatureListBySolarSystem, 
                '/api/solar_system/<int:solar_system_id>/signature',
                '/api/solar_system/<int:solar_system_id>/signature/'
                )
api.add_resource(SignatureBySolarSystem, 
                 '/api/solar_system/<int:solar_system_id>/signature=[<string:code_as_str>]')