# from ...exceptions import GrammarError

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


def parse(text):
    stream = TokenStream(text)
    return parse_atom(stream)


def parse_atom(stream):
    stream.read()


def parse_choice(stream):
    stream.read()
