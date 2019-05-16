# Keywords

[Home](../README.md)

---

Keywords are names with different properties, used to reference tree nodes.

In the example below, the keyword `answer` is set to reference the `int` 42:

```
answer = 42
```


Keywords can be prefixed with symbols like: `#`, `@`, `%` and `?`.


## Tags

Tags are used to define a name as `true` by default. Tags are `#` prefixed names.

```
(person
    #vip
    name = "Mary"
)
```


Tags can be used to generate information like CSS classes. See below:

```
(title
    #active
    #bold

    "content"
)
```

This can be converted to HTML as:

```
<title class="active bold">content</title>
```
