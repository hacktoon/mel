 # Syntax rules

[Home](../README.md)

---

Dale's syntax rules are:

```
root            =  metadata* object*

metadata        =  assignment | flag
path            =  identifier ( attribute | child )*
identifier      =  NAME | uid | variable | format | doc
attribute       =  '.' ( identifier | flag )
child           =  '/' NAME
uid             =  '#' NAME
variable        =  '$' NAME
format          =  '%' NAME
doc             =  '?' NAME
flag            =  '!' NAME

assignment      =  path '=' object

object          =  literal | list | scope | base-object ('/' sub-object)*
base-object     =  query | identifier | wildcard
sub-object      =  INT | range | base-object

literal         =  INT | FLOAT | STRING | BOOLEAN

scope           =  '(' key metadata* object* ')'
key             =  ':' | path

query           =  '{' target criteria* object* '}'
target          =  path
criteria        =  flag | path sign object
sign            =  "=" | "!=" | ">" | "<" | ">=" | "<="

list            =  '[' object* ']'


wildcard        =  '*'
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
(name "Bob", "Joe");
(age 12),
(items ball, fruit),
"Description about Bob (Joe)";
```


## Comments

A comment starts with the `--` symbol and ends at the end of the line. Comments are ignored by the parser and won't be interpreted.

```
"A string"   -- this is a comment and (id 5) won't be interpreted

-- another comment
```
