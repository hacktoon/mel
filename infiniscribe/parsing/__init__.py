import functools

from .stream import Stream


# TODO: class RuleRegistry

class Language:
    def __init__(self, name='Default'):
        self.name = name
        self._start = lambda stream: None
        self._rules = {}

    def start(self, parser):
        def decorator(evaluator):
            @functools.wraps(evaluator)
            def real_parser(stream):
                return evaluator(parser(stream))
            self._start = real_parser
            return real_parser
        return decorator

    def rule(self, id, parser):
        def decorator(evaluator):
            @functools.wraps(evaluator)
            def real_parser(stream):
                return evaluator(parser(stream))
            self._rules[id] = real_parser
            return real_parser  # TODO: wrap in Parser Metadata class
        return decorator

    # TODO: add magic_methods to extend evaluators, maybe

    def parse(self, text):
        return self._start(Stream(text))


'''
# parsers =================================
s
r
digit
digits  -- one or many digits
quoted  -- disables reading spaces
litseq  -- disables reading spaces
seq     -- sequence of parsers
alt
non
opt
onemany
zeromany


# rules ===================================
lang.single_comment('#')
lang.multi_comment('##')
lang.separator(' \n\t,;')

@lang.rule('int', some(digit()))
def eval_float(parsed):
    return

@lang.rule('float', lseq(numbers(), opt(numbers()), ))
def eval_float(parsed):
    return

@lang.rule('float', seq(
    s('('),
    r('key'), r('value'),
    s(')')
)
def eval_float(parsed):
    return

@lang.rule('string', quoted('"\''))
def eval_string(parsed):
    return parsed.value.strip(parsed.parser.hint)

@lang.rule('concept', lit(upper(), zero_many(alnum())))
def eval_concept(parsed):
    return

@lang.rule('keyword', oneof(t('string'), t('int'), t('float')))
def eval_keyword(parsed):
    return

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
