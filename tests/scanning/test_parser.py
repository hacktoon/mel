import pytest

from mel.scanning.stream import CharStream
from mel.scanning.char import Char
from mel.scanning.parser import (
    Parser,
    ZeroManyParser,
    OneManyParser,
    OptionalParser,
    AlphaParser,
    SeqParser,
    SpaceParser,
    LowerParser,
    UpperParser,
    DigitParser,
    OneOfParser,
    CharParser,
    Produce,
)


CHARS_ABC = [
    Char.build('a'),
    Char.build('b'),
    Char.build('c'),
]

CHARS_DEF = [
    Char.build('d'),
    Char.build('e'),
    Char.build('f'),
]

NAME_PARSER = SeqParser(
    LowerParser(),
    ZeroManyParser(
        OneOfParser(
            CharParser('_'),
            AlphaParser(),
        )
    )
)

INT_PARSER = SeqParser(
    OptionalParser(CharParser('-')),
    DigitParser(),
    ZeroManyParser(
        DigitParser()
    )
)


# ====================================================================
# PRODUCE TESTS
# ====================================================================

def test_produce_length():
    prod2 = Produce(CHARS_ABC)
    assert len(prod2) == len(CHARS_ABC)


def test_produce_string():
    produce = Produce(CHARS_ABC)
    assert str(produce) == 'abc'


def test_produce_repr():
    produce = Produce(CHARS_ABC)
    assert repr(produce) == 'Produce(abc)'


def test_produces_add_length():
    produce = Produce(CHARS_ABC) + Produce(CHARS_DEF)
    assert len(produce) == len(CHARS_ABC) + len(CHARS_DEF)


def test_produces_add_string():
    produce = Produce(CHARS_ABC) + Produce(CHARS_DEF)
    assert str(produce) == 'abcdef'


def test_produces_iadd_length():
    produce = Produce(CHARS_ABC)
    produce += Produce(CHARS_DEF)
    assert len(produce) == len(CHARS_ABC) + len(CHARS_DEF)


def test_produces_iadd_string():
    produce = Produce(CHARS_ABC)
    produce += Produce(CHARS_DEF)
    assert str(produce) == 'abcdef'


# ====================================================================
# PARSER TESTS
# ====================================================================

@pytest.mark.parametrize('text, parsers', [
    ('a', [CharParser('a')]),
    ('b', [CharParser('b')]),
    ('%', [CharParser('%')]),
    ('%', [CharParser()]),
    ('a', [LowerParser(), DigitParser()]),
    ('6', [LowerParser(), CharParser()]),
    ('c', [LowerParser(), DigitParser(), UpperParser()]),
    ('6', [CharParser(), DigitParser(), UpperParser()]),
    ('Z', [LowerParser(), DigitParser(), UpperParser()]),
])
def test_valid_one_of_parser(text, parsers):
    parser = OneOfParser(*parsers)
    stream = CharStream(text)
    production = parser.parse(stream)
    assert str(production) == text
    assert bool(production)


@pytest.mark.parametrize('text, parsers', [
    ('z5', [LowerParser(), DigitParser()]),
    ('a4B', [CharParser(), DigitParser(), UpperParser()]),
    ('caA', [LowerParser(), LowerParser(), UpperParser()]),
    ('*\tA', [CharParser('*'), SpaceParser(), CharParser()]),
    ('$ 6', [CharParser('$'), SpaceParser(), DigitParser()]),
    ('# 6', [CharParser(), SpaceParser(), DigitParser()]),
])
def test_valid_seq_parser(text, parsers):
    parser = SeqParser(*parsers)
    stream = CharStream(text)
    production = parser.parse(stream)
    assert str(production) == text
    assert bool(production)


@pytest.mark.parametrize('text, parser', [
    ('Z', DigitParser()),
    ('', CharParser()),
    ('c', LowerParser()),
    ('C', LowerParser()),
    ('*', CharParser('*')),
    ('$', CharParser('$')),
    ('#', CharParser()),
    ('#', CharParser('#')),
])
def test_valid_optional_parser(text, parser):
    parser = OptionalParser(parser)
    stream = CharStream(text)
    assert parser.parse(stream)


@pytest.mark.parametrize('text, parsers', [
    ('Z5', [LowerParser(), DigitParser()]),
    ('44B', [LowerParser(), DigitParser(), UpperParser()]),
    ('AaA', [LowerParser(), LowerParser(), UpperParser()]),
    ('t\tA', [CharParser('*'), SpaceParser(), UpperParser()]),
    ('a 6', [CharParser('$'), SpaceParser(), DigitParser()]),
])
def test_invalid_seq_parser_returns_nothing(text, parsers):
    parser = SeqParser(*parsers)
    stream = CharStream(text)
    production = parser.parse(stream)
    assert str(production) == ''
    assert not bool(production)


@pytest.mark.parametrize('text, parser', [
    ('', LowerParser()),
    ('auyjhakvgj', LowerParser()),
    ('aZpjJcKvL', OneOfParser(LowerParser(), UpperParser())),
    ('a3r5t6h0k2', SeqParser(LowerParser(), DigitParser())),
    ('', SeqParser(LowerParser(), DigitParser())),
    ('-a -d -b ', SeqParser(CharParser('-'), LowerParser(), SpaceParser())),
])
def test_valid_zeromany_parser(text, parser):
    parser = ZeroManyParser(parser)
    stream = CharStream(text)
    production = parser.parse(stream)
    assert str(production) == text
    assert bool(production)


@pytest.mark.parametrize('text, parser', [
    ('auyjhakvgj', LowerParser()),
    ('aZpjJcKvL', OneOfParser(LowerParser(), UpperParser())),
    ('aZ', OneOfParser(LowerParser(), UpperParser())),
    ('a3r5t6h0k2', SeqParser(LowerParser(), DigitParser())),
    ('a3', SeqParser(LowerParser(), DigitParser())),
    ('-a -d -b ', SeqParser(CharParser('-'), LowerParser(), SpaceParser())),
])
def test_valid_onemany_parser(text: str, parser: Parser):
    parser = OneManyParser(parser)
    stream = CharStream(text)
    production = parser.parse(stream)
    assert str(production) == text
    assert bool(production)


# ====================================================================
# TOKEN TESTS
# ====================================================================

@pytest.mark.parametrize('text, parser', [
    ('auY_jHa', NAME_PARSER),
    ('aB_C2 ', NAME_PARSER),
    ('foobar', NAME_PARSER),
    ('a3r_', NAME_PARSER),
    ('fh44', NAME_PARSER),
    ('a', NAME_PARSER),
    ('2', INT_PARSER),
    ('21115', INT_PARSER),
    ('511', INT_PARSER),
    ('-42', INT_PARSER),
])
def test_valid_token_parser(text: str, parser: Parser):
    stream = CharStream(text)
    production = parser.parse(stream)
    assert text.startswith(str(production))
    assert bool(production)


@pytest.mark.parametrize('text', [
    '$uY_jHa',
    '6B_C2',
    '_3r_',
    '',
])
def test_invalid_name_token_parser(text: str):
    stream = CharStream(text)
    production = NAME_PARSER.parse(stream)
    assert str(production) == ''
    assert not bool(production)
