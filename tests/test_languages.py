from mel.languages import Language
from mel.parsing import Grammar

# TODO: need build the entire grammar tree to "unparse" example from it


def test_base_rule():
    g = Grammar()
    g.rule('root', g.zero_many(g.r('rule')))
    g.rule('rule', g.seq(
        g.r('name'), g.s('='), g.r('alternative'), g.s(';')
    ))
    g.rule('alternative', g.seq(
        g.r('sequence'),
        g.zero_many(g.s('|'), g.r('sequence'))
    ))
    g.rule('sequence', g.zero_many(g.r('name')))
    g.rule('name', g.p(r'[a-z]+'))

    g.skip('space', r'[ \t]+')
    g.skip('comment', r'--[^\n\r]*')

    lang = Language('Foo', g)
    node = lang.parse('address = street num; x = app;')

    assert node
