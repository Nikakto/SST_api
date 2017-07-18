from flask_restful import reqparse, Resource
from flask_cache.backends import null

from SST_api.models.location import SolarSystem

# create request parser
parser = reqparse.RequestParser()
parser.add_argument('id', type=str, location='args')
parser.add_argument('name', type=str, location='args')
parser.add_argument('security', type=float, location='args')
parser.add_argument('region', type=int, location='args')

# api/system
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
    
    def post(self, solar_system_id):
        ''' create new solar system
        '''

        args = parser.parse_args()
        return {'solar_system': {'id': solar_system_id,
                                 'name': args.name,
                                'security': args.security,
                                'region_id': args.region,
                                'region_url': '/region/%s' %args.region,
                                }
                }, 201

class SolarSystemName(Resource):
    ''' api for solar system by name
    '''

    def get(self, solar_system_name):
        ''' return information for solar system by name
        '''
        
        args = parser.parse_args()
        return {'solar_system': {'id': 0,
                                 'name': solar_system_name,
                                 'security': -1,
                                 'region_id': 0,
                                 'region_url': '/region/',
                                 }
                }, 200
    