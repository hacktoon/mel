class DaleError(Exception):
    pass


class BaseError(DaleError):
    def __init__(self, token, msg):
        super().__init__(msg)
        self.text = token.text
        self.index = token.index[0]
        self.line = token.line
        self.column = token.column


class InvalidSyntaxError(BaseError):
    def __init__(self, token):
        super().__init__(token, "This expression is not valid.")


class UnexpectedTokenError(BaseError):
    def __init__(self, token):
        super().__init__(token, "This token is not expected here.")


class UnexpectedEOFError(BaseError):
    def __init__(self, token):
        super().__init__(token, "Reached end of text while parsing.")


class KeywordNotFoundError(BaseError):
    def __init__(self, token):
        super().__init__(token, "Expected a keyword.")


class KeyNotFoundError(BaseError):
    def __init__(self, token):
        super().__init__(token, "Expected a path or ':'.")


class ExpectedValueError(BaseError):
    def __init__(self, token):
        super().__init__(token, "Expected a value.")


class ExpectedKeywordError(BaseError):
    def __init__(self, token):
        super().__init__(token, "Expected a keyword.")


class NameNotFoundError(BaseError):
    def __init__(self, token):
        super().__init__(token, "Expected a name after this symbol.")


class InfiniteRangeError(BaseError):
    def __init__(self, token):
        message = "Expected an integer before or after a range symbol."
        super().__init__(token, message)
