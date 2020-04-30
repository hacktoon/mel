from infiniscribe.parsing.chars import parse
from infiniscribe.parsing.chars import LOWER


def test_empty_text():
    chars = list(parse(''))
    assert len(chars) == 0


def test_lower_letter():
    chars = list(parse('a'))
    assert chars[0].type == LOWER