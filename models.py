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

    security = db.relationship("Security", backref="portfolio_composition")

    def format(self):
    	return {
    		'security_name': self.security.name,
    		'region': self.security.region.name,
    		'asset_class': self.security.asset_class.name,
    		'weight': self.weight
    	}

'''
Portfolios
'''
class Portfolio(db.Model):
	__tablename__ = 'portfolio'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)

	portfolio_compositions = db.relationship("PortfolioComposition", backref="portfolio")

	def format(self):
	    return {
			'portfolio_id': self.id,
			'portfolio_name': self.name,
			'portfolio_compositions': [portfolio_composition.format() for portfolio_composition in self.portfolio_compositions]
	    }

'''
Securities
'''
class Security(db.Model):
	__tablename__ = 'security'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)
	region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
	asset_class_id = db.Column(db.Integer, db.ForeignKey('assetClass.id'), nullable=False)

	region = db.relationship("Region", backref="security")
	asset_class = db.relationship("AssetClass", backref="security")

	def format(self):
		return {
			'security_id': self.id,
			'security_name': self.name,
			'region': self.region.name,
			'asset_class': self.asset_class.name
	    }


'''
AssetClass
'''
class AssetClass(db.Model):
	__tablename__ = 'assetClass'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)

	def format(self):
		return {
			'asset_class_id': self.id,
			'asset_class': self.name,
	    }

'''
Region
'''
class Region(db.Model):
	__tablename__ = 'region'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)

	def format(self):
		return {
			'region_id': self.id,
			'region': self.name,
	    }
