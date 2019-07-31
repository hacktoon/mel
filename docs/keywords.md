# Keywords

[Home](../README.md)

---

Keywords are names with different properties, used to reference tree nodes.

In the example below, the keyword `answer` is set to reference the `int` 42:

```
answer = 42
```

Keywords can be prefixed with symbols like: `!`, `@`, `#`, `$`, `%` and `?`, which add specific functions to them.


## Tags

Tags are used to define a keyword as `true` by default. Tags are `#` prefixed keywords.

```
(person
    #vip
    name = "Mary"
)
```


## Aliases

Aliases are used to reference other objects and allows reusability.

```
@mary = (person
    #vip
    name = "Mary"
)

"My friend is called" @mary/name
```
