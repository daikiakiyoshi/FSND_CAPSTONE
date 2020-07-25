import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Portfolio, Security

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

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404


if __name__ == '__main__':
    app.run()



