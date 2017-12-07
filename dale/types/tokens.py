import re
from collections import OrderedDict


rc = re.compile

specs = OrderedDict([
    ('.',          rc(r'\.')),
    ('@',          rc(r'@')),
    (':',          rc(r':')),
    ('(',          rc(r'\(')),
    (')',          rc(r'\)')),
    ('[',          rc(r'\[')),
    (']',          rc(r'\]')),
    ('whitespace', rc(r'[,\s]+')),
    ('comment',    rc(r'#[^\n\r]*')),
    ('boolean',    rc(r'(true|false)\b')),
    ('name',       rc(r'[_a-zA-Z]\w*(-[_a-zA-Z]\w*)?')),
    ('float',      rc(r'[-+]?\d*\.\d+([eE][-+]?\d+)?\b')),
    ('int',        rc(r'[-+]?\d+\b')),
    ('string',     rc(r'|'.join([r"'(?:\\'|[^'])*'", r'"(?:\\"|[^"])*"'])))
])