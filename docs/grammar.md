 # Syntax rules

[Home](../README.md)

---

## Grammar

```
TAG             =  '#'
LOG             =  '!'
ALIAS           =  '@'
CACHE           =  '$'
FORMAT          =  '%'
META            =  '.'
DOC             =  '?'
EQUAL           =  '='
DIFFERENT       =  '!='
LT              =  '<'
LTE             =  '<='
GT              =  '>'
GTE             =  '>='
IN              =  '><'
NOT-IN          =  '<>'
SUB-PATH        =  '/'
ATTR-PATH       =  '.'
WILDCARD        =  '*'
DEFAULT-DOC     =  '?:'
DEFAULT-FORMAT  =  '%:'
DEFAULT-PATH     =  ':'

root            =  expression*

expression      =  tag | relation | value

tag             =  '#' NAME ( SUB-PATH NAME )*

relation        =  path sign value

path            =  keyword ( separator keyword )*
keyword         =  NAME | CONCEPT | attr-keyword
attr-keyword    =  ( LOG | ALIAS | CACHE | FORMAT | META | DOC ) NAME

separator       =  SUB-PATH | ATTR-PATH

sign            =  EQUAL | DIFFERENT | LT | LTE | GT | GTE | IN | NOT-IN

value           =  reference | literal | list | object

reference       =  ( query | keyword ) reference-tail
reference-tail  =  ( sub-reference | attr-reference )*
sub-reference   =  WILDCARD | RANGE | INT | tag | list | object | query | keyword
attr-reference  =  WILDCARD | tag | keyword

literal         =  INT | FLOAT | STRING | TEMPLATE-STRING | BOOLEAN

list            =  '[' value* ']'

object          =  '(' object-key expression* ')'
object-key      =  WILDCARD | DEFAULT-PATH | DEFAULT-FORMAT | DEFAULT-DOC | path

query           =  '{' query-key expression* '}'
query-key       =  DEFAULT-PATH | path
```


## Comments

Comments starts with the `--` symbol. The parser will ignore everything else until the line ends.

```
"foobar"     -- defines a string
42           -- answers everything
```


## Names

Names (i.e `NAME`) are formed by lowercase letters and numbers only.
They're used to represent tree nodes by its names.

```
foo       -- the name 'foo'
f1o2_o3   -- can have numbers and underscores
3foo      -- wrong! Can't start with numbers
(bar_ 3)   -- defines an object named 'bar_'
```


## Concepts

Concepts are like `NAME`s except they start with a capital letter.
They represent names reserved (or concepts) for an application's context.

```
Web       -- a concept for using the Web
Page      -- the page collection in a site
File      -- a file reference
```


## Ranges

Ranges (i.e `RANGE`) represent numeric intervals between integers.

```
5..10     -- from 5 to 10

-9..0     -- from -9 to 0

-20..     -- starting from -20

..-20     -- from 0 to -20
```

The most common use for ranges are filtering items in lists:

```
movies/0..3   -- lists the first 4 movies
```


## Whitespace

Whitespace isn't significant. Spaces, tabs, newlines, commas `,` and semicolons `;` are all considered whitespace and will be ignored. All examples below are valid:

```
python='foo',,
python = 'bar';
"monty",python;;;
"monty"     python,
(person"john");(dog"rex")
```

The example below...

```
(name lang = "en"  "Bob")
(age 12)
(items ball fruit)
"Description about Bob"
```

...can be rewritten in one line...

```
(name "Bob") (age 12) (items ball fruit) "Description about Bob"
```

...or using commas, semicolons and tabs:

```
(name
    lang="en";
    "Bob"
);

(age 12);
(items; ball, fruit);

"Description about Bob";
```
