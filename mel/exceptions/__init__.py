class MelError(Exception):
    pass


class ParsingError(Exception):
    pass


class LexingError(MelError):
    def __init__(self, token, msg):
        super().__init__(msg)
        self.text = token.text
        self.index = token.index[0]
        self.line = token.line
        self.column = token.column


class InvalidSyntaxError(LexingError):
    def __init__(self, token):
        super().__init__(token, "This expression is not valid.")


class UnexpectedTokenError(LexingError):
    def __init__(self, token):
        super().__init__(token, "This token is not expected here.")


class EOFError(LexingError):
    def __init__(self, token):
        super().__init__(token, "Reached end of text while parsing.")


class KeywordNotFoundError(LexingError):
    def __init__(self, token):
        super().__init__(token, "Expected a keyword.")


class KeyNotFoundError(LexingError):
    def __init__(self, token):
        super().__init__(token, "Expected a path or ':'.")


class ExpectedValueError(LexingError):
    def __init__(self, token):
        super().__init__(token, "Expected a value.")


class ExpectedKeywordError(LexingError):
    def __init__(self, token):
        super().__init__(token, "Expected a keyword.")


class NameNotFoundError(LexingError):
    def __init__(self, token):
        super().__init__(token, "Expected a name after this symbol.")


class InfiniteRangeError(LexingError):
    def __init__(self, token):
        message = "Expected an integer before or after a range symbol."
        super().__init__(token, message)
