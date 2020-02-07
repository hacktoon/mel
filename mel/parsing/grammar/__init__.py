from ...exceptions import GrammarError
from .tokens import TokenStream


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


def parse(text: str):
    # grammar = Grammar()
    stream = TokenStream(text)
    return parse_atom(stream)


def parse_atom(stream: TokenStream):
    stream.read()


def parse_modifier(stream: TokenStream):
    return _parse_alternative(stream, '*?+')


def _parse_alternative(stream, ids):
    for id in ids:
        if stream.has(id):
            return stream.read(id)
    token = stream.peek()
    msg = f'Expected one of {ids} but found {token.id}'
    raise GrammarError(msg)
