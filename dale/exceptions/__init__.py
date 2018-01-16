import errno


class DaleError(Exception):
    pass


class InvalidSyntaxError(DaleError):
    def __init__(self, index):
        super().__init__('Invalid syntax')
        self.index = index


class FileError(DaleError):
    def __init__(self, token, original_error):
        if original_error.errno == errno.ENOENT:
            template = 'File {!r} could not be found or doesn\'t exist.'
        elif original_error.errno == errno.EPERM:
            template = 'No permission to open file {!r}.'
        super().__init__(template.format(token.value))
        self.index = token.start


class UnexpectedTokenError(DaleError):
    def __init__(self, token, expected_tokens=None):
        message = 'Found a {!r} token.\n'.format(token.id)
        if expected_tokens:
            message += 'Expected token(s): {!r}'.format(str(expected_tokens))
        super().__init__(message)
        self.index = token.start


class UnexpectedTokenValueError(DaleError):
    def __init__(self, token, expected_tokens=None, expected_values=None):
        tpl = 'Found a {!r} token with value {!r}.\n'
        message = tpl.format(token.id, token.value)
        if expected_tokens:
            message += 'Expected {!r} token(s)'.format(str(expected_tokens))
        if expected_values:
            message += ', with value(s): {!r}'.format(str(expected_values))
        super().__init__(message)
        self.index = token.start


class UnknownReferenceError(DaleError):
    def __init__(self, token):
        message = 'Name {!r} is not defined'.format(token.value)
        super().__init__(message)
        self.index = token.start
