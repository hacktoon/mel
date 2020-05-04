from infiniscribe.parsing import Language
from infiniscribe.parsing.stream import Stream
from infiniscribe.parsing.parsers import (
    digit
)


# HELPER FUNCTIONS ==================================

def create_base_lang():
    lang = Language('foo')

    @lang.start(lambda stream: 'start')
    def parse_start(parsed):
        return f'{parsed} node'
    return lang


def as_string(chars):
    return ''.join(char.value for char in chars)


# TESTS ==================================

def test_line_comment():
    lang = create_base_lang()
    assert lang.parse('') == 'start node'


def test_digit_parser():
    parser = digit()
    stream = Stream('545')
    assert as_string(parser(stream)) == '545'
