

class DaleError(Exception):
    pass


class LexingError(DaleError):
    pass


class ParsingError(DaleError):
    pass


class UnexpectedValueError(DaleError):
    def __init__(self, expected, found):
        template = 'expected a token of type {!r}, but found {!r}'
        super().__init__(template.format(expected, found))
