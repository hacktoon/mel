from .stream import Stream


# TODO: class RuleRegistry

class Language:
    def __init__(self, name='Default'):
        self.name = name
        self._start = lambda stream: None
        self._rules = {}
        self._tokens = {}

    def start(self, parser):
        def real_parser(stream):
            return parser(stream)
        self._start = real_parser
        return real_parser

    def rule(self, id, parser):
        def real_parser(stream):
            return parser(stream)
        self._rules[id] = real_parser
        return real_parser  # TODO: wrap in Parser Metadata class

    def token(self, id, parser):
        def token_parser(stream):
            # stream.read_separator()
            return parser(stream)
        self._tokens[id] = token_parser
        return token_parser  # TODO: wrap in Parser Metadata class

    # TODO: add magic_methods to extend evaluators, maybe

    def parse(self, text):
        return self._start(Stream(text))


'''
# parsers =================================
s
r
number  --
lower   --
upper   --
alpha   -- lower + upper
alnum   -- one of letters + digits
numbers -- shortcut to one or many digits
quoted  -- disables reading spaces
seq     -- sequence of parsers
alt
non
opt
optseq
onemany
zeromany


# rules ===================================
lang.single_comment('#')

lang.multi_comment('##')

lang.separator(' \n\t,;')

lang.token('int', numbers())

lang.token('float', seq(
    numbers(),
    optseq(s('.'), numbers()),
))

lang.rule('string', quoted('"\'', escape='\\'))

lang.token('concept', seq(upper(), zero_many(alnum())))

lang.rule('object', seq(
    s('('),
    r('key'), r('value'),
    s(')')
)

@lang.rule('keyword', oneof(t('string'), t('int')))


# ========= node conversion (to other formats)

@lang.map(lang.rules.string)
def string_node(node):
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
