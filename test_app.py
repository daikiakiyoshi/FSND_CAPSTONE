import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Portfolio, Security, PortfolioComposition, AssetClass, Region


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
        print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['portfolios'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()