# Flags

[Home](../README.md)

---

Flags are keywords used to mark or tag a node with a specific name.

```
(foo !bar 42)
```

## Applications

### HTML

Flags are used to represent the class attribute.

```
(input !checked type="checkbox" name="enable-validation")
```
is converted to
```
<input class="checked" type="checkbox" name="enable-validation" />
```
