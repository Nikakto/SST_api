from SST_api import db

#from SST_api.models.signature import Signature

class SolarSystem(db.Model):
    __tablename__ = 'solar_systems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    security = db.Column(db.Float)
    
    signatures = db.relationship('Signature', 
                                 backref = 'location', lazy = 'dynamic')
    
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<%r (id: %r)' % (self.name, self.id)