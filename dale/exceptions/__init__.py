class BaseError(Exception):
    pass


class LexingError(BaseError):
    pass


class ParsingError(BaseError):
    pass


class UnexpectedTokenError(LexingError):
    pass


class UnexpectedEOFError(LexingError):
    pass


class ExpectedValueError(ParsingError):
    pass
