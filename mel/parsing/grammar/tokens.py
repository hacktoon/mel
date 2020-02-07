import string

from ...exceptions import GrammarError
from ..stream import CharStream


TOKEN_SPEC = (
    (0, 'token',     r'[-A-Z]+\b',          string.ascii_uppercase),
    (0, 'name',      r'[-a-z]+\b',          string.ascii_lowercase),
    (0, 'eol',       r'[\r\n;]+',           '\r\n;'),
    (1, 'space',     r'[ \t]+',             ' \t'),
    (0, 'string',    r"'[^']*'|\"[^\"]*\"", "'\""),
    (1, 'comment',   r'#[^\r\n]*',          '#'),
    (0, 'meta',      r'@',                  '@'),
    (0, '=',         r'=',                  '='),
    (0, '*',         r'\*',                 '*'),
    (0, '+',         r'\+',                 '+'),
    (0, '?',         r'\?',                 '?'),
    (0, '(',         r'\(',                 '('),
    (0, ')',         r'\)',                 ')'),
    (0, '[',         r'\[',                 '['),
    (0, ']',         r'\]',                 ']'),
    (0, '|',         r'\|',                 '|'),
)


class TokenHintMap:
    '''
    FIXME: Currently supports only one token per hint
    '''

    def __init__(self, spec):
        self.map = self._build(spec)
        self.spec = spec

    def _build(self, spec):
        _map = {}

        def _build_hints(index, name, chars):
            for char in chars:
                if char in _map:
                    raise GrammarError(f'Hint already defined: "{name}"')
                _map[char] = index

        for index, (_, name, _, chars) in enumerate(spec):
            _build_hints(index, name, chars)

        return _map

    def get(self, hint):
        try:
            index = self.map[hint]
        except KeyError:
            raise GrammarError(f'Unrecognized hint: "{hint}"')
        return self.spec[index]


class TokenMap:
    def __init__(self):
        self.hint_map = TokenHintMap(TOKEN_SPEC)

    def tokenize(self, text):
        tokens = []
        txt_stream = CharStream(text)
        while not txt_stream.eof:
            (skip, name, pattern, _) = self.hint_map.get(txt_stream.head_char)
            match_text, index = txt_stream.read_pattern(pattern)
            if skip:
                continue
            tokens.append(Token(name, match_text))
        return tokens


class Token:
    def __init__(self, name, text):
        self.name = name
        self.text = text

    def __repr__(self):
        return f'Token({self.name}, "{self.text}")'


class TokenStream:
    def __init__(self, text):
        self.token_map = TokenMap()
        self.tokens = self.token_map.tokenize(text)
        self.text = text
        self.index = 0

    def read(self, name=''):
        token = self.read_stream()
        if name and not self.peek(name):
            msg = f'Expected token "{name}" but found "{token}"'
            raise GrammarError(msg)
        self.index += 1
        return token

    def peek(self, name):
        token = self.read_stream()
        return token.name == name

    def read_stream(self):
        try:
            token = self.tokens[self.index]
        except IndexError:
            return Token('eof', '')
        return token

    def __getitem__(self, index):
        return self.tokens[index]

    def __len__(self):
        return len(self.tokens)
