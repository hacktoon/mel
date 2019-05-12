# Names

[Home](../README.md)

---

Names are used to reference values. In the example below, the name `answer` is set to reference the `int` 42:

```
(answer 42)
```


Names can be prefixed with the following symbols: `!`, `#`, `$`, `%` and `?`.


## Flags

Flags are used to define a name as `true` by default. Flags are `!` prefixed names.

```
(person
    !vip
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

This can be converted to HTML as:

```
<title class="active bold">content</title>
```
