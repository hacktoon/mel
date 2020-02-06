import string

from ..exceptions import GrammarError
from .stream import TextStream


'''
Grammar's grammar:
---
@start      = rules*
rule        = '@'? name = alternative eol
alternative = sequence ('|' sequence)*
sequence    = atom+
atom        = ( name | token | group | string ) modifier?
group       = '(' alternative ')'
modifier    = '*' | '+' | '?'
'''


TOKEN_SPEC = (
    (0, 'token',     r'[-A-Z]+\b',          string.ascii_uppercase),
    (0, 'name',      r'[-a-z]+\b',          string.ascii_lowercase),
    (0, 'eol',       r'[\r\n;]+',           '\r\n;'),
    (1, 'space',     r'[ \t]*',             ' \t'),
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


class HintMap:
    '''
    TODO: Currently supports only one token per hint
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
    def __init__(self, spec):
        self.hint_map = HintMap(spec)

    def tokenize(self, text):
        tokens = []
        txt_stream = TextStream(text)
        while not txt_stream.eof:
            (skip, name, pattern, _) = self.hint_map.get(txt_stream.head_char)
            match_text, index = txt_stream.read_pattern(pattern)
            if skip:
                tokens.append(Token(name, match_text))
        return tokens


class TokenStream:
    def __init__(self, token_map, text):
        self.token_map = token_map
        self.tokens = token_map.tokenize(text)
        self.text = text
        self.index = 0

    def read(self, name=''):
        token = self.tokens[self.index]
        if name and token.name != name:
            msg = f'Expected token "{name}" but found "{token}"'
            raise GrammarError(msg)
        self.index += 1
        return token

    def peek(self, name=''):
        token = self.tokens[self.index]
        return token.name == name

    def __getitem__(self, index):
        return self.tokens[index]

    def __len__(self):
        return len(self.tokens)


class Token:
    def __init__(self, name, text):
        self.name = name
        self.text = text

    def __repr__(self):
        return f'Token({self.name}, "{self.text}")'


def parse(text):
    token_map = TokenMap(TOKEN_SPEC)
    stream = TokenStream(token_map, text)
    return parse_atom(stream)


def parse_atom(stream):
    stream.read()
