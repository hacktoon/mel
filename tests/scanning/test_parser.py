from mel.scanning.stream import CharStream
from mel.scanning.parser import LowerParser


# BEGIN  TESTS ==================================

def test_lower_char_parser():
    parser = LowerParser(0)
    stream = CharStream('abc')
    prod = parser.parse(stream)
    assert prod
