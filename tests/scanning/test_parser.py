from mel.scanning.stream import CharStream
from mel.scanning.char import Char
from mel.scanning.parser import (
    Produce,
    LowerParser,
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
    prod = parser.parse(0, stream)
    assert prod.index == 0
    assert len(prod) == 1


# def test_one_of_parser():
#     parser = OneOfParser(LowerParser())
#     stream = CharStream('abc')
#     prod = parser.parse(0, stream)
#     assert prod.index == 0
