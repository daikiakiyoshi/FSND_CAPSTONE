# FSND_CAPSTONE: Asset Management Company API

## HEROKU project URL
```https://nd-asset-managament.herokuapp.com/```

To use the live URL above, replace <token> with FUND_MANAGER in setup.sh.
### GET '/portfolios'
- Sample: ```curl https://nd-asset-managament.herokuapp.com/ -X GET -H 'Authorization: Bearer <token>'```

## Getting Started
If you want to run this project locally, run the followings.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql assetmanagement < assetmanagement_data.psql
```

## Environment Variables Setup
```bash
source setup.sh
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

## Tasks

Asset Manager Specifications
* The Asset Manager models a company that is responsible for making portfolios and managing and allocating securities to those portfolios. You are a Fund Manager within the company and are creating a system to simplify and streamline your process. 
* Models:
    * Portfolios with attributes name, security, and weight
    * Securities with attributes name, region, asset class
* Endpoints:
    * GET /portfolios and /securities
    * DELETE /portfolios/ and /securities/
    * POST /portfolios and /securities and
    * PATCH /securities/ and /portfolios/
* Roles:
    * Administrative Assistant 
        * Can view portfolios and securities
    * Analyst
        * All permissions an Administrative Assistant  has and…
        * Add a security from the database
        * Modify a security 
    * Fund Manager
        * All permissions an Analyst has and…
        * Delete a security
        * Add or delete a portfolio from the database
* Tests:
    * One test for success behavior of each endpoint
    * One test for error behavior of each endpoint
    * At least two tests of RBAC (role based access control) for each role

## API Endpoints
### GET '/portfolios'
- Sample: ```curl http://127.0.0.1:5000/portfolios -X GET -H 'Authorization: Bearer <token>'```
### GET '/portfolios/<int:portfolio_id>'
- Sample: ```curl http://127.0.0.1:5000/portfolios/2 -X GET -H 'Authorization: Bearer <token>'```
### POST '/portfolios'
- Sample: ```curl http://127.0.0.1:5000/portfolios -X POST -H "Content-Type:application/json" -d '{"portfolio_name": "S&P/NASDAQ 60/40 Equity", "portfolio_compositions": [{"security_id": 1, "weight": 60}, {"security_id": 2, "weight": 40}]}' -H 'Authorization: Bearer <token>'```
### DELETE '/portfolios/<int:portfolio_id>'
- Sample: ```curl http://127.0.0.1:5000/portfolio/2 -X DELETE -H 'Authorization: Bearer <token>'```
### PATCH '/portfolios/<int:portfolio_id>'
- Sample: ```curl http://127.0.0.1:5000/portfolio/2 -X PATCH -H "Content-Type:application/json" -d '{"portfolio_name": "S&P/NASDAQ 60/40 Equity", "portfolio_compositions": [{"security_id": 1, "weight": 60}, {"security_id": 2, "weight": 40}]}' -H 'Authorization: Bearer <token>'```

### GET '/securities'
- Sample: ```curl http://127.0.0.1:5000/securities -X GET -H 'Authorization: Bearer <token>'```
### GET '/securities/<int:security_id>'
- Sample: ```curl http://127.0.0.1:5000/securities/2 -X GET -H 'Authorization: Bearer <token>'```
### POST '/securities'
- Sample: ```curl http://127.0.0.1:5000/securities -X POST -H "Content-Type:application/json" -d '{"security_name": "TOPIX", "region_id": "1", "asset_class_id": 1}' -H 'Authorization: Bearer <token>'```
### DELETE '/securities/<int:security_id>'
- Sample: ```curl http://127.0.0.1:5000/securities/2 -X DELETE -H 'Authorization: Bearer <token>'```
### PATCH '/securities/<int:security_id>'
- Sample: ```curl http://127.0.0.1:5000/securities/2 -X PATCH -H "Content-Type:application/json" -d '{"security_name": "TOPIX", "region_id": "1", "asset_class_id": 1}' -H 'Authorization: Bearer <token>'```

### GET '/asset_classes'
- Sample: ```curl http://127.0.0.1:5000/asset_classes -X GET```
### GET '/securities'
- Sample: ```curl http://127.0.0.1:5000/regions -X GET```

## Testing
To run the tests, run
```
dropdb assetmanagement_test && createdb assetmanagement_test
python helper.py
psql assetmanagement_test < assetmanagement_data.psql
python test_app.py
```
