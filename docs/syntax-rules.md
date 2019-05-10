 # Syntax rules

[Home](../README.md)

---

## Grammar

```
root       =  meta object*

meta       =  ( flag | statement )*
flag       =  '!' NAME
statement  =  path symbol object

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

struct     =  key meta object*
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
f1o2o3    -- can have numbers
3foo      -- wrong! Can't start with numbers
(bar 3)   -- defines an scope named 'bar'
```


## Reserved names

Reserved names are like `NAME`s except they start with a capital letter.
They represent names reserved for an application's context.

```
Pages                -- all the pages in a site
{File "index.html"}  -- a query to a file named "index.html"

```


## Ranges

Ranges (i.e `RANGE`) represent numeric intervals between integers.

```
Pages                -- all the pages in a site
{File "index.html"}  -- a query to a file named "index.html"

```


## Whitespace

Whitespace isn't significant, except for some cases like names followed by numbers, which may cause semantic errors:

```
(foo 42)  -- a scope with a name `foo` followed by a number 42
foo42   -- a name `foo42`
```

So there's no problem concatenating a string and a name, since the quote symbol act as a delimiter between a string and anything else:

```
"monty"python
```

Or typing scopes without any separation:

```
(person"john")(dog"rex")
```

Spaces, tabs, newlines, commas and semicolons are all considered whitespace and will be ignored. Consider the example:

```
(name "Bob")
(age 12)
(items ball fruit)
"Description about Bob"
```

It can be rewritten in one line:

```
(name "Bob") (age 12) (items ball fruit) "Description about Bob"
```

or using commas ans semicolons:

```
(name lang="en"; "Bob");
(age 12);
(items ball, fruit);
"Description about Bob";
```
