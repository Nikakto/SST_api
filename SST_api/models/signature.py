from SST_api import db
from flask_sqlalchemy import sqlalchemy

#from SST_api.models.location import SolarSystem

class Signature(db.Model):
    __tablename__ = 'signatures'
    
    id = db.Column(db.Integer, primary_key=True)
    
    solar_system_id = db.Column(db.Integer, db.ForeignKey('solar_systems.id'))
    code = db.Column(db.String(7))
    
    type_id = db.Column(db.Integer, db.ForeignKey('signatures_types.id'))
    name_id = db.Column(db.Integer, db.ForeignKey('signatures_names.id'))

    def __init__(self, systemID, code, type_id, name_id):
        
            # easy vars
        self.solar_system_id = systemID
        self.code = code
        
            # type_id cannot be null (default 1)
        if type_id:
            self.type_id = type_id
        else:
            self.type_id = 1
            
            # name_id cannot be null (default 2)
        if name_id:
            self.name_id = name_id
        else:
            self.name_id = 2

    def __repr__(self):
        return '<systemID=%r; code=%r>' % (self.solar_system_id, self.code)
    
    def as_dict(self):
        ''' Return models data as dict
        '''
        
        data = {'solar_system_id': self.solar_system_id,
                'code': self.code,
                'type': self.type_id,
                'name': self.name_id,
                }
        
        return data
    
    def criterion(filters):            
        ''' return <criterion> for sql.query.filter(<criterion>) by filters dict
        '''
        
            # empty filters list
        comporators = []
        
            # filter by solar system
        if filters['solar_system_id']:
            comporators.append( Signature.solar_system_id.op('=')(filters['solar_system_id']) )
            
            # filter by codes
        if filters['code']:
            comporators.append( Signature.code.in_(filters['code'].split(',')) )
            
            # filter by type
        if filters['type']:
            comporators.append( Signature.type_id.op('=')(filters['type']) )
            
            # filter by name
        if filters['name']:
            comporators.append( Signature.name_id.op('=')(filters['name']) )
            
        return sqlalchemy.sql.and_( * [comporator for comporator in comporators])
    
    def is_valid(self):
        ''' Return True if signature data is valid
        '''
        
            # check solar system
        if not(self.solar_system_id>0):
            print('Signature: Solar system error')
            return False
        
            # check code
        code_parts = self.code.split('-')
        if isinstance(code_parts, list) and len(code_parts) == 2:
            
                # get part nums and chars
            chars = code_parts[0]
            nums = code_parts[1]
            
                # if nums isn't only nums and chars isn't only chars
            if not (nums.isdigit() and chars.isalpha()):
                print('Signature: Code error parts')
                return False
            
        else:
            print('Signature: Code error')
            return False
        
            # check type (it should be none or bigger then zero)
        if not (self.type_id==None or self.type_id>0):
            print('Signature: type error')
            return False
        
            # check name (it should be none or bigger then zero)
        if not (self.name_id==None or self.name_id>0):
            print('Signature: name error')
            return False
        
            # checked
        return True
    
class SignatureType(db.Model):
    __tablename__ = 'signatures_types'
    
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(20))
    
    def __init__(self, type_id):
        self.id = type_id

    def __repr__(self):
        return '<Table: signatures_types; id: %s; English: %r>' % (self.id, self.english)
    
class SignatureName(db.Model):
    __tablename__ = 'signatures_names'
    
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(20))
    
    def __init__(self, name_id):
        self.id = name_id

    def __repr__(self):
        return '<Table: signature_name; id: %s; English: %r>' % (self.id, self.english)