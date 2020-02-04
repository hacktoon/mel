from .stream import Stream
from .symbol import Root


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

    def rule(self, name, *symbols):
        self.symbols[name] = symbols

    def skip(self, name, *symbols):
        self.skip_symbols[name] = symbols

    def parse(self, text):
        return Root().parse(Context(
            start_symbols=self.start_symbols,
            skip_symbols=self.skip_symbols,
            symbols=self.symbols,
            stream=Stream(text)
        ))

    def __repr__(self):
        rules = []

        def repr_symbols(symbols):
            for name, symbols in symbols.items():
                expression = ' '.join([repr(s) for s in symbols])
                rules.append(f'{name} = {expression}')
        repr_symbols(self.symbols)
        repr_symbols(self.skip_symbols)
        return '\n'.join(rules)
