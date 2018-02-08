# Basic syntax

[Home](../README.md)

---

## Values

Dale's syntax is based on a simple idea: a sequence of one or more values. A sequence may contain any value type (See [Basic types](basic-types.md)) and they must be separated by at least one whitespace.

```
"a text"
454
true
```

Commas are considered whitespace, so they are optional and can be used anywhere. This allows you to organize your code as you prefer.

```
"a text", 454, true

['a list' ' with' ' no separator']

['a comma', '-separated', ' list']

,"another text",,  22,,,,  " a final text",
```


### Keywords

Keywords can be used to identify one or more values. **A keyword, by default, identifies one, and only one value**.

```
name "Ringo"
age 12  "About Ringo"
```

In the example above, `name` and `age` refer to the values `"Ringo"` and `12`, respectively. The text `"About Ringo"` isn't associated to the `age` keyword; it's just another normal, non-identified value in the sequence. Non-identified values can be mixed with identified values.


### Whitespace

Tabs, spaces, newlines and commas are all considered whitespace and are important for separating keywords and values. It is possible to rewrite the last example in one line:

```
name "Ringo"   age 12, "About Ringo"
```

Another example:

```
name "Yoko",

['apples'  "oranges"],

age 12

"About Ringo"  "About Yoko"
```


### Comments

A comment starts with the `#` symbol and ends at the end of the line. Comments are ignored by the parser and won't be interpreted.

```
"A string"   # this is a comment

# another comment
```


### Compound values

You may want a keyword to identify more than one value. In this case, parentheses are used to define a scope in which you can aggregate as many values as necessary. The parentheses are optional if there's only one value and no attributes.

```
age 33                 # a keyword 'age' with a value '33'

(age 33)               # the same as above

(numbers 33, 67, 90)   # three integers identified by the 'numbers' keyword

numbers [33, 67, 90]   # the same as above, but using a list (note the absence of parentheses)
```
