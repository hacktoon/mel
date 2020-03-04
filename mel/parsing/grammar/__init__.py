'''
@root = body?
@space = [SPACE|NEWLINE|,]+

body = expression ( _ expression )*
name = [a-z][a-z|0-9]+
concept = [A-Z][a-z|0-9]*

default-path = ':'
default-doc = '?:'
default-format = '%:'
wildcard = '*'

expression = tag | relation | value

tag = '#' name

relation = path _ sign _ value
sign = equal | diff | lte | lt | gte | gt | in | out
equal = '='
diff = '!='
lt = '<'
lte = '<='
gt = '>'
gte = '>='
in = '><'
out = '<>'

path = keyword ( _ ( sub-path | meta-path ) )*
sub-path = '/' _ keyword
meta-path = '.' _ keyword

keyword = name | concept | log | alias | cache | format | meta | doc
log = '!' name
alias = '@' name
cache = '$' name
format = '%' name
meta = '~' name
doc = '?' name

value = literal | reference | list | object

reference = head-reference sub-reference*
head-reference = query | keyword
sub-reference = _ '/' _ sub-reference-item
sub-reference-item = range | INT | tag | list | object | query | keyword | *

literal = INT | FLOAT | STRING | BOOLEAN

list = '[' _ list-items? _ ']'
list-items = value ( _ value )*

range = '..' INT | INT '..' INT?

object = '(' _ key _ body? _ ')'
key = path | default-path | default-format | default-doc

query = '{' _ target _ body _ '}'
target = default-path | path

'''


TOKEN_SPEC = {
    'space':   r',\s+',
    'comment': r'--',
    'concept': r'[A-Z]-?[_A-Z]+',
    'name':    r'[a-z]_?[_a-z]+',
    'float':   r'-?[0-9](.[0-9]+)?',
    'int':     r'-?[0-9]+',
    ':':       r':',
    '?:':      r'\?:',
    '%:':      r'%:',
    '!':       r'!',
    '@':       r'@',
    '#':       r'#',
    '$':       r'\$',
    '%':       r'%',
    '?':       r'\?',
    '/':       r'/',
    '..':      r'..',
    '.':       r'.',
    "'":       r"'",
    '"':       r'"',
    '=':       r'=',
    '!=':      r'!=',
    '<>':      r'<>',
    '><':      r'><',
    '>=':      r'>=',
    '<=':      r'<=',
    '>':       r'>',
    '<':       r'<',
    '*':       r'\*',
    '(':       r'\(',
    ')':       r'\)',
    '[':       r'\[',
    ']':       r'\]',
    '{':       r'\{',
    '}':       r'\}',
}


RULES = (
    # First line is the start rule
    # RULE         PARSER    EXPANSION
    ('grammar',    '*',      '@rule'),
    ('rule',       'SEQ',    '@rule-type', '@rule-name', '=', '@alt', 'eol'),
    ('rule-name',  'ALT',    'name', 'token'),
    ('rule-type',  '?/ALT',  '/', '-'),
    ('alt',        'SEQ',    '@seq', '@alt-tail'),
    ('alt-tail',   '*/SEQ',  '|', '@seq'),
    ('seq',        '+',      '@atom'),
    ('atom',       'SEQ',    '@atom-head', '@modifier'),
    ('atom-head',  'ALT',    '@group', 'name', 'token', 'string'),
    ('group',      'SEQ',    '(', '@alt', ')'),
    ('modifier',   '?/ALT',  '*', '?', '+'),
)


def parse_spec(spec):
    pass


def zero_many(parser):
    pass


def rule(name):
    pass


def _parse_alternative(stream, ids):
    for id in ids:
        if stream.has(id):
            return stream.read(id)
    stream.peek()
