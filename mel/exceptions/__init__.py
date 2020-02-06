class MelError(Exception):
    pass


class GrammarError(Exception):
    pass


class ParsingError(MelError):
    def __init__(self, msg='Parsing error!'):
        super().__init__(msg)
