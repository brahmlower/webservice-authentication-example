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

from .auth_generations import PlaintextAuth
from .auth_generations import BcryptAuth

class BaseAccount(object):
    def __init__(self):
        self.record_id = None
        self.name = None
        self.providers = None

    @classmethod
    def from_db(cls, rowproxy):
        inst = cls()
        inst.record_id = rowproxy.id
        inst.name = rowproxy.name
        return inst

    def load_providers(self, session):
        tmp_dict = {}
        # Standard accounts
        db_standard = account_standard_get_by_account_id(session, self.record_id)
        if db_standard is not None:
            standard = StandardAccount.from_db(db_standard)
            tmp_dict['standard'] = [standard]
        # Google accounts
        db_googles = account_google_get_by_account_id(session, self.record_id)
        if db_googles is not None:
            tmp_dict['google'] = list(map(GoogleAccount.from_db, db_googles))
        self.providers = tmp_dict

    def as_dict(self):
        return {
            'id': self.record_id,
            'name': self.name,
            'providers': list(self.providers.keys())
        }

class StandardAccount(object):
    TARGET_AUTH_GEN = 'gen_0'
    AUTH_GEN_REGISTRY = {
        'gen_0': PlaintextAuth,
        'gen_1': BcryptAuth
    }

    def __init__(self):
        self.record_id = None
        self.account_id = None
        self.username = None
        self.password = None
        self.hash_gen = None

    @classmethod
    def from_db(cls, db_account):
        inst = cls()
        inst.record_id = db_account['id']
        inst.account_id = db_account['account_id']
        inst.username = db_account['username']
        inst.password = db_account['password']
        inst.hash_gen = db_account['hash_gen']
        return inst

    def as_dict(self):
        return {
            'id': self.record_id,
            'account_id': self.account_id,
            'username': self.username
        }

    def update_password(self, session):
        result = account_standard_update_password(
            session,
            self.account_id,
            self.password,
            self.hash_gen
        )
        print("INFO: Update result: {}".format(result))

    def set_auth_gen(self, auth_gen_id, plaintext_secret):
        # Verify auth gen id is valid
        if auth_gen_id not in self.AUTH_GEN_REGISTRY.keys():
            raise ValueError('Invalid auth_gen_id: {}. Options are: {}'.format(auth_gen_id, self.AUTH_GEN_REGISTRY.keys()))
        auth_class = self.AUTH_GEN_REGISTRY[auth_gen_id]
        new_inst = auth_class.prepare_account(self, plaintext_secret)
        self.__dict__ = {**self.__dict__, **new_inst.__dict__} # Is probably intoduces some weird errors. Prolly shouldn't be doing this

    def set_auth_gen_latest(self, plaintext_secret):
        return self.set_auth_gen(self.TARGET_AUTH_GEN, plaintext_secret)

    def check_auth_gen_current(self):
        return self.hash_gen == self.TARGET_AUTH_GEN

    def check_password(self, plaintext_secret):
        auth_class = self.AUTH_GEN_REGISTRY[self.hash_gen]
        print("INFO: Authenticating using {} (gen_id: {})".format(
            auth_class.__name__,
            self.hash_gen
        ))
        return auth_class.check_secret(plaintext_secret, self)

    def save(self, session):
        return account_standard_update_auth_gen(session, self.record_id, self.password, self.hash_gen)

class GoogleAccount(object):
    def __init__(self):
        pass

def list_accounts(session):
    db_results = account_base_list(session)
    return list(map(BaseAccount.from_db, db_results))

def get_account(session, account_id):
    db_result = account_base_get_by_id(session, account_id)
    base_account = BaseAccount.from_db(db_result)
    base_account.load_providers(session)
    return base_account

def list_account_providers(session, account_id):
    db_result = account_base_get_by_id(session, account_id)
    base_account = BaseAccount.from_db(db_result)
    base_account.load_providers(session)
    return list(base_account.providers.keys())

def get_account_provider(session, account_id, provider_name):
    db_result = account_base_get_by_id(session, account_id)
    base_account = BaseAccount.from_db(db_result)
    base_account.load_providers(session)
    return base_account.providers[provider_name]

def get_auth_jwt(session, account_id, jwt_secret, jwt_algo):
    account = account_base_get_by_id(session, account_id)
    if account is None:
        raise Exception('account with id {} not found'.format(account_id))
    # TODO: The following two lines are a sloppy way of preparing the account data
    # for the jwt token. We're basically encoding everything from the account record
    # in the token except for the primary id.
    jwt_dict = dict(account)
    del(jwt_dict['id'])
    token_bytes = jwt.encode(jwt_dict, jwt_secret, algorithm=jwt_algo)
    token_sting = token_bytes.decode('utf-8')
    return token_sting
