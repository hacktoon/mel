from mel.parsing import Grammar
from mel.parsing.symbol import (
    ZeroMany,
    Str,
    OneMany,
    Sym,
    Opt,
    Regex
)


def test_base_string_repetition():
    g = Grammar()
    g.start('root', ZeroMany(Str('a')))
    g.skip('space', Regex(r'[ \t]+'))
    node = g.parse('  \ta ')
    assert node


def test_skip_parse_multi_symbols():
    g = Grammar()
    g.start('root', ZeroMany(Str('a')))
    g.skip('space', Regex(r'[ \t]+'), Str(';'))
    node = g.parse('  \t;a  ;a    ;')
    assert node


def test_opt():
    g = Grammar()
    g.start('root', Opt(Str('a'), Regex(r'[a-z]')))
    node = g.parse('ag')
    assert node
    node = g.parse('aa')
    assert node
    node = g.parse('')
    assert node


def test_complete_grammar():
    g = Grammar()

    g.start('root', ZeroMany(Sym('rule')))

    g.rule('rule', Sym('name'), Str('='), Sym('alternative'))
    g.rule('alternative', Sym('sequence'), ZeroMany(
        Str('|'),
        Sym('sequence')
    ))
    g.rule('sequence', OneMany(Sym('name')))
    g.rule('name', Regex(r'[a-z]+'))

    g.skip('space', Regex(r'[ \t]+'))
    g.skip('comment', Regex(r'--[^\n\r]*'))

    node = g.parse('person = john')

    assert node
