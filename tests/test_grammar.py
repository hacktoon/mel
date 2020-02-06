from mel.parsing.grammar import (
    TokenMap,
)


SAMPLE_SPEC = (
    (1, 'name', r'[abc]+', 'abc'),
    (1, 'number', r'[123]+', '123'),
    (0, 'space', r'[ \t]+', ' \t'),
)


def test_token_map():
    token_map = TokenMap(SAMPLE_SPEC)
    (skip, name, pattern, hints) = token_map.get('a')
    assert skip == 1
    assert name == 'name'
    assert hints == 'abc'


def test_token_props():
    text = 'aabc 12'
    token_map = TokenMap(SAMPLE_SPEC)
    tokens = token_map.tokenize(text)
    assert tokens[0].name == 'name'
    assert tokens[0].text == 'aabc'
    assert tokens[1].name == 'number'
    assert tokens[1].text == '12'


def test_lex_skip_space():
    token_map = TokenMap(SAMPLE_SPEC)
    tokens = token_map.tokenize('ab  2')
    assert len(tokens) == 2
