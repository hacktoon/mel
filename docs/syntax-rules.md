# Syntax rules

[Home](../README.md)

---

Dale's syntax is based on a simple idea: a sequence of one or more values of any type. [Values](values.md) must be separated by at least one whitespace and can have an optional keyword.

The general syntax rules can be (partially) written in [EBNF](https://tomassetti.me/ebnf/):

```
value    =  text | number | boolean | list | group
scope    =  '('  ')'
item     =  keyword? value
grammar  =  item*
```


## Whitespace

Tabs, spaces, newlines, commas and semicolons are considered whitespace and are important for separating tags and values. For example, the code below:

```
name "Ringo"
age 12
"About Ringo" [1, 2, 3]
```

can be rewritten in one line:

```
name "Ringo" age 12 "About Ringo" [1 2 3]
```

or using commas and/or semicolons:

```
name "Ringo";
age 12, "About Ringo" [1; 2; 3]
```


## Comments

A comment starts with the `#` symbol and ends at the end of the line. Comments are ignored by the parser and won't be interpreted.

```
"A string"   # this is a comment

# another comment
```


## Values

[Values](values.md) are the main components of Dale as it is a sequence of values. Values can be modified and composed in [groups](groups.md).

```
"a text"

454

true
```


### Groups

You may want a keyword to identify more than one value. In this case, parentheses are used to define a [Group](groups.md), in which you can combine as many values as necessary. The parentheses are optional if there's only one value and no metadata.

```
age 33                 # a keyword 'age' with a value '33'

(age 33)               # the same as above

(numbers 33, 67, 90)   # three integers identified by the 'numbers' keyword

numbers [33, 67, 90]   # the same as above, but using a list (note the absence of parentheses)
```
