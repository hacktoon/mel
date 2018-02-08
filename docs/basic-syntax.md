# Dale

[Home](../README.md)

---

## Basic syntax

Dale's syntax is based on a simple idea: a sequence of one or more values.

```
"a single text value"
```

A sequence may contain any value (See [Basic types](basic-types.md)) and they must be separated by at least one whitespace.

```
"a text"
454
true
```

Commas are considered whitespace so they are optional and can be used anywhere. This allows you to organize your code as you prefer.

```
"a text", 454, true

['a list' 'with' ' no separator']

['a comma', '-separated', 'list']

,"another text",,  22,,,,  " a final text",
```

Keywords can be used to identify a value. **A keyword refers to one, and only one value**. If you need to aggregate more values under a keyword, _expressions_ are the solution.

```
name "Ringo"
age 12
```

In the example above, `name` and `age` refer to the values `"Ringo"` and `12`, respectively. It is possible to rewrite this example in one line, separated by tabs, spaces, newlines or commas.

```
name "Ringo"    age 12,
address "Liverpool St"
```

Non-keyword values can be mixed with keyword values.

```
name "Ringo",

['apple' 'orange'],

age 12

"description about Ringo"
```


### Comments

A comment starts with the `#` symbol and ends at the end of the line. Comments are ignored by the parser and won't be interpreted as keyword or values.

```
"A string"   # this is a comment

# another comment
```
