# Flags

[Home](../README.md)

---

Flags (or tags) are used to mark a property. Flags are keys that start with a `!` and don't expect values when declared. A flag value is always TRUE.

```
(Person
    !VIP
    !Active

    Name "Mary"
)
```


Flags can be used to generate information like CSS classes. See below:

```
(Title
    !Active
    !Bold

    "content"
)
```

This can be converted to:

```
<title class="active bold">content</title>
```
