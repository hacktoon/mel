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


class SubNodeError(DaleError):
    def __init__(self, index):
        self.index = index
        super().__init__("An object is expected after a slash.")


class NameNotFoundError(DaleError):
    def __init__(self, index):
        self.index = index
        super().__init__("A name is expected after a property prefix.")
