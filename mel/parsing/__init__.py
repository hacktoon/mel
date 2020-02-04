from .stream import Stream
from .symbol import Root


# GRAMMAR ==============================================

class Grammar:
    def __init__(self):
        self.rules = {}
        self.skip_rules = {}

    @property
    def start_rule(self):
        return next(iter(self.rules.values()))

    def rule(self, name, *symbols):
        self.rules[name] = Rule(name, symbols)

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
        lines = []

        def repr_rules(rules):
            for name, rules in rules.items():
                expression = ' '.join([repr(s) for s in rules])
                lines.append(f'{name} = {expression}')
        repr_rules(self.rules)
        repr_rules(self.skip_rules)
        return '\n'.join(lines)


class Rule:
    def __init__(self, name, symbols):
        self.name = name
        self.symbols = symbols


class SkipRule(Rule):
    pass


class Context:
    def __init__(self, **kw):
        self.__dict__.update(kw)
