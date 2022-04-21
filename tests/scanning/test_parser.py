import pytest

from mel.scanning.stream import CharStream
from mel.scanning.char import Char
from mel.scanning.parser import (
    Produce,
    CharParser,
    SpaceParser,
    LowerParser,
    DigitParser,
    OneOfParser,
    SeqParser,
    UpperParser,
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


# BEGIN  TESTS ==================================

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


@pytest.mark.parametrize('value, parsers', [
    ('a', [CharParser('a')]),
    ('b', [CharParser('b')]),
    ('%', [CharParser('%')]),
    ('a', [LowerParser(), DigitParser()]),
    ('6', [LowerParser(), DigitParser()]),
    ('c', [LowerParser(), DigitParser(), UpperParser()]),
    ('6', [LowerParser(), DigitParser(), UpperParser()]),
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
    ('a4B', [LowerParser(), DigitParser(), UpperParser()]),
    ('caA', [LowerParser(), LowerParser(), UpperParser()]),
    ('*\tA', [CharParser('*'), SpaceParser(), UpperParser()]),
    ('$ 6', [CharParser('$'), SpaceParser(), DigitParser()]),
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
