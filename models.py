import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

database_name = "assetmanagement"
database_path = "postgresql://localhost:5432/{}".format(database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
	migrate = Migrate(app, db)
	app.config["SQLALCHEMY_DATABASE_URI"] = database_path
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	db.app = app
	db.init_app(app)
	db.create_all()

'''
PortfolioComposition
	association table between Portfolio and Security
'''
class PortfolioComposition(db.Model):
    __tablename__ = 'portfolio_composition'

    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), primary_key=True)
    security_id = db.Column(db.Integer, db.ForeignKey('security.id'), primary_key=True)
    weight = db.Column(db.Integer, nullable=False)

    security = db.relationship("Security")

'''
Portfolios
'''
class Portfolio(db.Model):
  __tablename__ = 'portfolio'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False, unique=True)

  securities = db.relationship("PortfolioComposition")

'''
Securities
'''
class Security(db.Model):
  __tablename__ = 'security'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False, unique=True)
  region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
  asset_class_id = db.Column(db.Integer, db.ForeignKey('assetClass.id'), nullable=False)

  region = db.relationship("Region")
  asset_class = db.relationship("AssetClass")

'''
AssetClass
'''
class AssetClass(db.Model):
  __tablename__ = 'assetClass'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False, unique=True)

'''
Region
'''
class Region(db.Model):
  __tablename__ = 'region'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False, unique=True)
