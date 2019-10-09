import pytest

from mel.lexing import TokenStream
# from mel.exceptions import ParsingError


def create_stream(text):
    return TokenStream(text)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("56.75", 56.75),
        ("foo\n / bar", "foo"),
    ],
)
def test_token_value_attribute(test_input, expected):
    tokens = create_stream(test_input)
    assert tokens[0].value == expected
