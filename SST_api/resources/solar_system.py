from flask_restful import reqparse, Resource
from flask_cache.backends import null

# create request parser
parser = reqparse.RequestParser()
parser.add_argument('name', type=int, location='args')
parser.add_argument('security', type=float, location='args')
parser.add_argument('region', type=int, location='args')

# api/system
class SolarSystemList(Resource):
    ''' api for solar system list
    '''

    def get(self):
        ''' Return list of exists solar systems
        '''
        
        return {'solar_system0': {'id': 0,
                                  'name': 'Jita',
                                  },
                'solar_system1': {'id': 1,
                                  'name': 'Nomoa',
                                  },
                }, 200

# api/system/<int:solar_system_id>

class SolarSystemId(Resource):
    ''' api for solar system by id
    '''
    
    def get(self, solar_system_id):
        ''' return data for solar system
        '''
        
        args = parser.parse_args()
        return {'solar_system': {'id': solar_system_id,
                                 'name': args.name,
                                 'security': args.security,
                                 'region_id': args.region,
                                 'region_url': '/region/%s' %args.region,
                                 }
                }, 200
    
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
    