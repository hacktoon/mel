 # Syntax rules

[Home](../README.md)

---

Dale's syntax rules are:

```
root             =  metadata* object*

object           =  literal | list | reference | scope

literal          =  INT | FLOAT | STRING | BOOLEAN

list             =  '[' object* ']'

reference        =  base-reference ( reference-child | '.' identifier )*
base-reference   =  RANGE | query | identifier | wildcard
reference-child  =  '/' ( base-reference | INT | list )

scope            =  '(' key metadata* object* ')'
query            =  '{' key criteria* object* '}'

key              =  ':' | namespace

metadata         =  flag | equals

namespace        =  identifier ( '/' identifier | '.' identifier )*

identifier       =  NAME | RESERVED_NAME | uid | variable | format | doc
flag             =  '!' NAME
uid              =  '#' NAME
variable         =  '$' NAME
format           =  '%' NAME
doc              =  '?' NAME

wildcard         =  '*'

criteria         =  flag | equals | different | lt | lte | gt | gte
equals           =  namespace '=' object
different        =  namespace '!=' object
lt               =  namespace '<' object
lte              =  namespace '<=' object
gt               =  namespace '>' object
gte              =  namespace '>=' object

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
