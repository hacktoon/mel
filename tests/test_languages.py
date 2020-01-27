from mel.languages import Language
from mel.parsing import Grammar, zero_many, seq, one_many

# TODO: need build the entire grammar tree to "unparse" example from it


def test_base_rule():
    g = Grammar()
    g.rule('root', zero_many(g.r('rule')))
    g.rule('rule', seq(
        g.r('name'), g.s('='), g.r('alternative')
    ))
    g.rule('alternative', seq(
        g.r('sequence'),
        zero_many(g.s('|'), g.r('sequence'))
    ))
    g.rule('sequence', one_many(g.r('name')))
    g.rule('name', g.p(r'[a-z]+'))

    g.skip('space', r'[ \t]+')
    g.skip('comment', r'--[^\n\r]*')

    lang = Language('Foo', g)
    node = lang.parse('address = end|start about')
    assert node
