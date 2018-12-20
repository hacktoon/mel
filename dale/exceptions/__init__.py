class BaseError(Exception):
    pass


class LexingError(BaseError):
    def __init__(self, index=None):
        super().__init__("Invalid syntax")
        self.index = index


class ParsingError(BaseError):
    def __init__(self):
        super().__init__()


class UnexpectedTokenError(LexingError):
    def __init__(self, token):
        message = "Unexpected {!r} token.\n".format(token.id)
        super().__init__(message)
        self.index = token.index[0]


class UnexpectedTokenValueError(LexingError):
    def __init__(self, token):
        tpl = "Found a {!r} token with value {!r}.\n"
        message = tpl.format(token.id, token.value)
        super().__init__(message)
        self.index = token.index[0]


class UnexpectedEOFError(LexingError):
    pass


class ExpectedValueError(ParsingError):
    pass
