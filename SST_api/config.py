import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://admin:admin@localhost:3306/evesst_database'
SQLALCHEMY_TRACK_MODIFICATIONS = False