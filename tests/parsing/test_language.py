from mel.parsing import Language
from mel.parsing.parsers import (
    IntParser,
    StringParser,
)


def test_hint_map():
    lang = Language()
    assert lang.hint_map.has(IntParser)
    assert lang.hint_map.has(StringParser)
