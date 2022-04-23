import pytest

from mel.scanning.stream import CharStream
from mel.scanning.parser.base import Parser
from mel.scanning.parser.single import (
    ZeroManyParser,
    OneManyParser,
    OptionalParser,
)
from mel.scanning.parser.multi import (
    SeqParser,
    OneOfParser,
)
from mel.scanning.parser.char import (
    CharParser,
    NotCharParser,
    AlphaNumParser,
    SpaceParser,
    LowerParser,
    UpperParser,
    DigitParser,
)


NAME_PARSER = SeqParser(
    LowerParser(),
    ZeroManyParser(
        OneOfParser(
            CharParser('_'),
            AlphaNumParser(),
        )
    )
)


INT_PARSER = SeqParser(
    OptionalParser(CharParser('-')),
    DigitParser(),
    ZeroManyParser(
        DigitParser()
    )
)


# ====================================================================
# PARSER TESTS
# ====================================================================
@pytest.mark.parametrize('text, parser', [
    ('Z', DigitParser()),
    ('5', UpperParser()),
    ('2', LowerParser()),
    ('a', LowerParser()),
])
def test_valid_not_parser(text, parser):
    parser = NotCharParser(parser)
    stream = CharStream(text)
    produce = parser.parse(stream)
    assert str(produce) == ''
    assert produce


@pytest.mark.parametrize('text, parsers', [
    ('a', [CharParser('a')]),
    ('b', [CharParser('b')]),
    ('%', [CharParser('%')]),
    ('%', [CharParser()]),
    ('a', [LowerParser(), DigitParser()]),
    ('6', [LowerParser(), CharParser()]),
    ('c', [LowerParser(), DigitParser(), UpperParser()]),
    ('6', [CharParser(), DigitParser(), UpperParser()]),
    ('Z', [LowerParser(), DigitParser(), UpperParser()]),
])
def test_valid_one_of_parser(text, parsers):
    parser = OneOfParser(*parsers)
    stream = CharStream(text)
    production = parser.parse(stream)
    assert str(production) == text
    assert production


@pytest.mark.parametrize('text, parser', [
    ('Z', DigitParser()),
    ('', CharParser()),
    ('c', LowerParser()),
    ('C', LowerParser()),
    ('*', CharParser('*')),
    ('$', CharParser('$')),
    ('#', CharParser()),
    ('#', CharParser('#')),
])
def test_valid_optional_parser(text, parser):
    parser = OptionalParser(parser)
    stream = CharStream(text)
    assert parser.parse(stream)


@pytest.mark.parametrize('text, parsers', [
    ('z5', [LowerParser(), DigitParser()]),
    ('a4B', [CharParser(), DigitParser(), UpperParser()]),
    ('caA', [LowerParser(), LowerParser(), UpperParser()]),
    ('*\tA', [CharParser('*'), SpaceParser(), CharParser()]),
    ('$ 6', [CharParser('$'), SpaceParser(), DigitParser()]),
    ('# 6', [CharParser(), SpaceParser(), DigitParser()]),
])
def test_valid_seq_parser(text, parsers):
    parser = SeqParser(*parsers)
    stream = CharStream(text)
    production = parser.parse(stream)
    assert str(production) == text
    assert production


@pytest.mark.parametrize('text, parsers', [
    ('Z5', [LowerParser(), DigitParser()]),
    ('44B', [LowerParser(), DigitParser(), UpperParser()]),
    ('AaA', [LowerParser(), LowerParser(), UpperParser()]),
    ('t\tA', [CharParser('*'), SpaceParser(), UpperParser()]),
    ('a 6', [CharParser('$'), SpaceParser(), DigitParser()]),
])
def test_invalid_seq_parser_returns_nothing(text, parsers):
    parser = SeqParser(*parsers)
    stream = CharStream(text)
    production = parser.parse(stream)
    assert str(production) == ''
    assert not production


@pytest.mark.parametrize('text, parser', [
    ('', LowerParser()),
    ('auyjhakvgj', LowerParser()),
    ('aZpjJcKvL', OneOfParser(LowerParser(), UpperParser())),
    ('a3r5t6h0k2', SeqParser(LowerParser(), DigitParser())),
    ('', SeqParser(LowerParser(), DigitParser())),
    ('-a -d -b ', SeqParser(CharParser('-'), LowerParser(), SpaceParser())),
])
def test_valid_zeromany_parser(text, parser):
    parser = ZeroManyParser(parser)
    stream = CharStream(text)
    production = parser.parse(stream)
    assert str(production) == text
    assert production


@pytest.mark.parametrize('text, parser', [
    ('auyjhakvgj', LowerParser()),
    ('aZpjJcKvL', OneOfParser(LowerParser(), UpperParser())),
    ('aZ', OneOfParser(LowerParser(), UpperParser())),
    ('a3r5t6h0k2', SeqParser(LowerParser(), DigitParser())),
    ('a3', SeqParser(LowerParser(), DigitParser())),
    ('-a -d -b ', SeqParser(CharParser('-'), LowerParser(), SpaceParser())),
])
def test_valid_onemany_parser(text: str, parser: Parser):
    parser = OneManyParser(parser)
    stream = CharStream(text)
    production = parser.parse(stream)
    assert str(production) == text
    assert production


# ====================================================================
# TOKEN TESTS
# ====================================================================

@pytest.mark.parametrize('text, parser', [
    ('auY_jHa', NAME_PARSER),
    ('aB_C2 ', NAME_PARSER),
    ('foobar', NAME_PARSER),
    ('a3r_', NAME_PARSER),
    ('fh44', NAME_PARSER),
    ('a', NAME_PARSER),
    ('2', INT_PARSER),
    ('21115', INT_PARSER),
    ('511', INT_PARSER),
    ('-42', INT_PARSER),
])
def test_valid_token_parser(text: str, parser: Parser):
    stream = CharStream(text)
    production = parser.parse(stream)
    assert text.startswith(str(production))
    assert production


@pytest.mark.parametrize('text, parser', [
    ('$uY_jHa', NAME_PARSER),
    ('6B_C2', NAME_PARSER),
    ('_3r_', NAME_PARSER),
    ('', NAME_PARSER),
    ('', INT_PARSER),
    ('a', INT_PARSER),
])
def test_invalid_token_parser(text: str, parser: Parser):
    stream = CharStream(text)
    production = parser.parse(stream)
    assert str(production) == ''
    assert not production
