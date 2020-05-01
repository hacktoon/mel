

'''
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


# rules =================================

@lang.line_comment(oneof('STRING', 'INT', 'FLOAT'))
def literal_parser(value):
    return

@lang.rule('keyword', oneof('STRING', 'INT', 'FLOAT'))
def literal_parser(value):
    return


@lang.rule('literal', oneof('STRING', 'INT', 'FLOAT'))
def literal_parser(value):
    return


@lang.rule('int', zeromany(char('digit'), hints=digits)
def int_parser(value):
    return


@lang.token('string', use('STRING'))
def string_parser(value):
    return


# ========= node conversion (to other formats)

@lang.map(lang.rules.string)
def string_node(node):
    return


'''
# criar char scanner - serve pra sanitizar caracteres
# atribui tipo, coluna e linha pra cada char
# Enum types: alpha:1, digit:2, symbol:3, space:4, newline:5, unknown:6


# token e string nao viram um node

# MULTI_COMMENT_ID = '1'
# LINE_COMMENT_ID  = '2'
# SPACE_ID         = '3'
# NEWLINE_ID       = '4'
# LEXING_TABLE     = (
#     # ID                PATTERN                 SKIP  HINTS
#     # RESERVED RULES =========================================
#     (MULTI_COMMENT_ID,  r'##',                  1,    '#'),
#     (LINE_COMMENT_ID,   r'#',                   1,    '#'),
#     (SPACE_ID,          r'[ \t]+',              1,    ' \t'),
#     (NEWLINE_ID,        r'\n|\r\n?',            1,    '\r\n'),
#     # CUSTOM RULES ===========================================
#     ('equals',          r'=',                   0,    '='),
#     ('optional'         r'\?',                  0,    '?'),
#     ('one-many'         r'\+',                  0,    '+'),
#     ('zero-many'        r'\*',                  0,    '*'),
#     ('not'              r'!',                   0,    '!'),
#     ('alternative',     r'\|',                  0,    '|'),
#     ('open-group',      r'\(',                  0,    '('),
#     ('close-group',     r'\)',                  0,    ')'),
#     ('open-list',       r'\[',                  0,    '['),
#     ('close-list',      r'\]',                  0,    ']'),
#     ('space',           r'__',                  0,    '__'),
#     ('optional-space',  r'_',                   0,    '_'),
#     ('charset',         r'[A-Za-z]-[A-Za-z]',   0,    letters),
#     ('rule',            r'[a-z](-[a-z])*',      0,    lowercase),
#     ('token',           r'[A-Z](-[A-Z])*',      0,    uppercase),
#     ('string',          r"'[^']*'|\"[^\"]*\"",  0,    "'\""),
# )


# class Token:
#     def __init__(self, id, text):
#         self.id = id
#         self.text = text

#     def __repr__(self):
#         return f'Token({self.id.upper()}, "{self.text}")'


# def tokenize(text):
#     tokens = []
#     token_spec = TokenSpec(LEXING_TABLE)
#     char_stream = CharStream(text)
#     while not char_stream.eof:
#         (id, skip, pattern, _) = token_spec.get(char_stream.head_char)
#         match_text, index = char_stream.read_pattern(pattern)
#         if skip:
#             continue
#         token = Token(id, match_text)
#         tokens.append(token)
#     return tokens
