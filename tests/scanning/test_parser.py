import pytest

from mel.scanning.stream import CharStream
from mel.scanning.char import Char
from mel.scanning.parser import (
    Produce,
    LowerParser,
    DigitParser,
    OneOfParser,
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


def test_lower_char_parser():
    parser = LowerParser()
    stream = CharStream('a')
    prod = parser.parse(stream)
    assert prod.index == 0
    assert len(prod) == 1


def test_valid_one_of_parser():
    parser = OneOfParser(LowerParser())
    stream = CharStream('a')
    prod = parser.parse(stream)
    assert prod.index == 0


def test_invalid_one_of_parser():
    parser = OneOfParser(LowerParser())
    stream = CharStream('2')
    production = parser.parse(stream)
    assert not bool(production)


@pytest.mark.parametrize('value', 'a3c90z7')
def test_valid_one_of_parser_lower_int(value):
    parser = OneOfParser(LowerParser(), DigitParser())
    stream = CharStream(value)
    production = parser.parse(stream)
    assert str(production) == value
    assert bool(production)
