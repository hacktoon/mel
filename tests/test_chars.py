from infiniscribe.parsing.chars import parse
from infiniscribe.parsing.chars import (
    LOWER, UPPER, DIGIT
)


def fixture_chars(chars):
    return list(parse(chars))


def test_empty_text():
    chars = fixture_chars('')
    assert len(chars) == 0


def test_lower_letters():
    chars = fixture_chars('a')
    assert chars[0].type == LOWER


def test_upper_letters():
    chars = fixture_chars('Y')
    assert chars[0].type == UPPER


def test_digits():
    chars = fixture_chars('5')
    assert chars[0].type == DIGIT