from mel.parsing import Grammar
from mel.parsing.symbol import (
    ZeroMany,
    Str,
    Seq,
    OneMany,
    Rule,
    Regex
)


def test_base_string_repetition():
    g = Grammar()
    g.rule('root', ZeroMany(Str('a')))
    g.skip('space', Regex(r'[ \t]+'))
    node = g.parse('  \ta ')
    assert node


def test_base_rule():
    g = Grammar()
    g.rule('root', ZeroMany(Rule('rule')))
    g.rule('rule', Seq(
        Rule('name'), Str('='), Rule('alternative')
    ))
    g.rule('alternative', Seq(
        Rule('sequence'),
        ZeroMany(Seq(Str('|'), Rule('sequence')))
    ))
    g.rule('sequence', OneMany(Rule('name')))
    g.rule('name', Regex(r'[a-z]+'))

    g.skip('space', Regex(r'[ \t]+'))
    g.skip('comment', Regex(r'--[^\n\r]*'))

    node = g.parse('person = john')
    assert node
