from SST_api import db
from flask_restful import reqparse, Resource

from SST_api.models.location import Region

# create request parser
parser = reqparse.RequestParser()
parser.add_argument('id', type=str, location='args')
parser.add_argument('name', type=str, location='args')

# /api/region
class RegionList(Resource):
    ''' api for regions list
    '''

    def get(self):
        ''' Return list of exists regions
        '''
        
            #read args
        args = parser.parse_args()
        
            # create criterion by filters for region list
        filters = {'id': args.id,
                   'name': args.name,
                   }
            
            #try read regions by filters
        try:
            regions_as_list = Region.query.filter(Region.criterion(filters)).all()
        
            # catch errors
        except Exception as err:
            return {err}, 404
        
            # if no errors
        else:
            
                #convert regions list to dict (json format)
            regions_as_dict = {}
            for region in regions_as_list:
                regions_as_dict[region.id] = region.as_dict()
    
                #return json
            return regions_as_dict, 200

# /api/region/<int:region_id>
class RegionId(Resource):
    ''' api for region by id
    '''
    
    def get(self, region_id):
        ''' return data for region by id
        '''
        
            #read args
        args = parser.parse_args()
        
            # create criterion by filters for region
        filters = {'id': None,
                   'name': args.name,
                   }
            
            #try read region by filters
        try:
            region = Region.query.filter(Region.id == region_id,
                                         Region.criterion(filters)).one()
        
            # catch errors
        except Exception as err:
            return {err}, 404
        
            # if no errors
        else:
            return {region.id: region.as_dict()}, 200
    
    def post(self, region_id):
        ''' create new region in database
        '''
        
            # read args
        args = parser.parse_args()
        
            # create region
        region_new = Region(region_id, 
                            args.name,
                            )
        
            # check valid
        if not region_new.is_valid():
            return {'ERROR': 'Region is not valid'}, 404
            
            # try create
        try:
            db.session.add(region_new)
            db.session.commit()
            
            # except error
        except Exception as err:
            db.session.rollback()
            return 'Error: %s' %err, 404
        
            # if no error
        else:
            return {region_new.id: region_new.as_dict()}, 201
