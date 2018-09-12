# Flags

[Home](../README.md)

---

Flags (or tags) are used to mark a property. Flags are keys that start with a `!` and don't expect values when declared. A flag value is always TRUE.

```
(person
    !vip

    (#rg 457567567)
    (#tel 5456567)
    (name "Mary")
)
```


Flags can be used to generate information like CSS classes. See below:

```
(title
    !active
    !bold

    "content"
)
```

This can be converted to:

```
<title class="active bold">content</title>
```
