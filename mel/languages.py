from .parsing import Stream, Grammar, Parser


def build_grammar(g):

    # root  =  rule*
    # g.root(g.zero_many(g.r('rule')))

    # # rule  =  rule-id '=' alternative
    # g.rule('rule', g.seq(
    #     g.p('[a-z]+'), g.s('='), g.p(r'[0-9]+')
    # ))

    # g.rule('alternative', g.r('int'))
    # g.rule('int', g.p(r'[0-9]+'))

    # # alternative  =  sequence ( '|' sequence )*
    # g.rule('alternative', g.seq(
    #     g.r('sequence'),
    #     g.zero_many(g.s('|'), g.r('sequence'))
    # ))

    # # sequence  =  atom+
    # g.rule('sequence', g.one_many('atom'))

    # # atom  =  ( PATTERN | STRING | NAME ) quantifier?
    # g.rule('atom', g.seq(
    #     g.one_of(
    #           g.r('pattern'), g.r('string'),
    #           g.r('name'), g.r('group')),
    #     g.opt('quantifier')
    # ))

    # # group  =  '(' alternative ')'
    # g.rule('group', g.seq(
    #     g.s('('), g.r('alternative'), g.s(')')
    # ))

    # # quantifier  =  '.*' | '_*' | '*' | '+' | '?'
    # g.rule('quantifier', g.p(r'[*?+]'))

    # g.rule('name', g.p(r'[a-z]+'))
    # g.rule('pattern', g.p(r'/[^/]+/'))
    # g.rule('string', g.p(r"'[^']+'"))

    return g


class Language:
    def __init__(self, name, grammar):
        self.name = name
        self.grammar = build_grammar(grammar)

    def parse(self, text):
        stream = Stream(text)
        return self.grammar.match(stream)

    def generate(self, options=None):
        return options

    def __repr__(self):
        return f"{self.name} language"
