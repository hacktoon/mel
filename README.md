[![Build Status](https://travis-ci.org/hacktoon/dale.svg?branch=master)](https://travis-ci.org/hacktoon/dale)

# DALE

Dale is an abbreviation of *Data Language*. Dale's purpose is to provide a uniform interface for building webapps through a tree-based structure.

---

## Basic syntax

### Types

#### Numbers

Integers and floats are supported as expected.

```
1
-7
+99
4.535
-0.9
```

Floats support scientific notation:

```
-56.2e-5
+0.33e+2
0.7e5
```


#### Texts (strings)

Texts can use double or single quotes as delimiters:

```
"this text uses double quotes"

'and this text uses single quotes'
```

You can write a double-quote character `"` inside a double-quoted text by repeating the character `"`:

```
"She said ""Hello"" yesterday."
```

Texts also can span many lines:

```
"Lorem Ipsum is simply dummy text of the printing and typesetting industry.

Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,

when an unknown printer took a galley of type and scrambled it to make a type specimen book."
```


#### Lists
Lists can have different value types and are enclosed by square brackets:

```
[]

[1, 2, 4]

["foo", 55, "bar"]

```

Commas are optional to separate list items, but you need at least one whitespace to separate items:

```
[1  2  3]

["foo"  5  10]
```

> Commas are ignored and treated as whitespace no matter where you put them in your code.

#### Booleans

```
true

false
```


### Comments

Comments start with the `#` symbol. Anything after a `#` will be ignored until the end of line.

```
"A string"  # this is a comment

# another comment
```


---


## Expressions

Expressions are simply a group of values with some rules. They're formed by a keyword, a set of attributes (or metadata) and a list of values between parenthesis. The example below maps the keyword `title` to the value `"foo-bar"`, in which there are no attributes and there's only a value:

```
(title "foo-bar")
```

By using the `:param value` construction, you can specify the expression's metadata:

```
(person :id 222 :order 223 "John" "Doe")
```

Expressions can have as much attributes as you need. The only rule is: they must start with a semin-colon and be separated by at least one whitespace.

All values within an expression will be concatenated, if possible. In the example above, the result value will be `John Doe`. Note that separating the strings is required since joining them will produce a double quote as stated before: `John"Doe`. Optionally use commas or newlines to visually separate attributes and/or values:

```
(person
    :id 222,
    :order 223,
    "John",
    "Doe"
)
```

Expressions can have sub-expressions, which produce a tree-like data structure.

```
(person
    :id 222

    (name "John")
    (surname "Doe")
)
```
