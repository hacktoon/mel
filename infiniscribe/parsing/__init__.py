# from .stream import CharStream
# from .symbol import Start, Regex


# RULES = (
#     # First line is the start rule
#     # RULE         PARSER    EXPANSION
#     ('grammar',    '*',      '@rule'),
#     ('rule',       'SEQ',    '@rule-type', '@rule-name', '=', '@alt', 'eol'),
#     ('rule-name',  'ALT',    'name', 'token'),
#     ('rule-type',  '?/ALT',  '/', '-'),
#     ('alt',        'SEQ',    '@seq', '@alt-tail'),
#     ('alt-tail',   '*/SEQ',  '|', '@seq'),
#     ('seq',        '+',      '@atom'),
#     ('atom',       'SEQ',    '@atom-head', '@modifier'),
#     ('atom-head',  'ALT',    '@group', 'name', 'token', 'string'),
#     ('group',      'SEQ',    '(', '@alt', ')'),
#     ('modifier',   '?/ALT',  '*', '?', '+'),
# )


# # GRAMMAR ==============================================

# class Grammar:
#     def __init__(self):
#         self.rules = {}
#         self.tokens = {}
#         self.skip_rules = {}
#         self.start_rule = Start([])

#     def rule(self, name, *symbols):
#         self.rules[name] = Rule(symbols)

#     def token(self, name, string):
#         self.tokens[name] = Regex(string)

#     def start(self, name, *symbols):
#         self.start_rule = Start(*symbols)
#         self.rule(name, *symbols)

#     def skip(self, name, *symbols):
#         self.skip_rules[name] = SkipRule(symbols)

#     def parse(self, text):
#         return self.start_rule.parse(Context(
#             start_rule=self.start_rule,
#             skip_rules=self.skip_rules,
#             rules=self.rules,
#             stream=CharStream(text)
#         ))

#     def __repr__(self):
#         rules = {**self.rules, **self.skip_rules}
#         return '\n'.join(repr(rule) for rule in rules.values())


# class Rule:
#     def __init__(self, symbols):
#         self.symbols = symbols

#     def __repr__(self):
#         expression = ' '.join(repr(s) for s in self.symbols)
#         return f'{self.name} = {expression}'


# class SkipRule(Rule):
#     pass


# class Context:
#     def __init__(self, **kw):
#         self.__dict__.update(kw)
