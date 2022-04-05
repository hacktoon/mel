from mel.scanning.stream import CharStream
from mel.parsing.parsers import (
    IntParser
)


# def test_int_parser():
#     parser = IntParser()
#     stream = CharStream('51')
#     match = parser.parse(stream)
#     assert str(match) == '51'
#     assert stream.eof


# def test_int_parser_not_eof():
#     parser = IntParser()
#     stream = CharStream('3d')
#     match = parser.parse(stream)
#     assert str(match) == '3'
#     assert not stream.eof


# def test_int_parser_wrong_text():
#     parser = IntParser()
#     stream = CharStream('d')
#     match = parser.parse(stream)
#     assert str(match) == ''
