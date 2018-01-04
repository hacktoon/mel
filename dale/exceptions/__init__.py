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
        super().__init__(template.format(token.eval()))
        self.index = token.index


class UnexpectedTokenError(DaleError):
    def __init__(self, token, allowed_values=None):
        message = 'Found a {!r} token.'.format(token.id)
        if allowed_values:
            message += ' Expected token(s): ' + str(allowed_values)
        super().__init__(message)
        self.index = token.index
