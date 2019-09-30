class MelError(Exception):
    pass


class ParsingError(MelError):
    def __init__(self, token):
        super().__init__()
        self.text = token.text
        self.index = token.index[0]
        self.line = token.line
        self.column = token.column
