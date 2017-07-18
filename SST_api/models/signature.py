from SST_api import db
from flask_sqlalchemy import sqlalchemy

from SST_api.models.location import SolarSystem

class Signature(db.Model):
    __tablename__ = 'signatures'
    
    id = db.Column(db.Integer, primary_key=True)
    
    solar_system_id = db.Column(db.Integer, db.ForeignKey('solar_systems.id'))
    code = db.Column(db.String(7))
    
    type_id = db.Column(db.Integer, db.ForeignKey('signatures_types.id'), default=1)
    name_id = db.Column(db.Integer, db.ForeignKey('signatures_names.id'), default=2)
    
    created = db.Column(db.DateTime, server_default=sqlalchemy.text("default"))
    checked = db.Column(db.DateTime, server_default=sqlalchemy.text("default"))

    def __init__(self, systemID, code, type_id=1, name_id=2):
        
            # easy vars
        self.solar_system_id = systemID
        self.code = code
        self.type_id = type_id
        self.name_id = name_id

    def __repr__(self):
        return '<systemID=%r; code=%r>' % (self.solar_system_id, self.code)
    
    def as_dict(self):
        ''' Return models data as dict
        '''

        data = {'solar_system:': {
                    'solar_system_id': self.solar_system_id,
                    'solar_system_url': '/api/solar_system/%s' % self.solar_system_id,
                    },
                'code': self.code,
                'type': self.type_id,
                'name_id': self.name_id,
                'name': 'NONAME',
                'created': str(self.created),
                'checked': str(self.checked),
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
        if filters['code'] != None:
            comporators.append( Signature.code.in_(filters['code'].split(',')) )
            
            # filter by type
        if filters['type'] != None:
            comporators.append( Signature.type_id.op('=')(filters['type']) )
            
            # filter by name
        if filters['name'] != None:
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
            
                # len of nums and chars parts should be 3
            if len(chars)!=3 or len(nums)!=3:
                return False
            
                # if nums isn't only nums and chars isn't only chars
            if not (nums.isdigit() and chars.isalpha()):
                return False
            
        else:
            return False
        
            # check type (it should be none or bigger then zero)
        if not (self.type_id==None or self.type_id>0):
            return False
        
            # check name (it should be none or bigger then zero)
        if not (self.name_id==None or self.name_id>0):
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