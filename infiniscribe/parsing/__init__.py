import functools


class Language:
    def __init__(self, name='Default'):
        self.name = name
        self._start = lambda stream: None
        self._tokens = {}
        self._rules = {}

    def start(self, parser):
        def decorator(evaluator):
            @functools.wraps(evaluator)
            def _evaluator(stream):
                return evaluator(parser(stream))
            self._start = _evaluator
            return _evaluator
        return decorator

    def token(self, id, parser):
        def decorator(evaluator):
            @functools.wraps(evaluator)
            def _evaluator(stream):
                return evaluator(parser(stream))
            self._tokens[id] = _evaluator
            return _evaluator
        return decorator

    def parse(self, text):
        # stream = TokenStream(text)
        return self._start(text)


'''
# rules =================================

lang.line_comment('#')
lang.multi_comment('##')

@lang.rule('int', integer())
def eval_int(parsed):
    return

@lang.rule('float', floatp())
def eval_float(parsed):
    return

@lang.rule('concept', seq(upper(), zero_many(alnum())))
def eval_concept(parsed):
    return

@lang.rule('string', qst('"'))
def eval_string(parsed):
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
