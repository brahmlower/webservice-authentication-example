import jwt
from google.oauth2 import id_token
from google.auth.transport import requests

from ..data_access.account import account_base_create
from ..data_access.account import account_base_list
from ..data_access.account import account_base_get_by_id
from ..data_access.account import account_standard_create
from ..data_access.account import account_standard_get_by_username
from ..data_access.account import account_standard_get_by_account_id
from ..data_access.account import account_standard_update_password
from ..data_access.account import account_standard_update_auth_gen
from ..data_access.account import account_google_create
from ..data_access.account import account_google_get_by_email
from ..data_access.account import account_google_get_by_account_id

from .account import StandardAccount
from .auth_generations import PlaintextAuth
from .auth_generations import BcryptAuth

from ..errors import InvalidProviderError
from ..errors import StandardSignupMissingName
from ..errors import StandardSignupMissingUsername
from ..errors import StandardSignupMissingPassword
from ..errors import StandardAuthFailure

# Base class
class AuthProviders(object):
    providers = {}
    def __init__(self, method, method_inst):
        self.method = method
        self.method_inst = method_inst

    @classmethod
    def get_provider(cls, method):
        if method not in cls.providers.keys():
            raise InvalidProviderError(method)
        return cls.providers[method]

    @classmethod
    def from_dict(cls, data):
        method = data.get('method')
        if method is None:
            raise ValueError('Incorrectly formatted request')
        if method not in data.keys():
            raise ValueError('Missing method specific data structure')
        method_class = cls.get_provider(method)
        method_inst = method_class.from_dict(data[method])
        inst = cls(method, method_inst)
        return inst

# Signup classes ---------------------------------------------------------------

class StandardSignupRequest(object):
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def signup(self, session):
        # Create base account
        db_result = account_base_create(session, self.name)
        if db_result is None:
            raise Exception('Database operation failed while creating base account')
        # Create google account
        account_id = db_result['id']
        db_result = account_standard_create(session, account_id, self.username, self.password)
        if db_result is None:
            raise Exception('Database operation failed while creating standard association')
        return account_id

    @classmethod
    def from_dict(cls, data):
        name = data.get('name')
        if name is None:
            raise StandardSignupMissingName()
        username = data.get('username')
        if username is None:
            raise StandardSignupMissingUsername()
        password = data.get('password')
        if password is None:
            raise StandardSignupMissingPassword()
        inst = cls(name, username, password)
        return inst

class GoogleSignupRequest(object):
    def __init__(self, token):
        self.token = token

    def signup(self, session, google_client_id):
        # Verify the provided token
        oauth_result = verify_google_token(google_client_id, self.token) # TODO: What happens when this fails?
        oauth_name = oauth_result['name']
        oauth_email = oauth_result['email']
        # Create base account
        db_result = account_base_create(session, oauth_name)
        if db_result is None:
            raise Exception('Database operation failed while creating base account')
        # Create google account
        account_id = db_result['id']
        db_result = account_google_create(session, account_id, oauth_name, oauth_email)
        if db_result is None:
            raise Exception('Database operation failed while creating google oauth association')
        return account_id

    @classmethod
    def from_dict(cls, data):
        token = data.get('token')
        if token is None:
            raise ValueError('Google: Missing token')
        inst = cls(token)
        return inst

class SignupRequest(AuthProviders):
    providers = {
        'standard': StandardSignupRequest,
        'google': GoogleSignupRequest
    }
    def signup(self, session, app_config):
        if self.method == 'standard':
            # handle standard signup
            account_id = self.method_inst.signup(session)
            return account_id
        elif self.method == 'google':
            # handle google oauth signup
            google_client_id = app_config['auth']['backends']['google']['client_id']
            account_id = self.method_inst.signup(session, google_client_id)
            return account_id
        raise ValueError('Method has no corresponding authentication mechanism')

# Authentication classes -------------------------------------------------------

class StandardAuthRequest(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def auth(self, session):
        # Step 1: Fetch account provider record
        print("INFO: Fetching account with username: {}".format(self.username))
        db_account = account_standard_get_by_username(session, self.username)
        if db_account is None:
            raise StandardAuthFailure()
        account = StandardAccount.from_db(db_account)
        # Step 2: Create hash with recorded hash_gen
        print("INFO: Creating hash of provided password")
        if account.check_password(self.password) is False:
            raise StandardAuthFailure()
        # Step 3: Upgrade hash using new hashing func if needed
        print("DEBUG: Comparing accounts hashing generation")
        if account.check_auth_gen_current() is False:
            print("INFO: Updating hash generation of account password")
            account.set_auth_gen_latest(self.password)
            account.save(session)
        # Step 4: Return base account ID
        return account.account_id

    @classmethod
    def from_dict(cls, data):
        username = data.get('username')
        if username is None:
            raise ValueError()
        password = data.get('password')
        if password is None:
            raise ValueError()
        inst = cls(username, password)
        return inst

class GoogleAuthRequest(object):
    def __init__(self, token):
        self.token = token

    def auth(self, session, google_client_id):
        oauth_result = verify_google_token(google_client_id, self.token) # TODO: What happens when this fails?
        oauth_email = oauth_result['email']
        # Account retrieval
        db_result = account_google_get_by_email(session, oauth_email)
        if db_result is None:
            raise Exception('Error while getting google stuff')
        return db_result['account_id']

    @classmethod
    def from_dict(cls, data):
        user_token = data.get('token')
        if user_token is None:
            raise ValueError('Missing required property: token')
        inst = cls(user_token)
        return inst

class AuthRequest(AuthProviders):
    providers = {
        'standard': StandardAuthRequest,
        'google': GoogleAuthRequest
    }
    def auth(self, session, app_config):
        if self.method == 'standard':
            # handle standard signup
            account_id = self.method_inst.auth(session)
            return account_id
        elif self.method == 'google':
            # handle google oauth signup
            google_client_id = app_config['auth']['backends']['google']['client_id']
            account_id = self.method_inst.auth(session, google_client_id)
            return account_id
        raise ValueError('Method has no corresponding authentication mechanism')

def verify_google_token(google_client_id, user_token):
    id_info = id_token.verify_oauth2_token(user_token, requests.Request(), google_client_id)
    if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        return None
    return id_info
