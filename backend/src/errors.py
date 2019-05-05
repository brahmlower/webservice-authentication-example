
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

class InvalidProviderError(ServiceException):
    def __init__(self, provider):
        super().__init__('Invalid provider: {}'.format(provider))

class StandardSignupMissingName(ServiceException):
    def __init__(self):
        super().__init__('Standard signup error: Missing field Name')

class StandardSignupMissingUsername(ServiceException):
    def __init__(self):
        super().__init__('Standard signup error: Missing field Username')

class StandardSignupMissingPassword(ServiceException):
    def __init__(self):
        super().__init__('Standard signup error: Missing field Password')

class StandardAuthFailure(ServiceException):
    def __init__(self):
        super().__init__('Username or password incorrect')
