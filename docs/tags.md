# Tags

[Home](../README.md)

---

Tags are keywords used to mark a node with a specific name. Any keyword prefixed with a `#` symbol is considered a tag.

```
(foo #bar #baz 42)  -- tags the 'foo' object with #bar and #baz.
```

## Applications

### HTML

Tags are used to represent the class attribute.

```
(input #active type="checkbox" name="enable-validation")
```
is converted to
```
<input class="active" type="checkbox" name="enable-validation" />
```
