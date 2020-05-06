from infiniscribe.parsing.stream import Stream
from infiniscribe.parsing.parsers import (
    digit
)


def test_digit_parser():
    parser = digit()
    stream = Stream('545')
    match = parser(stream)
    assert str(match) == '5'


def test_digit_parser_wrong_string():
    parser = digit()
    stream = Stream('drfg')
    match = parser(stream)
    assert str(match) == ''
