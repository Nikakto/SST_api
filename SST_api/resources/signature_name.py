from SST_api import db
from flask_restful import reqparse, Resource

from SST_api.models.signature import SignatureName

# create request parser
parser = reqparse.RequestParser()

# static arguments   
parser.add_argument('id', type=str, location='args')   
parser.add_argument('name', type=str, location='args')

# /api/signature_name
class SignatureNameApi(Resource):
    ''' api for list of signature names
    '''
    
    def get(self):
        ''' Return list of signatures for solar system by filters
        '''
        
            #read args
        args = parser.parse_args()
        
            # create criterion by filters for signature list
        filters = {'id': args.id,
                   'english': args.name,
                   }
            
            #try read signatures by filters
        try:
            names_as_list = SignatureName.query.filter(SignatureName.criterion(filters)).all()
        
            # catch errors
        except Exception as err:
            return {err}, 404
        
            # if no errors
        else:
            
                #convert signatures list to dict (json format)
            names_as_dict = {}
            for name in names_as_list:
                names_as_dict[name.id] = name.as_dict()
    
                #return json request
            return names_as_dict, 200
    
    def post(self):
        ''' create new signature in database
        '''
        
            # read args
        args = parser.parse_args()
        
            # check code exist
        if args.name == None:
            return {'ERROR': 'Required signature name to create'}

        # create new name for signature
        name_new = SignatureName(args.name)
                
        if name_new.is_valid():
            
                # try create all
            try:
                db.session.add(name_new)
                db.session.commit()
                
                # except error
            except Exception as err:
                db.session.rollback()
                return 'Error: %s' %err, 404
            
                # if no error
            else:
                return name_new.as_dict(), 201
            
        else:
            return {'Error': 'No any valid signatures'}, 404
    
    def put(self):
        ''' update exist signature
        '''
        
            # read args
        args = parser.parse_args()
        
            # check code exist
        if args.id == None or args.name == None:
            return {'ERROR': 'Not enough arguments'}
        
            # get filter to find signature
        filters = {'id': args.id,
                   'english': None
                   }
        
        try:
            sig_name = SignatureName.query.filter(SignatureName.criterion(filters)).one()
        
            # catch errors
        except Exception as err:
            return {err}, 204
        else: 
            if args.name:
                sig_name.english = args.name
            
            try:
                db.session.commit()
                
            except Exception as err:
                db.session.rollback()
                return {err}, 204
            
            else:
                return {sig_name.id: sig_name.as_dict()}, 200