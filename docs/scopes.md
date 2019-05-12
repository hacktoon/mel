# Scopes

[Home](../README.md)

---

A scope defines a context, which has a key and zero or more expressions.

Any first path is considered the scope's key.

Scopes are used to set values in contexts. The example below defines an scope `person` with properties `name` and `age` equal to `"Mary"` and `42`, respectively:

```
(person
    name = "Mary"
    age = 42
)
```

## Keys

Keys are the first value in a scope.


## Values

Scopes can have as many values as necessary.
