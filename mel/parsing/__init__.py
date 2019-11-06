from .grammar import mel_grammar


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, stream):
        return self.grammar.parse(stream)


class MelParser(Parser):
    def __init__(self):
        super().__init__(mel_grammar)
