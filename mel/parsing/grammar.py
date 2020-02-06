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
            (skip, name, pattern, _) = self.get_by_hint(stream.head[0])
            match_text, index = stream.read_pattern(pattern)
            if skip:
                tokens.append(Token(name, match_text))
        return TokenStream(tokens)

    def get_by_hint(self, char):
        try:
            index = self.map[char]
        except KeyError:
            raise GrammarError(f'Unrecognized character: "{char}"')
        return self.spec[index]


class Token:
    def __init__(self, name, text):
        self.name = name
        self.text = text

    def __repr__(self):
        return f'Token({self.name}, "{self.text}")'


class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def get(self):
        token = self.tokens[self.index]
        self.index += 1
        return token

    def __getitem__(self, index):
        return self.tokens[index]

    def __len__(self):
        return len(self.tokens)


def parse(text):
    token_map = TokenMap(TOKEN_SPEC)
    tokens = token_map.tokenize(text)
    return parse_rules(token_map, tokens)


def parse_rules(token_map, tokens):
    return tokens


def parse_rule(token_map, tokens):
    return tokens
