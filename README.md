[![Build Status](https://travis-ci.org/hacktoon/dale.svg?branch=master)](https://travis-ci.org/hacktoon/dale)

# DALE

Dale is a _**da**ta description **l**anguag**e**_ which describes the metadata, attributes and relations in a data model. Dale can be used to generate data like HTML, CSS, XML, JSON and other tree structures, using a common language.


## Main objectives
 * Provide a uniform interface for building webapps
 * Build and represent different type of information
 * Generate different outputs

---

* [Basic syntax](docs/basic-syntax.md)
* [Basic types](docs/basic-types.md)

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
