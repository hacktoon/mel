import string

from ..exceptions import GrammarError
from .stream import Stream


TOKEN_SPEC = (
    (0, 'token',         r'[-A-Z]+\b',   string.ascii_uppercase),
    (0, 'rule',          r'[-a-z]+\b',   string.ascii_lowercase),
    (1, 'eol',           r"[\r\n;]+",    '\r\n;'),
    (1, 'space',         r"[ \t]*",      ' \t'),
    (0, 'meta rule',     r'@[a-z]+\b',   '@'),
    (1, 'comment',       r'#[^\r\n]*',   '#'),
    (0, 'single string', r"'[^'\r\n]*'", "'"),
    (0, 'double string', r'"[^"\r\n]*"', '"'),
    (0, '*',             r'\*',          '*'),
    (0, '+',             r'\+',          '+'),
    (0, '?',             r'\?',          '?'),
    (0, '(',             r'\(',          '('),
    (0, ')',             r'\)',          ')'),
    (0, '[',             r'\[',          '['),
    (0, ']',             r'\]',          ']'),
    (0, '|',             r'\|',          '|'),
    (0, '=',             r'=',           '='),
)


class TokenMap:
    def __init__(self, spec):
        self.map = self._build_map(spec)
        self.spec = spec

    def _build_map(self, spec):
        _map = {}
        for index, (_, name, _, hints) in enumerate(spec):
            for char in hints:
                if char in _map:
                    raise GrammarError(f'Token already defined: "{name}"')
                _map[char] = index
        return _map

    def tokenize(self, text):
        tokens = []
        stream = Stream(text)
        while not stream.eof:
            (skip, name, pattern, _) = self.get(char=stream.head[0])
            match_text, index = stream.read_pattern(pattern)
            if skip:
                tokens.append(Token(name, match_text))
        return tokens

    def get(self, char):
        index = self._get(char)
        return self.spec[index]

    def _get(self, char):
        try:
            return self.map[char]
        except KeyError:
            raise GrammarError(f'Unrecognized character: "{char}"')


class Token:
    def __init__(self, name, text):
        self.name = name
        self.text = text

    def __repr__(self):
        return f'Token({self.name}, "{self.text}")'


def parse(text):
    token_map = TokenMap(TOKEN_SPEC)
    tokens = token_map.tokenize(text)
    return parse_rules(token_map, tokens)


def parse_rules(token_map, tokens):
    return tokens


def parse_rule(token_map, tokens):
    return tokens
