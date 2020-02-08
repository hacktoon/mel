from ...exceptions import GrammarError
from .tokens import TokenStream


'''
Grammar's grammar:
---
/grammar    = rule*
rule        = '@'? NAME = alternative eol
alternative = seq *('|' seq)
seq         = atom+
atom        = ( NAME | TOKEN | group | string ) modifier?
group       = '(' alternative ')'
modifier    = '*' | '+' | '?'
NAME        = [a-z]+
TOKEN       = [A-Z]+
-SPACE      = '\n'+
'''


GRAMMAR_SPEC = (
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
    token = stream.peek()
    msg = f'Expected one of {ids} but found {token.id}'
    raise GrammarError(msg)
