# Flags

[Home](../README.md)

---

Flags are keywords used to mark or tag a node with a specific name. Any keyword prefixed with a exclamation symbol is considered a flag.

```
(foo !bar !baz 42)  -- adds the !bar and !baz to foo object.
```

## Applications

### HTML

Flags are used to represent the class attribute.

```
(input !active type="checkbox" name="enable-validation")
```
is converted to
```
<input class="active" type="checkbox" name="enable-validation" />
```
