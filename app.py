import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json 

from models import setup_db, db, Portfolio, Security, PortfolioComposition

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)

  setup_db(app)
  CORS(app)

  return app

app = create_app()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/portfolios', methods=['GET'])
def retrieve_portfolios():

    portfolios = Portfolio.query.order_by(Portfolio.id).all()
    portfolios_formatted = [portfolio.format() for portfolio in portfolios]

    if len(portfolios_formatted) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'portfolios': portfolios_formatted
    })


@app.route('/portfolios/<int:portfolio_id>',methods = ['GET'])
def retrive_portfolio(portfolio_id):

	portfolio = Portfolio.query.get(portfolio_id)

	if portfolio is None:
   		abort(404)

	return jsonify({
        'success': True,
        'portfolio_id': portfolio.id,
        'portfolio_name': portfolio.name,
        'portfolio_compositions': [portfolio_composition.format() for portfolio_composition in portfolio.portfolio_compositions]
	})

@app.route('/portfolios',methods = ['POST'])
def create_portfolio():

	body = request.get_json()
	portfolio_name = body.get('portfolio_name', None)
	portfolio_compositions = body.get('portfolio_compositions', None)

	# check if portfolio compositions sum up to 100 %
	total_weight = 0
	for portfolio_composition in portfolio_compositions:
		total_weight += portfolio_composition['weight']
	if total_weight != 100:
		abort(422)

	portfolio = Portfolio(name=portfolio_name)

	for portfolio_composition in portfolio_compositions:
		composition = PortfolioComposition(security_id=portfolio_composition['security_id'], weight=portfolio_composition['weight'])
		composition.portfolio = portfolio
		db.session.add(composition)

	db.session.commit()

	return jsonify({
        'success': True,
        'portfolio_id': portfolio.id,
        'portfolio_name': portfolio.name,
	})

@app.route('/securities', methods=['GET'])
def retrieve_securities():

    securities = Security.query.order_by(Security.id).all()
    securities_formatted = [security.format() for security in securities]

    if len(securities_formatted) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'securities': securities_formatted
    })


@app.route('/securities/<int:security_id>',methods = ['GET'])
def retrive_security(security_id):

	security = Security.query.get(security_id)

	if security is None:
   		abort(404)

	return jsonify({
        'success': True,
        'security_id': security.id,
        'security_name': security.name,
        'asset_class': security.asset_class.name,
        'region': security.region.name
	})

@app.route('/securities',methods = ['POST'])
def create_security():

	body = request.get_json()
	security_name = body.get('security_name', None)
	region_id = body.get('region_id', None)
	asset_class_id = body.get('asset_class_id', None)

	security = Security(name=security_name, region_id=region_id, asset_class_id=asset_class_id)

	db.session.add(security)
	db.session.commit()

	return jsonify({
        'success': True,
        'security_id': security.id,
        'security_name': security.name,
        'region': security.region.name,
        'asset_class': security.asset_class.name,
	})

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404

@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable entity"
    }), 422


if __name__ == '__main__':
    app.run()



