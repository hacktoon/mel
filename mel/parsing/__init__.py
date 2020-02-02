from .stream import Stream
from .symbol import Root, Skip


# GRAMMAR ==============================================

class Context:
    def __init__(self, **kw):
        self.__dict__.update(kw)


class Grammar:
    def __init__(self):
        self.symbols = {}
        self.skip_symbols = {}

    def rule(self, id, symbol):
        self.symbols[id] = symbol

    def skip(self, id, symbol):
        self.skip_symbols[id] = Skip(symbol)

    def parse(self, text):
        context = Context(
            skip_symbols=self.skip_symbols,
            symbols=self.symbols,
            stream=Stream(text)
        )
        return Root().parse(context)
