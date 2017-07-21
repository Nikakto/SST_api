from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# create app and api
app = Flask(__name__)
api = Api(app)

# config database and create models
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# import db models and pages
from SST_api import models, views

# api moduls
from SST_api.resources.signature import *
from SST_api.resources.signature_name import *
from SST_api.resources.signature_type import *
from SST_api.resources.solar_system import *
from SST_api.resources.region import *

# add api resources

    # region
api.add_resource(RegionList, '/api/region', '/api/region/')
api.add_resource(RegionId, '/api/region/<int:region_id>')

    # solar system
api.add_resource(SolarSystemList, '/api/solar_system', '/api/solar_system/')
api.add_resource(SolarSystemId, '/api/solar_system/<int:solar_system_id>')

    # signature
api.add_resource(SignatureApi, 
                '/api/solar_system/<int:solar_system_id>/signature',
                '/api/solar_system/<int:solar_system_id>/signature/'
                )

    # signature name
api.add_resource(SignatureNameApi, 
                '/api/signature_name',
                '/api/signature_name/'
                )

    # signature type
api.add_resource(SignatureTypeApi, 
                '/api/signature_type',
                '/api/signature_type/'
                )