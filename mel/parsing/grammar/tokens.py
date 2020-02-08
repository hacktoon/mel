import string

from ...exceptions import GrammarError
from ..stream import CharStream


TOKEN_SPEC = (
    # ID         SKIP  PATTERN                 HINT
    ('token',    0,    r'[-A-Z]+\b',           string.ascii_uppercase),
    ('name',     0,    r'[-a-z]+\b',           string.ascii_lowercase),
    ('eol',      0,    r'[\r\n;]+',            '\r\n;'),
    ('space',    1,    r'[ \t]+',              ' \t'),
    ('string',   0,    r"'[^']*'|\"[^\"]*\"",  "'\""),
    ('comment',  1,    r'#[^\r\n]*',           '#'),
    ('meta',     0,    r'@',                   '@'),
    ('=',        0,    r'=',                   '='),
    ('*',        0,    r'\*',                  '*'),
    ('+',        0,    r'\+',                  '+'),
    ('?',        0,    r'\?',                  '?'),
    ('(',        0,    r'\(',                  '('),
    (')',        0,    r'\)',                  ')'),
    ('[',        0,    r'\[',                  '['),
    (']',        0,    r'\]',                  ']'),
    ('|',        0,    r'\|',                  '|'),
)


class TokenStream:
    def __init__(self, text):
        self.tokens = tokenize(TOKEN_SPEC, text)
        self.index = 0

    def read(self, id):
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
        for index, (id, _, _, chars) in enumerate(spec):
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


def tokenize(spec, text):
    tokens = []
    hint_map = TokenHintMap(spec)
    txt_stream = CharStream(text)
    while not txt_stream.eof:
        (id, skip, pattern, _) = hint_map.get(txt_stream.head_char)
        match_text, index = txt_stream.read_pattern(pattern)
        if skip:
            continue
        tokens.append(Token(id, match_text))
    return tokens
