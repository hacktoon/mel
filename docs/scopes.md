# Scopes

[Home](../README.md)

---

Scopes define a context for a sequence of values
Scopes are values with sub-values, defined by a key, which is also a value. Consider the example:

```
(name "Mary")
```

Scopes can be of two types: set and get.

```
(name "Mary")
```

## Set



## Get




Here, `name` and `"Mary"` are values, with `name` being the key of this scope since it is the first value. It defines a relationship: `name` is equal to `"Mary"`.

Scopes can have one or more values. The following example shows a scope with three values, one of then being a sub-scope defining the language as english, followed by two strings that together define the `name`:

```
(name (lang "en") "Mary" "Sue")
```

## Keys

Keys are the first value in a scope, determining


## Values

Scopes can have as many values as necessary.

