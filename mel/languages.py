from .parsing import Grammar, Parser


# BUILT-IN LANGUAGE BASED ON GRAMMAR BELOW


class MetaLanguage:
    def __init__(self):
        self.grammar = self._build_grammar()
        self.parser = Parser(self.grammar)

    def parse(self, text):
        return self.parser.parse(text)

    def persist_node(self):
        pass

    def _build_grammar(self):
        g = Grammar()

        # root        = rule*
        g.root(g.zero_many('rule'))

        # rule        = prefix? NAME '=' alternative ( NEWLINE | EOF )
        g.rule('rule', g.seq(
            g.opt('prefix'),
            g.r('name'),
            g.s('='),
            g.r('alternative')
        ))

        # prefix      = '-' | '@'
        g.rule('prefix', g.p(r'[@-]'))

        # alternative = sequence ( '|' sequence )*
        g.rule('alternative', g.seq(
            g.r('sequence'),
            g.zero_many(g.s('|'), g.r('sequence'))
        ))

        # sequence    = atom+
        g.rule('sequence', g.one_many('atom'))

        # atom        = ( PATTERN | STRING | NAME ) quantifier?
        g.rule('atom', g.seq(
            g.one_of(g.r('pattern'), g.r('string'), g.r('name'), g.r('group')),
            g.opt('quantifier')
        ))

        # group       = '(' alternative ')'
        g.rule('group', g.seq(
            g.s('('), g.r('alternative'), g.s(')')
        ))

        # quantifier  = '*' | '+' | '?'
        g.rule('quantifier', g.p(r'[*?+]'))

        g.rule('name', g.p(r'[a-z]+'))
        g.rule('pattern', g.p(r'/[^/]+/'))
        g.rule('string', g.p(r"'[^']+'"))

        return g
