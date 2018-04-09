# Syntax rules

[Home](../README.md)

---

Dale's syntax is based on a simple idea: a sequence of one or more properties. [Values](values.md) must be separated by at least one whitespace and can have an optional key.

The general syntax rules can be (partially) written in [EBNF](https://tomassetti.me/ebnf/):

```
key           =  [A-Z][_0-9a-zA-Z]*
name          =  [a-z][_0-9a-zA-Z]*

keyspace      =  key ('.' key)*
namespace     =  name ('.' name)*

meta-value    =  '{' keyspace flag* attribute* property+ '}'

value         =  text | number | boolean | list | scope | meta-value | ...

flag          =  '!' key value
attribute     =  ':' key value

scope         =  '(' (keyspace)? flag* attribute* property+ ')' ( /1 ')' )?

property      =  keyspace? flag* attribute* value

dale          =  property*
```


## Whitespace

Tabs, spaces, newlines, commas and semicolons are considered whitespace and are important for separating tags and values. For example, the code below:

```
Name "Ringo"
Age 12
"About Ringo" (1, 2, 3)
```

can be rewritten in one line:

```
Name "Ringo" Age 12 "About Ringo" (1 2 3)
```

or using commas and/or semicolons:

```
Name "Ringo";
Age 12;
"About Ringo";
(1; 2; 3)
```


## Comments

A comment starts with the `--` symbol and ends at the end of the line. Comments are ignored by the parser and won't be interpreted.

```
"A string"   -- this is a comment

-- another comment
```


## Values

[Values](values.md) are the main components of Dale since it's a sequence of values. Values can be modified and composed in [scopes](scopes.md).

```
'a text'

454

TRUE
```


### Scopes

You may want a keyword to identify more than one value. In this case, parentheses are used to define a [Scope](scopes.md), in which you can combine as many values as necessary. The brackets are optional if there's only one value and no metadata.

```
Age 33                 -- a keyword 'age' with a value '33'

(Age 33)               -- the same as above

(Numbers 33, 67, 90)   -- three integers identified by the 'Numbers' keyword

Numbers (33, 67, 90)   -- the same as above, but using a list (note the absence of brackets}
```
