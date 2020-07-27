import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import json 

from models import setup_db, db, Portfolio, Security, PortfolioComposition, AssetClass, Region
from auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/portfolios', methods=['GET'])
    @requires_auth('get:portfolios')
    def retrieve_portfolios(payload):
        portfolios = Portfolio.query.order_by(Portfolio.id).all()
        portfolios_formatted = [portfolio.format() for portfolio in portfolios]

        if len(portfolios_formatted) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'portfolios': portfolios_formatted
        })

    @app.route('/portfolios/<int:portfolio_id>',methods = ['GET'])
    @requires_auth('get:portfolios')
    def retrieve_portfolio(payload, portfolio_id):

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
    @requires_auth('post:portfolios')
    def create_portfolio(payload):

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

    @app.route('/portfolios/<int:portfolio_id>', methods=['DELETE'])
    @requires_auth('delete:portfolios')
    def delete_portfolio(payload, portfolio_id):
        portfolio = Portfolio.query.get(portfolio_id)

        if portfolio is None:
            abort(404)

        db.session.delete(portfolio)
        db.session.commit()

        return jsonify({
            'success': True,
            'deleted': portfolio_id
        })

    @app.route('/portfolios/<int:portfolio_id>',  methods=['PATCH'])
    @requires_auth('patch:portfolios')
    def update_portfolio(payload, portfolio_id):
        body = request.get_json()
        new_name = body.get('portfolio_name', None)
        new_portfolio_compositions = body.get('portfolio_compositions', None)
        
        portfolio = Portfolio.query.get(portfolio_id)

        if portfolio is None:
            abort(404)

        if new_name is not None:
            portfolio.name = new_name
        if new_portfolio_compositions is not None:
            # check if portfolio compositions sum up to 100 %
            total_weight = 0
            for portfolio_composition in new_portfolio_compositions:
                total_weight += portfolio_composition['weight']
            if total_weight != 100:
                abort(422)

            # delete the current compositions
            PortfolioComposition.query.filter_by(portfolio_id=portfolio_id).delete()

            # add new compositions
            for portfolio_composition in new_portfolio_compositions:
                composition = PortfolioComposition(security_id=portfolio_composition['security_id'], weight=portfolio_composition['weight'])
                composition.portfolio = portfolio
                db.session.add(composition)

            db.session.commit()

        return jsonify({
            'success': True,
            'updated': portfolio_id
        }), 200

    @app.route('/securities', methods=['GET'])
    @requires_auth('get:securities')
    def retrieve_securities(payload):

        securities = Security.query.order_by(Security.id).all()
        securities_formatted = [security.format() for security in securities]

        if len(securities_formatted) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'securities': securities_formatted
        })


    @app.route('/securities/<int:security_id>',methods = ['GET'])
    @requires_auth('get:securities')
    def retrieve_security(payload, security_id):

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
    @requires_auth('post:securities')
    def create_security(payload):

        body = request.get_json()
        security_name = body.get('security_name', None)
        region_id = body.get('region_id', None)
        asset_class_id = body.get('asset_class_id', None)

        if Region.query.get(region_id) == None or AssetClass.query.get(asset_class_id) == None:
            abort(422)

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

    @app.route('/securities/<int:security_id>', methods=['DELETE'])
    @requires_auth('delete:securities')
    def delete_security(payload, security_id):
        security = Security.query.get(security_id)

        if security is None:
            abort(404)

        # check if the security is in any of the existing portfolios
        if PortfolioComposition.query.filter_by(security_id=security_id).count() > 0:
            abort(422)

        db.session.delete(security)
        db.session.commit()

        return jsonify({
            'success': True,
            'deleted': security_id
        })

    @app.route('/securities/<int:security_id>',  methods=['PATCH'])
    @requires_auth('patch:securities')
    def update_security(payload, security_id):
        body = request.get_json()
        new_name = body.get('security_name', None)
        new_region_id = body.get('region_id', None)
        new_asset_class_id = body.get('asset_class_id', None)
        security = Security.query.get(security_id)

        if security is None:
            abort(404)

        if Region.query.get(new_region_id) == None or AssetClass.query.get(new_asset_class_id) == None:
            abort(422)

        if new_name is not None:
            security.name = new_name
        if new_region_id is not None:
            security.region_id = new_region_id
        if new_asset_class_id is not None:
            security.asset_class_id = new_asset_class_id

        db.session.commit()

        return jsonify({
            'success': True,
            'updated': security_id
        }), 200

    @app.route('/asset_classes', methods=['GET'])
    def retrieve_asset_classes():

        asset_classes = AssetClass.query.order_by(AssetClass.id).all()
        asset_classes_formatted = [asset_class.format() for asset_class in asset_classes]

        if len(asset_classes_formatted) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'asset_classes': asset_classes_formatted
        })

    @app.route('/regions', methods=['GET'])
    def retrieve_regions():

        regions = Region.query.order_by(Region.id).all()
        regions_formatted = [region.format() for region in regions]

        if len(regions_formatted) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'regions': regions_formatted
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

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'authentification failed'
        }), 401

    return app

app = create_app()

if __name__ == '__main__':
    app.run()

