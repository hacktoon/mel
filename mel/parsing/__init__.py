from ..lexing.stream import CharStream
from .parsers import ParserHintMap


class Language:
    def __init__(self):
        self.hint_map = ParserHintMap()

    def parse(self, text):
        stream = CharStream(text)


'''
# PARSER GENERATORS =================================
NAME         HINT
S            first char
R            get from parser in called rule
Digit        any digit
Lower        all lower
Upper        all upper
Alpha        lower + upper
Alnum        one of letters + digits
Digits       shortcut to one or many digits
Quote        disables reading spaces
LitSeq       disables reading spaces
Seq          sequence of parsers
Alt
OptAlt       optional alternative
Not          special ANY char
Opt          first char of parser
OptSeq       optional sequence
OneMany
ZeroMany

# rules ===================================
lang.single_comment('#')

lang.multi_comment('##')

lang.space(' \n\t,;')

lang.rule('int', Digits())

lang.rule('float', LitSeq(
    Digits(),
    OptSeq(S('.'), Digits()),
))

lang.rule('string', Quote('"\'', escape='\\'))

lang.rule('concept', Seq(Upper(), ZeroMany(AlNum())))

lang.rule('object', Seq(
    S('('),
    R('key'), R('value'),
    S(')')
))

lang.rule('relation', Seq(
    R('path'), R('symbol'), R('value')
))

lang.rule('path', Seq(
    R('keyword'),
    ZeroMany(Seq(
        R('separator'), R('keyword')
    ))
))



# ========= node conversion (to other formats)

@lang.map(lang.rules.object)
def eval_object(match):
    return


@lang.map(lang.tokens.string)
def eval_string(match):
    return


==========================================================
GRAMMAR
==========================================================
# line comment
root          =  *expression
expression    =  tag | relation | value | +attr-keyword
tag           =  '#' NAME *( SUB-PATH NAME )

##  multi comment
relation      =  path sign value?
##

path          =  keyword __ *( separator __ keyword )
keyword       =  !( NAME | CONCEPT )
attr-keyword  =  '@' name
separator     =  sub-path | !attr-path
literal       =  STRING | INT | FLOAT
name          =  [a-z]
string        =  '"' *(!'"') '"'

oneof  = um dentre as opcoes
anyof  = quantos possiveis dentre as opcoes
noneof = um fora das opcoes

'''
