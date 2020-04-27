from infiniscribe.parsing.grammar.tokens import (
    TokenHintMap,
    TokenStream,
)


SAMPLE_SPEC = (
    (1, 'name', r'[abc]+', 'abc'),
    (1, 'number', r'[123]+', '123'),
    (0, 'space', r'[ \t]+', ' \t'),
)


def test_token_hint_map_get():
    hint_map = TokenHintMap(SAMPLE_SPEC)
    (skip, id, _, hints) = hint_map.get('a')
    assert skip == 1
    assert id == 'name'
    assert hints == 'abc'


def test_token_props():
    stream = TokenStream('aabc =')
    assert stream[0].id == 'name'
    assert stream[0].text == 'aabc'
    assert stream[1].id == '='
    assert stream[1].text == '='


def test_lex_skip_space():
    stream = TokenStream('ab def')
    assert len(stream) == 2


# PARSING TESTS

# def test_parse_modifier():
#     for id in '?+*':
#         stream = TokenStream('?')
#         assert parse_modifier(stream)
