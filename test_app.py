import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db, Portfolio, Security, PortfolioComposition, AssetClass, Region


class AssetManagementSystemTestCase(unittest.TestCase):
    """This class represents the asset management system test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "assetmanagement_test"
        self.database_path = "postgresql://localhost:5432/{}".format(self.database_name)
        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_retrieve_portfolios(self):
        res = self.client().get('/portfolios')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['portfolios'])

    def test_retrieve_portfolio(self):
        res = self.client().get('/portfolios/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['portfolio_id'], 1)
        self.assertTrue(data['portfolio_name'])
        self.assertTrue(data['portfolio_compositions'])

    def test_404_retrieve_portfolio(self):
    	""" Test the case where portfolio_id does not exist """
        res = self.client().get('/portfolios/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")

    def test_create_portfolio(self):
    	new_portfolio = {"portfolio_name": "TEST_PORT", 
    					"portfolio_compositions": [{"security_id": 1, "weight": 60}, 
    												{"security_id": 2, "weight": 40}]}

        res = self.client().post('/portfolios', json=new_portfolio)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['portfolio_name'], "TEST_PORT")
        self.assertTrue(data['portfolio_id'])

    def test_422_create_portfolio(self):
    	""" Test the case where portfolio composition does not sum up to 100% """
    	new_portfolio = {"portfolio_name": "TEST_PORT2", 
    					"portfolio_compositions": [{"security_id": 1, "weight": 100}, 
    												{"security_id": 2, "weight": 100}]}

        res = self.client().post('/portfolios', json=new_portfolio)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable entity")

    def test_delete_portfolio(self):
    	portfolio_delete_id = 2
        res = self.client().delete('/portfolios/{}'.format(portfolio_delete_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], portfolio_delete_id)

    def test_delete_portfolio(self):
    	""" Test the case where portfolio_id does not exist """
    	portfolio_delete_id = 100
        res = self.client().delete('/portfolios/{}'.format(portfolio_delete_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")

    def test_update_portfolio(self):
    	update_portfolio = {"portfolio_name": "TEST_PORT3", 
    					"portfolio_compositions": [{"security_id": 1, "weight": 50}, 
    												{"security_id": 2, "weight": 50}]}
    	portfolio_update_id = 3
        res = self.client().patch('/portfolios/{}'.format(portfolio_update_id), json=update_portfolio)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], portfolio_update_id)

    def test_404_update_portfolio(self):
    	""" Test the case where portfolio_id does not exist """
    	update_portfolio = {"portfolio_name": "TEST_PORT3", 
    					"portfolio_compositions": [{"security_id": 1, "weight": 50}, 
    												{"security_id": 2, "weight": 50}]}
    	portfolio_update_id = 100
        res = self.client().patch('/portfolios/{}'.format(portfolio_update_id), json=update_portfolio)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")

    def test_422_update_portfolio(self):
    	""" Test the case where portfolio composition does not sum up to 100% """
    	update_portfolio = {"portfolio_name": "TEST_PORT3", 
    					"portfolio_compositions": [{"security_id": 1, "weight": 100}, 
    												{"security_id": 2, "weight": 100}]}
    	portfolio_update_id = 100
        res = self.client().patch('/portfolios/{}'.format(portfolio_update_id), json=update_portfolio)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable entity")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()