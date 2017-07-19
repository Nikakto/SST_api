from SST_api import db
from flask_sqlalchemy import sqlalchemy

class SolarSystem(db.Model):
    __tablename__ = 'solar_systems'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    security = db.Column(db.Float, default=-1)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    
    signatures = db.relationship('Signature', 
                                 backref = 'location', lazy = 'dynamic')
    
    def __init__(self, id, name, security, region_id):
        self.id = id
        self.name = name
        self.security = security
        self.region_id = region_id

    def __repr__(self):
        return '<%r (id: %r)' % (self.name, self.id)
    
    def as_dict(self):
        ''' Return models data as dict
        '''
        
        data = {'id': self.id,
                'name': self.name,
                'security': self.security,
                'url': '/api/solar_system/%s' % self.id,
                'region': {
                    'id': self.region_id,
                    'url': '/api/region/%s' % self.region_id,
                    },
                }
        
        return data
    
    def is_valid(self):
        ''' Return true if self.data is valid
        '''
        
            # check id
        if self.id not in range(30000000, 32000000):
            print('solar system: id error')
            return False
    
            # check region
        if self.region_id not in range(10000000, 12000000):
            print('solar system: region id error')
            return False
        
            # check sec and name
        if self.security == None or self.name == None:
            print('solar system: sec or name error')
            return False
        
            # solar system is valid
        return True
    
    def criterion(filters):            
        ''' return <criterion> for sql.query.filter(<criterion>) by filters dict
        '''
        
            # empty filters list
        comporators = []
            
            # filter by solar system id
        if filters['id'] != None:
            comporators.append( SolarSystem.id.in_(filters['id'].split(',')) )
            
            # filter by name
        if filters['name'] != None:
            comporators.append( SolarSystem.name.in_(filters['name'].split(',')) )
            
            # filter by region
        if filters['region'] != None:
            comporators.append( SolarSystem.region_id.op('=')(filters['region']) )
            
        return sqlalchemy.sql.and_( * [comporator for comporator in comporators])
    
class Region(db.Model):
    __tablename__ = 'regions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<region: %r (id: %r)' % (self.name, self.id)