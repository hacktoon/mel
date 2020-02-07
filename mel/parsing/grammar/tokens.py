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


class TokenStream:
    def __init__(self, text):
        self.token_map = TokenMap(TOKEN_SPEC)
        self.tokens = self.token_map.tokenize(text)
        self.index = 0

    def read(self, id=''):
        token = self.peek()
        if self.has(id):
            self.index += 1
            return token
        msg = f'Expected token "{id}" but found "{token.id}"'
        raise GrammarError(msg)

    def has(self, id):
        return self.peek().id == id

    def peek(self):
        try:
            return self.tokens[self.index]
        except IndexError:
            return Token('eof', '\0')

    def __getitem__(self, index):
        return self.tokens[index]

    def __len__(self):
        return len(self.tokens)


class TokenMap:
    def __init__(self, spec):
        self.hint_map = TokenHintMap(spec)

    def tokenize(self, text):
        tokens = []
        txt_stream = CharStream(text)
        while not txt_stream.eof:
            (skip, id, pattern, _) = self.hint_map.get(txt_stream.head_char)
            match_text, index = txt_stream.read_pattern(pattern)
            if skip:
                continue
            tokens.append(Token(id, match_text))
        return tokens


class TokenHintMap:
    '''
    FIXME: Currently supports only one token per hint
    '''

    def __init__(self, spec):
        self.map = self._build(spec)
        self.spec = spec

    def _build(self, spec):
        _map = {}

        def _build_hints(index, id, chars):
            for char in chars:
                if char in _map:
                    raise GrammarError(f'Hint already defined: "{id}"')
                _map[char] = index

        for index, (_, id, _, chars) in enumerate(spec):
            _build_hints(index, id, chars)

        return _map

    def get(self, hint):
        try:
            index = self.map[hint]
        except KeyError:
            raise GrammarError(f'Unrecognized hint: "{hint}"')
        return self.spec[index]


class Token:
    def __init__(self, id, text):
        self.id = id
        self.text = text

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({self.id.upper()}, "{self.text}")'
