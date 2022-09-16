exceptions = []


class IDException(Exception):
    code = '0'
    message = None

    def __init_subclass__(cls, *args, **kws):
        exceptions.append(cls)

    def __init__(self, message=None):
        self.message = message

    def __repr__(self):
        return f'Error(msg={self.message})'


class ParseError(IDException):
    code = '0'
    message = 'Data Parsing Error，Please Validate The Malformed Data'


class MediaTypeError(IDException):
    code = '0'
    message = 'Media Type Error，Please Set Content_Type As Application/Json In Headers'


class UnknownError(IDException):
    code = '0'
    message = 'Error！'


class IDValidationError(IDException):
    code = '0'
    message = 'Input Parameters Validation Error！'

class IDMethodNotAllowed(IDException):
    code = '0'
    message = 'Method Not Allowed！'
