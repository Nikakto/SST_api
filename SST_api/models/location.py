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
    
    def __init__(self, id):
        self.id = id

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
                    'region_id': self.region_id,
                    'region_url': '/api/region/%s' % self.region_id,
                    },
                }
        
        return data
    
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
            comporators.append( SolarSystem.name.op('=')(filters['name']) )
            
            # filter by region
        if filters['region'] != None:
            comporators.append( SolarSystem.region_id.op('=')(filters['region']) )
            
        return sqlalchemy.sql.and_( * [comporator for comporator in comporators])