from mel.scanning.stream import CharStream
from mel.scanning.parser import (
    LowerParser,
    OneOfParser,
)


# BEGIN  TESTS ==================================

def test_lower_char_parser():
    parser = LowerParser(0)
    stream = CharStream('abc')
    prod = parser.parse(stream)
    assert prod.index == 0


def test_one_of_parser():
    parser = OneOfParser([LowerParser()])
    stream = CharStream('abc')
    prod = parser.parse(stream, 0)
    assert prod.index == 0
