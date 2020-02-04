from .stream import Stream
from .symbol import Root


# GRAMMAR ==============================================

class Grammar:
    def __init__(self):
        self.rules = {}
        self.skip_rules = {}
        self.start_rule = StartRule('', [])

    def rule(self, name, *symbols):
        self.rules[name] = Rule(name, symbols)

    def start(self, name, *symbols):
        self.start_rule = StartRule(name, symbols)
        self.rule(name, *symbols)

    def skip(self, name, *symbols):
        self.skip_rules[name] = SkipRule(name, symbols)

    def parse(self, text):
        return Root().parse(Context(
            start_rule=self.start_rule,
            skip_rules=self.skip_rules,
            rules=self.rules,
            stream=Stream(text)
        ))

    def __repr__(self):
        rules = {**self.rules, **self.skip_rules}
        return '\n'.join(repr(rule) for rule in rules.values())


class Rule:
    def __init__(self, name, symbols):
        self.name = name
        self.symbols = symbols

    def __repr__(self):
        expression = ' '.join(repr(s) for s in self.symbols)
        return f'{self.name} = {expression}'


class StartRule(Rule):
    pass


class SkipRule(Rule):
    pass


class Context:
    def __init__(self, **kw):
        self.__dict__.update(kw)
