import pytest

from mel.scanning.stream import CharStream
from mel.scanning.char import Char
from mel.scanning.parser import (
    Parser,
    ZeroManyParser,
    OneManyParser,
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

@pytest.mark.parametrize('value, parsers', [
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
def test_valid_one_of_parser(value, parsers):
    parser = OneOfParser(*parsers)
    stream = CharStream(value)
    production = parser.parse(stream)
    assert str(production) == value
    assert bool(production)


@pytest.mark.parametrize('value, parsers', [
    ('z5', [LowerParser(), DigitParser()]),
    ('a4B', [CharParser(), DigitParser(), UpperParser()]),
    ('caA', [LowerParser(), LowerParser(), UpperParser()]),
    ('*\tA', [CharParser('*'), SpaceParser(), CharParser()]),
    ('$ 6', [CharParser('$'), SpaceParser(), DigitParser()]),
    ('# 6', [CharParser(), SpaceParser(), DigitParser()]),
])
def test_valid_seq_parser(value, parsers):
    parser = SeqParser(*parsers)
    stream = CharStream(value)
    production = parser.parse(stream)
    assert str(production) == value
    assert bool(production)


@pytest.mark.parametrize('value, parsers', [
    ('Z5', [LowerParser(), DigitParser()]),
    ('44B', [LowerParser(), DigitParser(), UpperParser()]),
    ('AaA', [LowerParser(), LowerParser(), UpperParser()]),
    ('t\tA', [CharParser('*'), SpaceParser(), UpperParser()]),
    ('a 6', [CharParser('$'), SpaceParser(), DigitParser()]),
])
def test_invalid_seq_parser_returns_nothing(value, parsers):
    parser = SeqParser(*parsers)
    stream = CharStream(value)
    production = parser.parse(stream)
    assert str(production) == ''
    assert not bool(production)


@pytest.mark.parametrize('value, parser', [
    ('', LowerParser()),
    ('auyjhakvgj', LowerParser()),
    ('aZpjJcKvL', OneOfParser(LowerParser(), UpperParser())),
    ('a3r5t6h0k2', SeqParser(LowerParser(), DigitParser())),
    ('', SeqParser(LowerParser(), DigitParser())),
    ('-a -d -b ', SeqParser(CharParser('-'), LowerParser(), SpaceParser())),
])
def test_valid_zeromany_parser(value, parser):
    parser = ZeroManyParser(parser)
    stream = CharStream(value)
    production = parser.parse(stream)
    assert str(production) == value
    assert bool(production)


@pytest.mark.parametrize('value, parser', [
    ('auyjhakvgj', LowerParser()),
    ('aZpjJcKvL', OneOfParser(LowerParser(), UpperParser())),
    ('aZ', OneOfParser(LowerParser(), UpperParser())),
    ('a3r5t6h0k2', SeqParser(LowerParser(), DigitParser())),
    ('a3', SeqParser(LowerParser(), DigitParser())),
    ('-a -d -b ', SeqParser(CharParser('-'), LowerParser(), SpaceParser())),
])
def test_valid_onemany_parser(value: str, parser: Parser):
    parser = OneManyParser(parser)
    stream = CharStream(value)
    production = parser.parse(stream)
    assert str(production) == value
    assert bool(production)


# ====================================================================
# TOKEN TESTS
# ====================================================================

@pytest.mark.parametrize('value', [
    'auY_jHa',
    'aB_C2 ',
    'foobar',
    'a3r_',
    'fh44',
    'a',
])
def test_valid_name_token_parser(value: str):
    stream = CharStream(value)
    production = NAME_PARSER.parse(stream)
    assert value.startswith(str(production))
    assert bool(production)


@pytest.mark.parametrize('value', [
    '$uY_jHa',
    '6B_C2',
    '_3r_',
    '',
])
def test_invalid_name_token_parser(value: str):
    stream = CharStream(value)
    production = NAME_PARSER.parse(stream)
    assert str(production) == ''
    assert not bool(production)
