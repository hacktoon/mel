 # Syntax rules

[Home](../README.md)

---

## Grammar

```
root       =  expression*

expression =  flag | relation | object
flag       =  '!' NAME
relation   =  path symbol object

path       =  keyword ( '/' keyword )*

keyword    =  NAME | RESERVED_NAME | uid | variable | format | doc
uid        =  '#' NAME
variable   =  '$' NAME
format     =  '%' NAME
doc        =  '?' NAME

symbol     =  '=' | '!=' | '<' | '<=' | '>' | '>='

object     =  reference | literal | list | scope

reference  =  head-ref ( '/' child-ref )* ( '/' flag )?
head-ref   =  query | keyword
child-ref  =  RANGE | INT | wildcard | list | query | keyword

literal    =  RANGE | INT | FLOAT | STRING | BOOLEAN

list       =  '[' object* ']'
scope      =  '(' struct ')'
query      =  '{' struct '}'

struct     =  key root
key        =  ':' | path

wildcard   =  '*'

comment    =  '--'
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
(bar_ 3)   -- defines an scope named 'bar_'
```


## Reserved names

Reserved names are like `NAME`s except they start with a capital letter.
They represent names reserved for an application's context.

```
Page      -- the page class
File      -- a file reference

```


## Ranges

Ranges (i.e `RANGE`) represent numeric intervals between integers.

```
0..10    -- from 0 to 10
..6      -- from 0 to 6
8..      -- from 8 to infinity
-5..0    -- from -5 to 0
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
