class DaleError(Exception):
    pass


class InvalidSyntaxError(DaleError):
    def __init__(self, index):
        self.index = index
        super().__init__("This expression is not valid.")


class UnexpectedTokenError(DaleError):
    def __init__(self, token):
        self.index = token.index[0]
        super().__init__("This token is not expected here.")


class UnexpectedEOFError(DaleError):
    def __init__(self, token):
        self.index = token.index[0]
        super().__init__("Reached end of text while parsing.")


class SubNodeError(DaleError):
    def __init__(self, token):
        self.index = token.index[0]
        super().__init__("Expected an object after this symbol.")


class RelationError(DaleError):
    def __init__(self, token):
        self.index = token.index[0]
        super().__init__("Expected an object to make a relation.")
