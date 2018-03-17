# Keywords

[Home](../README.md)

---

### Keyword chaining

Converte os componentes em tags aninhadas

```
li.a.title = "example"
```

Result:
```
<li><a><title id="3">example</title></li></a>
```


The attribute `:id` is a value unique identifier. It is stored in a global dictionary.

```
:id 44

package #id
(keyword #pid 34)

package #pid 2

```