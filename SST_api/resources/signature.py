from SST_api import db
from flask_restful import reqparse, Resource

from SST_api.models.signature import Signature

# create request parser
parser = reqparse.RequestParser()

# static arguments   
parser.add_argument('code', type=str, location='args')   
parser.add_argument('type', type=int, location='args')
parser.add_argument('name', type=int, location='args')

# /api/solar_system/<int:solar_system_id>/signature/
class SignatureApi(Resource):
    ''' api for list of signatures in solar system
    '''
    
    def get(self, solar_system_id):
        ''' Return list of signatures for solar system by filters
        '''
        
            #read args
        args = parser.parse_args()
        
            # create criterion by filters for signature list
        filters = {'solar_system_id': solar_system_id,
                   'code': args.code,
                   'type': args.type,
                   'name': args.name}
            
            #try read signatures by filters
        try:
            signatures_as_list = Signature.query.filter(Signature.criterion(filters)).all()
        
            # catch errors
        except Exception as err:
            return {err}, 404
        
            # if no errors
        else:
            
                #convert signatures list to dict (json format)
            signatures_as_dict = {}
            for signature in signatures_as_list:
                signatures_as_dict[signature.code] = signature.as_dict()
    
                #return json request
            return signatures_as_dict, 200
    
    def post(self, solar_system_id):
        ''' create new signature in database
        '''
        
            # read args
        args = parser.parse_args()
        
            # check code exist
        if args.code == None:
            return {'ERROR': 'Required signature code for update'}

        # create new valid signature for each code
        signatures_as_list = []
        
        for each_code in args.code.split(','):
            signature_new = Signature(solar_system_id, each_code, args.type, args.name)
            if signature_new.is_valid():
                signatures_as_list.append(signature_new)
                
        if len(signatures_as_list) in range(1,30):
            
                # try create all
            try:
                db.session.add_all(signatures_as_list)
                db.session.commit()
                
                # except error
            except Exception as err:
                db.session.rollback()
                return 'Error: %s' %err, 404
            
                # if no error
            else:
                
                    #convert signatures list to dict (json format)
                signatures_as_dict = {}
                for signature in signatures_as_list:
                    signatures_as_dict[signature.code] = signature.as_dict()
        
                    #return json request
                return signatures_as_dict, 201
            
        else:
            return {'Error': 'No any valid signatures'}, 404
    
    def put(self, solar_system_id):
        ''' update exist signature
        '''
        
            # read args
        args = parser.parse_args()
        
            # check code exist
        if args.code == None:
            return {'ERROR': 'Required signature code for update'}
        
            # get filter to find signature
        filters = {'solar_system_id': solar_system_id,
                   'code': args.code,
                   'type': None,
                   'name': None
                   }
        
        try:
            signature = Signature.query.filter(Signature.criterion(filters)).one()
        
            # catch errors
        except Exception as err:
            return {err}, 204
        else:
            
            if args.type:
                signature.type_id = args.type
                
            if args.name:
                signature.name_id = args.name
            
            try:
                db.session.commit()
                
            except Exception as err:
                db.session.rollback()
                return {err}, 204
            
            else:
                return {signature.code: signature.as_dict()}, 200