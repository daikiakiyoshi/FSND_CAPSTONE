import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "assetmanagement"
database_path = "postgresql://localhost:5432/{}".format(database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Portfolios
'''
class Portfolios(db.Model):
  __tablename__ = 'portfolios'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  security = Column(Integer)
  weight = Column(Integer)

'''
Securities
'''
class Securities(db.Model):
  __tablename__ = 'security'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  region = Column(Integer)
  asset_class = Column(Integer)
  weight = Column(Integer)

'''
AssetClass
'''
class AssetClass(db.Model):
  __tablename__ = 'assetClass'

  id = Column(Integer, primary_key=True)
  name = Column(String)

'''
Region
'''
class Region(db.Model):
  __tablename__ = 'region'

  id = Column(Integer, primary_key=True)
  name = Column(String)
