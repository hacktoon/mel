import errno


class DaleError(Exception):
    pass


class LexingError(DaleError):
    pass


class ParsingError(DaleError):
    pass


class FileError(DaleError):
    def __init__(self, token, original_error):
        if original_error.errno == errno.ENOENT:
            template = 'File {!r} could not be found or doesn\'t exist.'
        elif original_error.errno == errno.EPERM:
            template = 'No permission to open file {!r}.'
        super().__init__(template.format(token.value))
        self.index = token.index


class UnexpectedTokenError(DaleError):
    def __init__(self, token, allowed_values=None):
        message = 'Expected a token of type {!r}.'.format(token.id)
        if allowed_values:
            message += ' Accepted type(s): ' + str(allowed_values)
        super().__init__(message)
        self.index = token.index
