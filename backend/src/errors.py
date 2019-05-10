
class ServiceException(Exception):
    def __init__(self, message, status=400):
        super().__init__()
        self.message = message
        self.status_code = status

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, self.message)

    def as_dict(self):
        return {
            'error': self.__class__.__name__,
            'message': self.message
        }

# Generic errors

class DatabaseError(ServiceException):
    def __init__(self, error):
        super().__init__('Database error: {}'.format(str(error)), status=500)

class ItemNotFound(ServiceException):
    def __init__(self, item_id):
        super().__init__('Could not find item with id {}'.format(item_id))

# Standard signup/authentication errors

class StandardSignupMissingName(ServiceException):
    def __init__(self):
        super().__init__('Standard signup error: Missing field Name')

class StandardSignupMissingUsername(ServiceException):
    def __init__(self):
        super().__init__('Standard signup error: Missing field Username')

class StandardSignupMissingPassword(ServiceException):
    def __init__(self):
        super().__init__('Standard signup error: Missing field Password')

class StandardAuthMissingUsername(ServiceException):
    def __init__(self):
        super().__init__('Standard login error: Missing field Username')

class StandardAuthMissingPassword(ServiceException):
    def __init__(self):
        super().__init__('Standard login error: Missing field Password')

class StandardAuthFailure(ServiceException):
    def __init__(self):
        super().__init__('Username or password incorrect')

# Google signup/authentication errors

class GoogleAuthUpstreamError(ServiceException):
    def __init__(self):
        super().__init__('Error while requesting Google Oauth service', status=500)

class GoogleSignupMissingToken(ServiceException):
    def __init__(self):
        super().__init__('Missing google oauth token')

class GoogleAuthMissingToken(ServiceException):
    def __init__(self):
        super().__init__('Missing google oauth token')

# Auth provider errors

class AuthProviderRequestUnreadable(ServiceException):
    """ For cases when the request failed to be parsed as JSON by Flask. This can be caused by forgetting the content-type header. """
    def __init__(self):
        super().__init__('Provided data could not be read')

class AuthProviderInvalidProvider(ServiceException):
    def __init__(self, provider):
        super().__init__('Invalid provider: {}'.format(provider))

class AuthProviderNotImplemented(ServiceException):
    def __init__(self, provider):
        super().__init__('Provider "{}" supported but not implemented (Programming error)'.format(provider), status=500)

class AuthProviderMissingProvider(ServiceException):
    def __init__(self):
        super().__init__('Provided data missing "method" key')

class AuthProviderMissingProviderDetails(ServiceException):
    def __init__(self):
        super().__init__('Provided data missing provider specific details')

# Misc auth errors

class MissingRequiredHeader(ServiceException):
    def __init__(self, header):
        super().__init__('Missing required header: {}'.format(header))

class AuthTokenInvalid(ServiceException):
    def __init__(self):
        super().__init__('Provided JWT token is invalid')
