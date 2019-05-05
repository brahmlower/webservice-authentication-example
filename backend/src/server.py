import json
from flask import Flask
from flask import Response
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

from .domain.auth import AuthRequest
from .domain.auth import SignupRequest
from .domain.account import get_auth_jwt
from .domain.account import list_accounts
from .domain.account import get_account
from .domain.account import list_account_providers
from .domain.account import get_account_provider
from .domain.buildings import get_building
from .domain.buildings import list_buildings
from .domain.buildings import Building
from .errors import ServiceException

class BuildingsApi(Flask):
    def __init__(self, app_config):
        super().__init__(__name__)
        # Service management routes
        self.route('/')(self.index)
        self.route('/health')(self.health)
        # API routes
        self.route('/api/signup', methods=['POST'])(self.api_signup)
        self.route('/api/auth', methods=['POST'])(self.api_auth)
        self.route('/api/accounts')(self.api_list_accounts)
        self.route('/api/accounts/<account_id>')(self.api_get_account)
        self.route('/api/accounts/<account_id>/providers')(self.api_list_account_providers)
        self.route('/api/accounts/<account_id>/providers/<provider_name>')(self.api_get_account_provider)
        self.route('/api/buildings')(self.api_list_buildings)
        self.route('/api/buildings/<building_id>')(self.api_get_building)
        # Read the configuration file
        self.app_config = app_config
        self.config['SQLALCHEMY_DATABASE_URI'] = self._get_db_uri()
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db = SQLAlchemy(self, session_options={"autoflush": False})
        self.Session = sessionmaker()
        self.Session.configure(bind=self.db.engine)

    def _get_db_uri(self):
        return "postgresql://{username}:{password}@{hostname}:{port}/{database}".format(
            username=self.app_config['db']['username'],
            password=self.app_config['db']['password'],
            hostname=self.app_config['db']['hostname'],
            database=self.app_config['db']['database'],
            port=self.app_config['db']['port']
        )

# Authentication routes --------------------------------------------------------

    def api_signup(self):
        """ Endpoint to handle the signup/account creation process

            This endpoints recieves an account creation request, indicating which
            type of account method to set up. Only one account method can be created
            on account creation, but other can be created at a later point. Like
            account authentication, supported methods are 'standalone' and 'google'.

            Creation request for 'standalone' method:
            ```
            {
                'method': 'standalone',
                'standalone': {
                    'name': '<user provided name>',
                    'username': '<user provided username>',
                    'password': '<user provided password>'
                }
            }
            ```

            Creation request for 'google' method:
            ```
            {
                'method': 'google',
                'google': {
                    'token': '<google provided oauth token>',
                }
            }
            ```
        """
        signup_data = request.get_json()
        jwt_secret = self.app_config['auth']['jwt']['secret']
        jwt_algo = self.app_config['auth']['jwt']['algo']
        session = self.Session(autoflush=True)
        try:
            signup_request = SignupRequest.from_dict(signup_data)
            account_id = signup_request.signup(session, self.app_config)
            token = get_auth_jwt(session, account_id, jwt_secret, jwt_algo)
        except ServiceException as error:
            session.rollback()
            status_code = error.status_code
            response_dict = {'success': False, 'response': error.as_dict()}
        else:
            session.commit()
            status_code = 200
            response_dict = {'success': True, 'response': token}
        finally:
            content = json.dumps(response_dict)
            return Response(content, status=status_code, mimetype='application/json')

    def api_auth(self):
        """ Endpoint to handle the process of logging into an account

            The endpoint handles the authentication process for any supported
            authentication method. Current supported auth methods are 'standalone'
            and 'google'. Examples for each are as follows:

            Authentication request for 'standalone' method:
            ```
            {
                'method': 'standalone',
                'standalone': {
                    'username': '<user provided username>',
                    'password': '<user provided password>'
                }
            }
            ```

            Authentication request for 'google' method:
            ```
            {
                'method': 'google',
                'google': {
                    'token': '<google provided oauth token>'
                }
            }
            ```
        """
        auth_data = request.get_json()
        jwt_secret = self.app_config['auth']['jwt']['secret']
        jwt_algo = self.app_config['auth']['jwt']['algo']
        session = self.Session(autoflush=True)
        try:
            auth_request = AuthRequest.from_dict(auth_data)
            account_id = auth_request.auth(session, self.app_config)
            token = get_auth_jwt(session, account_id, jwt_secret, jwt_algo)
        except ServiceException as error:
            session.rollback()
            status_code = error.status_code
            response_dict = {'success': False, 'response': error.as_dict()}
        else:
            session.commit()
            status_code = 200
            response_dict = {'success': True, 'response': {'token': token}}
        finally:
            content = json.dumps(response_dict)
            return Response(content, status=status_code, mimetype='application/json')

# Account management routes ----------------------------------------------------

    def api_list_accounts(self):
        session = self.Session(autoflush=True)
        try:
            accounts = list_accounts(session)
        except ServiceException as error:
            status_code = 400
            response_dict = {'success': False, 'response': error.as_dict()}
        else:
            status_code = 200
            response_dict = {'success': True, 'response': [x.as_dict() for x in accounts]}
        finally:
            content = json.dumps(response_dict)
            return Response(content, status=status_code, mimetype='application/json')

    def api_get_account(self, account_id):
        session = self.Session(autoflush=True)
        try:
            account = get_account(session, account_id)
        except ServiceException as error:
            status_code = 400
            response_dict = {'success': False, 'response': error.as_dict()}
        else:
            status_code = 200
            response_dict = {'success': True, 'response': account.as_dict()}
        finally:
            content = json.dumps(response_dict)
            return Response(content, status=status_code, mimetype='application/json')

    def api_list_account_providers(self, account_id):
        session = self.Session(autoflush=True)
        try:
            provider_types = list_account_providers(session, account_id)
        except ServiceException as error:
            status_code = 400
            response_dict = {'success': False, 'response': error.as_dict()}
        else:
            status_code = 200
            response_dict = {'success': True, 'response': provider_types}
        finally:
            content = json.dumps(response_dict)
            return Response(content, status=status_code, mimetype='application/json')

    def api_get_account_provider(self, account_id, provider_name):
        session = self.Session(autoflush=True)
        try:
            provider_list = get_account_provider(session, account_id, provider_name)
        except ServiceException as error:
            status_code = 400
            response_dict = {'success': False, 'response': error.as_dict()}
        else:
            status_code = 200
            response_dict = {'success': True, 'response': [x.as_dict() for x in provider_list]}
        finally:
            content = json.dumps(response_dict)
            return Response(content, status=status_code, mimetype='application/json')

# Business routes --------------------------------------------------------------

    def index(self):
        content = json.dumps({
            'message': 'Version information should go here I think?'
        })
        return Response(content, mimetype='application/json')

    def health(self):
        content = json.dumps({
            'health': 'okay (stubbed)',
            'checks': {
                'db': 'okay (stubbed)'
            }
        })
        return Response(content, mimetype='application/json')

    def api_get_building(self, building_id):
        session = self.Session(autocommit=True)
        try:
            building = get_building(session, building_id)
        except ServiceException as error:
            status_code = 400
            response_dict = {'success': False}
        else:
            status_code = 200
            response_dict = {'success': True, 'response': building.as_dict()}
        finally:
            content = json.dumps(response_dict)
            return Response(content, status=status_code, mimetype='application/json')

    def api_list_buildings(self):
        session = self.Session(autocommit=True)
        try:
            buildings = list_buildings(session)
        except ServiceException as error:
            status_code = 400
            response_dict = {'success': False}
        else:
            status_code = 200
            response_dict = {'success': True, 'response': [x.as_dict() for x in buildings]}
        finally:
            content = json.dumps(response_dict)
            return Response(content, status=status_code, mimetype='application/json')
