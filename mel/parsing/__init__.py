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

    @property
    def start_symbols(self):
        return next(iter(self.symbols.values()))

    def rule(self, id, *symbols):
        self.symbols[id] = symbols

    def skip(self, id, symbol):
        self.skip_symbols[id] = Skip(symbol)

    def parse(self, text):
        context = Context(
            start_symbols=self.start_symbols,
            skip_symbols=self.skip_symbols,
            symbols=self.symbols,
            stream=Stream(text)
        )
        return Root().parse(context)

    def __repr__(self):
        rules = []

        def repr_symbols(symbols):
            for name, symbols in symbols.items():
                expression = ' '.join([repr(s) for s in symbols])
                rules.append(f'{name} = {expression}')
        repr_symbols(self.symbols)
        # repr_symbols(self.skip_symbols)
        return '\n'.join(rules)
