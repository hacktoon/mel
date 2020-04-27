class BaseError(Exception):
    pass


class LexingError(Exception):
    pass


class ParsingError(BaseError):
    def __init__(self, msg='Parsing error!'):
        super().__init__(msg)
