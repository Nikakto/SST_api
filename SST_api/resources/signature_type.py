from SST_api import db
from flask_restful import reqparse, Resource

from SST_api.models.signature import SignatureType

# create request parser
parser = reqparse.RequestParser()

# static arguments   
parser.add_argument('id', type=str, location='args')   
parser.add_argument('name', type=str, location='args')

# /api/signature_type
class SignatureTypeApi(Resource):
    ''' api for list of signature types
    '''
    
    def get(self):
        ''' Return list of signature types by filters
        '''
        
            #read args
        args = parser.parse_args()
        
            # create criterion by filters for signature list
        filters = {'id': args.id,
                   'name': args.name,
                   }
            
            #try read signature types by filters
        try:
            sig_types_as_list = SignatureType.query.filter(SignatureType.criterion(filters)).all()
        
            # catch errors
        except Exception as err:
            return {err}, 404
        
            # if no errors
        else:
            
                #convert signature types list to dict (json format)
            sig_types_as_dict = {}
            for sig_type in sig_types_as_list:
                sig_types_as_dict[sig_type.id] = sig_type.as_dict()
    
                #return json request
            return sig_types_as_dict, 200