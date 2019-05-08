
import bcrypt

class AuthMethod(object):
    """ Base AuthMethod to be subclassed for specific auth implementaitons

    I tried an abstract base class initially, but it lead down a rabbit-hole of
    unnecessary complexity for the scope of this project. Keep it simple stupid.
    """
    @classmethod
    def prepare_account(cls, account, plaintext_secret, *args, **kwargs):
        account.hash_gen = cls.GEN_ID # pylint: disable=E1101
        account.password = cls.hash_secret(plaintext_secret) # pylint: disable=E1101
        return account

class PlaintextAuth(AuthMethod):
    """ Plaintext authentication

    Defines the "hashing" and comparison functions for handling plaintext
    passwords. This is provided in part as an example to show how the
    authentication generations feature works.
    """
    GEN_ID = 'gen_0'

    @classmethod
    def hash_secret(cls, plaintext_secret, *args, **kwargs):
        return plaintext_secret

    @classmethod
    def check_secret(cls, plaintext_secret, account):
        return plaintext_secret == account.password

class BcryptAuth(AuthMethod):
    """ Bcrypt authentication

    A simple, slightly niave bcrypt hashing strategy. I say naive becase salt
    runs is left at its default value, and the hashing strategy does not
    re-hash the result of the first salt+hash.
    """
    GEN_ID = 'gen_1'

    @classmethod
    def hash_secret(cls, plaintext_secret, *args, **kwargs):
        raw_hash = bcrypt.hashpw(
            plaintext_secret.encode('utf-8'),
            bcrypt.gensalt()
        )
        return raw_hash.decode('utf-8')

    @classmethod
    def check_secret(cls, plaintext_secret, account, *args, **kwargs):
        clean_secret = plaintext_secret.encode('utf-8')
        clean_hash = account.password.encode('utf-8')
        return bcrypt.checkpw(clean_secret, clean_hash)
