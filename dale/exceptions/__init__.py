class DaleError(Exception):
    pass


class InvalidSyntaxError(DaleError):
    def __init__(self, index):
        self.index = index
        super().__init__("This expression is not valid.")


class UnexpectedTokenError(DaleError):
    def __init__(self, index):
        self.index = index
        super().__init__("This token is not expected here.")


class ValueChainError(DaleError):
    def __init__(self, index):
        self.index = index
        super().__init__("A value is expected after a chain separator.")
