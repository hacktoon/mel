from mel.lexing.stream import CharStream
from mel.parsing.parsers import (
    IntParser
)


def test_int_parser():
    parser = IntParser()
    stream = CharStream('51')
    match = parser.parse(stream)
    assert str(match) == '51'


def test_int_parser_wrong_text():
    parser = IntParser()
    stream = CharStream('d')
    match = parser.parse(stream)
    assert str(match) == ''
