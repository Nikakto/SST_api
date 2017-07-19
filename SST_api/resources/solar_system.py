from SST_api import db
from flask_restful import reqparse, Resource

from SST_api.models.location import SolarSystem

# create request parser
parser = reqparse.RequestParser()
parser.add_argument('id', type=str, location='args')
parser.add_argument('name', type=str, location='args')
parser.add_argument('security', type=float, location='args')
parser.add_argument('region', type=int, location='args')

# api/solar_system
class SolarSystemList(Resource):
    ''' api for solar system list
    '''

    def get(self):
        ''' Return list of exists solar systems
        '''
        
            #read args
        args = parser.parse_args()
        
            # create criterion by filters for signature list
        filters = {'id': args.id,
                   'name': args.name,
                   'region': args.region}
            
            #try read signatures by filters
        try:
            solar_systems_as_list = SolarSystem.query.filter(SolarSystem.criterion(filters)).all()
        
            # catch errors
        except Exception as err:
            return {err}, 404
        
            # if no errors
        else:
            
                #convert signatures list to dict (json format)
            solar_systems_as_dict = {}
            for solar_system in solar_systems_as_list:
                solar_systems_as_dict[solar_system.id] = solar_system.as_dict()
    
                #return json
            return solar_systems_as_dict, 200

# api/system/<int:solar_system_id>
class SolarSystemId(Resource):
    ''' api for solar system by id
    '''
    
    def get(self, solar_system_id):
        ''' return data for solar system
        '''
        
            #read args
        args = parser.parse_args()
        
            # create criterion by filters for signature list
        filters = {'id': None,
                   'name': args.name,
                   'region': args.region}
            
            #try read signatures by filters
        try:
            solar_system = SolarSystem.query.filter(SolarSystem.id == solar_system_id,
                                                    SolarSystem.criterion(filters)).one()
        
            # catch errors
        except Exception as err:
            return {err}, 404
        
            # if no errors
        else:
            return {solar_system.id: solar_system.as_dict()}, 200
    
    def post(self, solar_system_id):
        ''' create new solar system in database
        '''
        
            # read args
        args = parser.parse_args()
        
            # create solar system
        solar_system_new = SolarSystem(solar_system_id, 
                                       args.name, 
                                       args.security, 
                                       args.region
                                       )
        
            # check valid
        if not solar_system_new.is_valid():
            return {'ERROR': 'Solar system is not valid'}, 404
            
            # try create
        try:
            db.session.add(solar_system_new)
            db.session.commit()
            
            # except error
        except Exception as err:
            db.session.rollback()
            return 'Error: %s' %err, 404
        
            # if no error
        else:
            return {solar_system_new.id: solar_system_new.as_dict()}, 201