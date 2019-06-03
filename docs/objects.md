# Objects

[Home](../README.md)

---

Objects are used to define an object with properties.

The example below defines an object `person` with the properties `name` equal to "Mary" and `age` equal to 42:

```
(person  name = "Mary"  age = 42)
```

## Syntax

Objects require a key and can have zero or more expressions:

```
'(' key expressions* ')'
```

The key must be a path or a null key `:`.
The expressions can be tags, relations or values.


## Applications

### HTML

When converted to HTML, objects become tags. The example below:

```
(input type="text" 42)
```

is converted to:

```
<input type="text" value="42" />
```
