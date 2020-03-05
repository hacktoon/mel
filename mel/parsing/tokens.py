import string

from ...exceptions import LexingError
from ..stream import CharStream


TOKEN_SPEC = (
    # Priority is defined by declaration order
    # ID          PATTERN                HINT
    ('space',     r'[,\s]+',             string.whitespace + ','),
    ('comment',   r'--[^\r\n]*',         '-'),
    ('concept',   r'[A-Z][_A-Z]+',       string.ascii_uppercase),
    ('name',      r'[a-z][_a-z]+',       string.ascii_lowercase),
    ('float',     r'-?[0-9](.[0-9]+)?',  string.digits + '-'),
    ('int',       r'-?[0-9]+',           string.digits + '-'),
    ('string',    r"'[^']*'",            "'"),
    ('template',  r'"[^"]*"',            '"'),
    (':',         r':',                  ':'),
    ('?:',        r'\?:',                '?'),
    ('%:',        r'%:',                 '%'),
    ('..',        r'\.\.',               '.'),
    ('.',         r'\.',                 '.'),
    ('/',         r'/',                  '/'),
    ('=',         r'=',                  '='),
    ('!=',        r'!=',                 '!'),
    ('<>',        r'<>',                 '<'),
    ('><',        r'><',                 '>'),
    ('<=',        r'<=',                 '<'),
    ('>=',        r'>=',                 '>'),
    ('>',         r'>',                  '>'),
    ('<',         r'<',                  '<'),
    ('!',         r'!',                  '!'),
    ('@',         r'@',                  '@'),
    ('#',         r'#',                  '#'),
    ('$',         r'\$',                 '$'),
    ('%',         r'%',                  '%'),
    ('?',         r'\?',                 '?'),
    ('*',         r'\*',                 '*'),
    ('(',         r'\(',                 '('),
    (')',         r'\)',                 ')'),
    ('[',         r'\[',                 '['),
    (']',         r'\]',                 ']'),
    ('{',         r'\{',                 '{'),
    ('}',         r'\}',                 '}'),
)
SKIP_TOKENS = set('space', 'comment')


class TokenStream:
    def __init__(self, text, spec=TOKEN_SPEC):
        self.tokens = tokenize(spec, text)
        self.index = 0

    def read(self, id):
        token = self.peek()
        if self.has(id):
            self.index += 1
            return token
        msg = f'Expected token "{id}" but found "{token.id}"'
        raise LexingError(msg)

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


class TokenSpec:
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
                _map[char] = index
        for index, (id, _, _, chars) in enumerate(spec):
            _build_hints(index, id, chars)
        return _map

    def get(self, hint):
        try:
            index = self.map[hint]
        except KeyError:
            raise LexingError(f'Unrecognized hint: "{hint}"')
        return self.spec[index]


class Token:
    def __init__(self, id, text):
        self.id = id
        self.text = text

    def __repr__(self):
        return f'Token({self.id.upper()}, "{self.text}")'


def tokenize(spec, text):
    tokens = []
    token_spec = TokenSpec(spec)
    txt_stream = CharStream(text)
    while not txt_stream.eof:
        (id, skip, pattern, _) = token_spec.get(txt_stream.head_char)
        match_text, index = txt_stream.read_pattern(pattern)
        if skip:
            continue
        tokens.append(Token(id, match_text))
    return tokens
