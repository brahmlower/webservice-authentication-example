import sys
import json
from contextlib import contextmanager
from flask import Flask
from flask import Response
from flask import request
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
import jwt

from . import auth
from . import data_access

class BuildingsApi(Flask):
    def __init__(self, app_config):
        super().__init__(__name__)
        # Register the routes and their handlers
        self.route('/')(self.index)
        self.route('/login')(self.login)
        self.route('/logout')(self.logout)
        self.route('/home')(self.home)
        self.route('/signup')(self.signup)
        self.route('/static/<path:path>')(self.send_static)
        self.route('/api/')(self.api_index)
        self.route('/api/signup', methods=['POST'])(self.api_signup)
        self.route('/api/auth', methods=['POST'])(self.api_auth)
        self.route('/api/buildings')(self.api_buildings)
        self.route('/api/buildings/<building_id>')(self.api_building_get)
        # Read the configuration file
        self.app_config = app_config
        self.config['SQLALCHEMY_DATABASE_URI'] = self._get_db_uri()
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db = SQLAlchemy(self, session_options={"autoflush": False})
        self.Session = sessionmaker()
        self.Session.configure(bind=self.db.engine)

        # self.db.Model.metadata.reflect(self.db.engine)
        # Connect to the database and create our connection pool
        # try:
        #     self.db_pool = self._init_db_pool()
        # except Exception as e:
        #     sys.exit("Failed to connect to database: {}".format(e))

    def _get_db_uri(self):
        database = self.app_config['db']['database']
        username = self.app_config['db']['username']
        password = self.app_config['db']['password']
        hostname = self.app_config['db']['hostname']
        port = self.app_config['db']['port']
        return "postgresql://{username}:{password}@{hostname}:{port}/{database}".format(
            username=username,
            password=password,
            hostname=hostname,
            database=database,
            port=port
        )

    # def _init_db_pool(self):
    #     database = self.app_config['db']['database']
    #     username = self.app_config['db']['username']
    #     password = self.app_config['db']['password']
    #     hostname = self.app_config['db']['hostname']
    #     port = self.app_config['db']['port']
    #     db_pool = ThreadedConnectionPool(1, 20, database=database,
    #         user=username, password=password, host=hostname, port=port)
    #     return db_pool

    # @contextmanager
    # def _get_db_connection(self):
    #     try:
    #         connection = self.db_pool.getconn()
    #         yield connection
    #     finally:
    #         self.db_pool.putconn(connection)

    # @contextmanager
    # def _get_db_cursor(self, commit=False):
    #     with self._get_db_connection() as connection:
    #         cursor = connection.cursor(cursor_factory=RealDictCursor)
    #         try:
    #             yield cursor
    #             if commit:
    #                 connection.commit()
    #         finally:
    #             cursor.close()

    def index(self):
        return send_from_directory('static', 'index.html')

    def login(self):
        return send_from_directory('static', 'login.html')

    def signup(self):
        return send_from_directory('static', 'signup.html')

    def logout(self):
        return send_from_directory('static', 'logout.html')

    def home(self):
        return send_from_directory('static', 'home.html')

    def send_static(self, path):
        return send_from_directory('static', path)

    def api_index(self):
        content = json.dumps({'message': 'Hello world!'})
        return Response(content, mimetype='application/json')

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
        signup_request = request.get_json()
        signup_method = signup_request.get('method')
        signup_handlers = {
            'standalone': self._api_signup_standalone,
            'google': self._api_signup_google
        }
        # Input sanitisation
        if signup_method not in signup_handlers.keys():
            raise Exception
        if signup_method not in signup_request.keys():
            raise Exception
        # Call the requested signup method
        handler_request = signup_request[signup_method]
        handler_func = signup_handlers[signup_method]
        session = self.Session(autoflush=True)
        (signup_success, account_id) = handler_func(session, handler_request)
        if signup_success is True:
            token = self._get_auth_jwt(session, account_id)
            session.commit()
            content = {'success': signup_success, 'token': token.decode('utf-8')}
            return Response(json.dumps(content), mimetype='application/json')
        else:
            session.rollback()
            content = {'success': signup_success, 'token': None}
            return Response(json.dumps(content), mimetype='application/json')

    def _api_signup_google(self, session, signup_data):
        # Token verification w/ google
        user_token = signup_data.get('token')
        if user_token is None:
            return (False, None)
        google_client_id = self.app_config['auth']['backends']['google']['client_id']
        result = auth.verify_google_token(google_client_id, user_token) # TODO: What happens when this fails?
        # Create base account
        db_result = data_access.account_base_create(session, result['name'])
        if db_result is None:
            return (False, None)
        # Create google account
        account_id = db_result['id']
        db_result = data_access.account_google_create(session, account_id, result['name'], result['email'])
        if db_result is None:
            return (False, None)
        else:
            return (True, db_result['account_id'])

    def _api_signup_standalone(self, session, signup_data):
        name = signup_data.get('name')
        username = signup_data.get('username')
        password = signup_data.get('password')
        if None in [name, username, password]:
            return (False, None)
        # Create base account
        db_result = data_access.account_base_create(session, name)
        if db_result is None:
            return (False, None)
        # Create google account
        account_id = db_result['id']
        db_result = data_access.account_standalone_create(session, account_id, username, password)
        if db_result is not None:
            return (True, db_result['account_id'])
        else:
            return (False, None)

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
        auth_request = request.get_json()
        auth_method = auth_request.get('method')
        auth_handlers = {
            'standalone': self._api_auth_standalone,
            'google': self._api_auth_google
        }
        # Input sanitisation
        if auth_method is None:
            raise Exception('Missing required key: "auth_method"')
        if auth_method not in auth_handlers.keys():
            raise Exception('Invalid auth method: {}'.format(auth_method))
        # Call the requested authentication method
        handler_request = auth_request[auth_method]
        handler_func = auth_handlers[auth_method]
        session = self.Session(autocommit=True) # TODO: CHANGE THIS TO AUTOFLUSH, NOT AUTOCOMMIT
        (auth_success, account_id) = handler_func(session, handler_request)
        # Build the return response
        content = {'success': auth_success}
        if auth_success is True:
            # The user has been verified, so we can build an auth token for them now
            jwt_value = self._get_auth_jwt(session, account_id)
            content['token'] = jwt_value.decode("utf-8")
        else:
            print('Auth failed for method: {}'.format(auth_method))
        return Response(json.dumps(content), mimetype='application/json')

    def _get_auth_jwt(self, session, account_id):
        jwt_secret = self.app_config['auth']['jwt']['secret']
        jwt_algo = self.app_config['auth']['jwt']['algo']
        # print('building jwt for account_id: {}'.format(account_id))
        account = data_access.account_get_by_id(session, account_id)
        if account is None:
            raise Exception('account with id {} not found'.format(account_id))
        jwt_dict = dict(account)
        del(jwt_dict['id'])
        return jwt.encode(jwt_dict, jwt_secret, algorithm=jwt_algo)

    def _api_auth_standalone(self, session, auth_data):
        username = auth_data.get('username')
        password = auth_data.get('password')
        db_result = data_access.account_login_standalone(session, username, password)
        if db_result is not None:
            return (True, db_result['account_id'])
        else:
            return (False, None)

    def _api_auth_google(self, session, auth_data):
        # Token verification w/ google
        user_token = auth_data.get('token')
        if user_token is None:
            return (False, None)
        google_client_id = self.app_config['auth']['backends']['google']['client_id']
        result = auth.verify_google_token(google_client_id, user_token) # TODO: What happens when this fails?
        # Account retrieval
        db_result = data_access.account_login_google(session, result['email'])
        if db_result is not None:
            return (True, db_result['account_id'])
        else:
            return (False, None)

    def api_buildings(self):
        buildings = data_access.buildings_all(session)
        return Response(str(buildings), mimetype='application/json')

    def api_building_get(self, building_id):
        building = data_access.buildings_get(session, building_id)
        return Response(str(building), mimetype='application/json')
