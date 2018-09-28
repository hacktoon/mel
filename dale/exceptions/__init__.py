
class Error(Exception):
    pass


class InvalidSyntaxError(Error):
    def __init__(self, index):
        super().__init__('Invalid syntax')
        self.index = index


class UnexpectedTokenError(Error):
    def __init__(self, token, expected_tokens=None):
        message = 'Found a {!r} token.\n'.format(token.id)
        if expected_tokens:
            message += 'Expected token(s): {!r}'.format(str(expected_tokens))
        super().__init__(message)
        self.index = token.index[0]
