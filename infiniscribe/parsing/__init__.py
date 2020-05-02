import functools


class Language:
    def __init__(self, name='Default'):
        self.name = name
        self._start = None
        self._tokens = {}
        self._rules = {}

    def start(self, parser):
        def decorator(evaluator):
            @functools.wraps(evaluator)
            def _evaluator():
                return evaluator(parser())
            self._start = _evaluator
            return _evaluator
        return decorator

    def token(self, id, parser):
        def decorator(evaluator):
            @functools.wraps(evaluator)
            def _evaluator():
                return evaluator(parser())
            self._tokens[id] = _evaluator
            return _evaluator
        return decorator

    def node(self):
        pass

    def parse(self):
        return self._start()


'''
# rules =================================

lang.token('string', seq(s('"'), zero_many(neg(s('"'))), s('"')))
def eval_token(parsed):
    return

lang.line_comment(oneof('STRING', 'INT', 'FLOAT'))
lang.node('keyword', oneof('STRING', 'INT', 'FLOAT'))
lang.node('literal', oneof('STRING', 'INT', 'FLOAT'))
lang.node('int', zeromany(char('digit'), hints=digits)


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


# make extra processing, or define custom lexers
@lang.lex(rule, 'STRING')
def string_parser_plugin(stream):
    return
'''
