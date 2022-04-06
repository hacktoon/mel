# PARSER GENERATORS
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


## RULE GRAMMAR

There can be space between terms

```
root          = *expression
expression    =  tag | relation | value | +attr-keyword
tag           =  '#' NAME *( SUB-PATH NAME )

relation      =  path sign value?

path          =  keyword __ *( separator __ keyword )
keyword       =  !( NAME | CONCEPT )
attr-keyword  =  '@' name
separator     =  sub-path | !attr-path
literal       =  STRING | INT | FLOAT
```

## TOKEN GRAMMAR

There's no space between terms

```
INT                    =  '-'? DIGIT+
FLOAT                  =  '-'? DIGIT+ ('.' DIGIT+)?
NAME                   =  LOWER ('_' | LOWER | DIGIT)*
CONCEPT                =  UPPER ('_' | LOWER | DIGIT)*
STRING                 =  '"' [^'"']* '"'
EQUAL_SYMBOL           =  '='
DIFFERENT_SYMBOL       =  '!='
LT_SYMBOL              =  '<'
LTE_SYMBOL             =  '<='
GT_SYMBOL              =  '>'
GTE_SYMBOL             =  '>='
IN_SYMBOL              =  '><'
NOT_IN_SYMBOL          =  '<>'
PATH_SYMBOL            =  '.'
WILDCARD_SYMBOL        =  '*'
OPEN_OBJECT_SYMBOL     =  '('
CLOSE_OBJECT_SYMBOL    =  ')'
OPEN_QUERY_SYMBOL      =  '{'
CLOSE_QUERY_SYMBOL     =  '}'
OPEN_LIST_SYMBOL       =  '['
CLOSE_LIST_SYMBOL      =  ']'
```

### Token parsers
- char
- optional
- group
- not
- any
- one_many
- zero_many

Each parser returns a ParserResult

Example for NameToken
    seq(
        char(LowerChar()),
        zero_many(
            any(
                char(SymbolChar('_'))
                char(LowerChar())
                char(DigitChar())
            )
        )
    )
