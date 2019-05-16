# Scopes

[Home](../README.md)

---

Scopes are used to define objects and its properties. As the name says, it creates a new scope.

The example below defines a scope `person` with the properties `name` equal to "Mary" and `age` equal to 42:

```
(person
    name = "Mary"
    age = 42
)
```

## Syntax

Scopes require a key and can have zero or more expressions:

```
'(' key expressions* ')'
```

The key must be a path or a null key `:`.
The expressions can be tags, relations or objects. All tags and relations will be considered the scope's metadata.


## Applications

### HTML

When converted to HTML, scopes become tags. The example below:

```
(input type="text" 42)
```

is converted to:

```
<input type="text" value="42" />
```
