
class Language:
    def __init__(self, name='Unnamed'):
        self.name = name

    def line_comment(self, evaluator):
        def parser():
            return evaluator()
        return parser

    def node(self):
        pass


'''
# rules =================================

@lang.line_comment(oneof('STRING', 'INT', 'FLOAT'))
def literal_parser(value):
    return

@lang.node('keyword', oneof('STRING', 'INT', 'FLOAT'))
def literal_parser(value):
    return


@lang.node('literal', oneof('STRING', 'INT', 'FLOAT'))
def literal_parser(value):
    return


@lang.node('int', zeromany(char('digit'), hints=digits)
def int_parser(value):
    return


@lang.token('string', use('STRING'))
def string_parser(value):
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

# make extra processing, or define custom lexers
@lang.lex(rule, 'STRING')
def string_parser_plugin(stream):
    return
'''
