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
        self.fund_manager = os.environ.get('FUND_MANAGER')
        self.analyst = os.environ.get('ANALYST')
        self.assistant = os.environ.get('ASSISTANT')
        self.database_name = "assetmanagement_test"
        self.database_path = "postgresql://localhost:5432/{}".format(self.database_name)
        setup_db(self.app, self.database_path)
        db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_retrieve_portfolios(self):
        res = self.client().get('/portfolios', 
            headers={'Authorization':'Bearer ' + self.fund_manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['portfolios'])

    def test_retrieve_portfolio(self):
        res = self.client().get('/portfolios/1', 
            headers={'Authorization':'Bearer ' + self.fund_manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['portfolio_id'], 1)
        self.assertTrue(data['portfolio_name'])
        self.assertTrue(data['portfolio_compositions'])

    def test_404_retrieve_portfolio(self):
    	""" Test the case where portfolio_id does not exist """
    	res = self.client().get('/portfolios/100', 
            headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 404)
    	self.assertEqual(data['success'], False)
    	self.assertEqual(data['message'], "Not Found")

    def test_create_portfolio(self):
    	new_portfolio = {"portfolio_name": "TEST_PORT", 
    					"portfolio_compositions": [{"security_id": 1, "weight": 60}, 
    												{"security_id": 2, "weight": 40}]}
    	res = self.client().post('/portfolios', json=new_portfolio, 
            headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 200)
    	self.assertEqual(data['success'], True)
    	self.assertEqual(data['portfolio_name'], "TEST_PORT")
    	self.assertTrue(data['portfolio_id'])

    def test_analyst_401_create_portfolio(self):
    	""" Test the case when analyst tries to create a portfolio """
    	new_portfolio = {"portfolio_name": "TEST_PORT_401", 
    					"portfolio_compositions": [{"security_id": 1, "weight": 60}, 
    												{"security_id": 2, "weight": 40}]}
    	res = self.client().post('/portfolios', json=new_portfolio, 
            headers={'Authorization':'Bearer ' + self.analyst})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 401)
    	self.assertEqual(data['success'], False)
    	self.assertEqual(data['message'], "authentification failed")

    def test_422_create_portfolio(self):
    	""" Test the case where portfolio composition does not sum up to 100% """
    	new_portfolio = {"portfolio_name": "TEST_PORT", "portfolio_compositions": [{"security_id": 1, "weight": 100}, {"security_id": 2, "weight": 100}]}
    	res = self.client().post('/portfolios', json=new_portfolio, 
            headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 422)
    	self.assertEqual(data['success'], False)
    	self.assertEqual(data['message'], "Unprocessable entity")

    def test_delete_portfolio(self):
    	portfolio_delete_id = 2
    	res = self.client().delete('/portfolios/{}'.format(portfolio_delete_id), 
            headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 200)
    	self.assertEqual(data['success'], True)
    	self.assertEqual(data['deleted'], portfolio_delete_id)

    def test_404_delete_portfolio(self):
    	""" Test the case where portfolio_id does not exist """
    	portfolio_delete_id = 100
    	res = self.client().delete('/portfolios/{}'.format(portfolio_delete_id), 
            headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 404)
    	self.assertEqual(data['success'], False)
    	self.assertEqual(data['message'], "Not Found")

    def test_update_portfolio(self):
    	update_portfolio = {"portfolio_name": "TEST_PORT3", 
    					"portfolio_compositions": [{"security_id": 1, "weight": 50}, 
    												{"security_id": 2, "weight": 50}]}
    	portfolio_update_id = 3
    	res = self.client().patch('/portfolios/{}'.format(portfolio_update_id), json=update_portfolio, 
            headers={'Authorization':'Bearer ' + self.fund_manager})
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
    	res = self.client().patch('/portfolios/{}'.format(portfolio_update_id), json=update_portfolio, 
            headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 404)
    	self.assertEqual(data['success'], False)
    	self.assertEqual(data['message'], "Not Found")

    def test_422_update_portfolio(self):
    	""" Test the case where portfolio composition does not sum up to 100% """
    	update_portfolio = {"portfolio_name": "TEST_PORT3", 
    					"portfolio_compositions": [{"security_id": 1, "weight": 100}, 
    												{"security_id": 2, "weight": 100}]}
    	portfolio_update_id = 3
    	res = self.client().patch('/portfolios/{}'.format(portfolio_update_id), json=update_portfolio, 
            headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 422)
    	self.assertEqual(data['success'], False)
    	self.assertEqual(data['message'], "Unprocessable entity")

    def test_retrieve_securities(self):
        res = self.client().get('/securities', headers={'Authorization':'Bearer ' + self.fund_manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['securities'])

    def test_retrieve_security(self):
        res = self.client().get('/securities/1', headers={'Authorization':'Bearer ' + self.fund_manager})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['security_id'], 1)
        self.assertTrue(data['security_name'])
        self.assertTrue(data['asset_class'])
        self.assertTrue(data['region'])

    def test_assistant_retrieve_security(self):
    	""" Test the case where assistant views security"""
    	res = self.client().get('/securities/1', headers={'Authorization':'Bearer ' + self.assistant})
    	data = json.loads(res.data)
    	self.assertEqual(res.status_code, 200)
    	self.assertEqual(data['success'], True)
    	self.assertEqual(data['security_id'], 1)
    	self.assertTrue(data['security_name'])
    	self.assertTrue(data['asset_class'])
    	self.assertTrue(data['region'])

    def test_404_retrieve_security(self):
    	""" Test the case where security_id does not exist """
    	res = self.client().get('/securities/100', headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 404)
    	self.assertEqual(data['success'], False)
    	self.assertEqual(data['message'], "Not Found")

    def test_create_security(self):
    	new_security = {"security_name": "TEST_SECURITY", "region_id": 1, "asset_class_id": 1}
    	res = self.client().post('/securities', json=new_security, 
            headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 200)
    	self.assertEqual(data['success'], True)
    	self.assertEqual(data['security_name'], "TEST_SECURITY")
    	self.assertTrue(data['asset_class'])
    	self.assertTrue(data['region'])

    def test_analyst_create_security(self):
    	""" Test the case where analyst creates a security """
    	new_security = {"security_name": "TEST_SECURITY_analyst", "region_id": 1, "asset_class_id": 1}
    	res = self.client().post('/securities', json=new_security, 
            headers={'Authorization':'Bearer ' + self.analyst})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 200)
    	self.assertEqual(data['success'], True)
    	self.assertEqual(data['security_name'], "TEST_SECURITY_analyst")
    	self.assertTrue(data['asset_class'])
    	self.assertTrue(data['region'])

    def test_assistant_401_create_security(self):
    	""" Test the case where assistant tries to create a security """
    	new_security = {"security_name": "TEST_SECURITY_assistant", "region_id": 1, "asset_class_id": 1}
    	res = self.client().post('/securities', json=new_security, 
            headers={'Authorization':'Bearer ' + self.assistant})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 401)
    	self.assertEqual(data['success'], False)
    	self.assertEqual(data['message'], "authentification failed")

    def test_422_create_security(self):
    	""" Test the case where either asset_class_id or security_id is not available """
    	new_security = {"security_name": "TEST_SECURITY2", "region_id": 100, "asset_class_id": 1}
    	res = self.client().post('/securities', json=new_security, 
            headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 422)
    	self.assertEqual(data['success'], False)
    	self.assertEqual(data['message'], "Unprocessable entity")

    def test_delete_security(self):
    	security_delete_id = 5
    	res = self.client().delete('/securities/{}'.format(security_delete_id), 
            headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 200)
    	self.assertEqual(data['success'], True)
    	self.assertEqual(data['deleted'], security_delete_id)

    def test_404_delete_security(self):
    	""" Test the case where security_id does not exist """
    	security_delete_id = 100
    	res = self.client().delete('/securities/{}'.format(security_delete_id), 
            headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 404)
    	self.assertEqual(data['success'], False)
    	self.assertEqual(data['message'], "Not Found")

    def test_update_security(self):
    	update_security = {"security_name": "TEST_SECURITY3", "region_id": 1, "asset_class_id": 1}
    	security_update_id = 3
    	res = self.client().patch('/securities/{}'.format(security_update_id), 
            json=update_security, headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 200)
    	self.assertEqual(data['success'], True)
    	self.assertEqual(data['updated'], security_update_id)

    def test_404_update_security(self):
    	""" Test the case where security_id does not exist """
    	update_security = {"security_name": "TEST_SECURITY4", "region_id": 1, "asset_class_id": 1}
    	security_update_id = 100
    	res = self.client().patch('/securities/{}'.format(security_update_id), 
            json=update_security, headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 404)
    	self.assertEqual(data['success'], False)
    	self.assertEqual(data['message'], "Not Found")

    def test_422_update_security(self):
    	""" Test the case where either asset_class_id or security_id is not available """
    	update_security = {"security_name": "TEST_SECURITY4", "region_id": 100, "asset_class_id": 1}
    	security_update_id = 3
    	res = self.client().patch('/securities/{}'.format(security_update_id), 
            json=update_security, headers={'Authorization':'Bearer ' + self.fund_manager})
    	data = json.loads(res.data)

    	self.assertEqual(res.status_code, 422)
    	self.assertEqual(data['success'], False)
    	self.assertEqual(data['message'], "Unprocessable entity")

    def test_retrieve_regions(self):
        res = self.client().get('/regions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['regions'])

    def test_retrieve_asset_classes(self):
        res = self.client().get('/asset_classes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['asset_classes'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()