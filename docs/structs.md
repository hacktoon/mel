# Structs

[Home](../README.md)

---

A struct defines a context, which has an optional key and zero or more values.

The key and values are objects. Any first object is considered the struct's key.

Structs are used to set values in contexts. The example below defines an scope `person` with properties `name` and `age` equal to `"Mary"` and `42`, respectively:

```
(person
    (name "Mary")
    (age  42)
)
```

## Keys

Keys are the first value in a scope.
If the first value is a relation, the scope key is considered to be null.


## Values

Structs can have as many values as necessary.
