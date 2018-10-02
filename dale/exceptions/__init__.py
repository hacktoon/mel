
class Error(Exception):
    pass


class LexingError(Error):
    def __init__(self, index):
        super().__init__('Invalid syntax')
        self.index = index


class UnexpectedTokenError(LexingError):
    def __init__(self, token, expected_tokens=None):
        message = 'Found a {!r} token.\n'.format(token.id)
        if expected_tokens:
            message += 'Expected token(s): {!r}'.format(str(expected_tokens))
        super().__init__(message)
        self.index = token.index[0]


class UnexpectedTokenValueError(LexingError):
    def __init__(self, token, expected_tokens=None, expected_values=None):
        tpl = 'Found a {!r} token with value {!r}.\n'
        message = tpl.format(token.id, token.value)
        if expected_tokens:
            message += 'Expected {!r} token(s)'.format(str(expected_tokens))
        if expected_values:
            message += ', with value(s): {!r}'.format(str(expected_values))
        super().__init__(message)
        self.index = token.index[0]


class ParsingError(Error):
    def __init__(self):
        super().__init__()


class ExpectedValueError(ParsingError):
    pass
