from mel.languages import Language
from mel.parsing import ParserGenerator, ZeroMany, Seq, OneMany

# TODO: need build the entire grammar tree to "unparse" example from it


def test_base_rule():
    p = ParserGenerator()
    p.rule('root', ZeroMany(p.r('rule')))
    p.rule('rule', Seq(
        p.r('name'), p.s('='), p.r('alternative')
    ))
    p.rule('alternative', Seq(
        p.r('sequence'),
        ZeroMany(p.s('|'), p.r('sequence'))
    ))
    p.rule('sequence', OneMany(p.r('name')))
    p.rule('name', p.p(r'[a-z]+'))

    p.skip('space', r'[ \t]+')
    p.skip('comment', r'--[^\n\r]*')

    lang = Language('Foo', p)
    node = lang.parse('address = end|start about')
    assert node
