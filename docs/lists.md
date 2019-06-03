# Lists

[Home](../README.md)

---

A list is a collection of values. Allowed values are references, literals, objects and other lists. Mixed types are permitted.

```
names = ['alice', 'ana', 'bob']
values = [42, GoldenHeart, (person #id="bob")]
fibonacci = [1 1 2 3 5 8 13 21]
```


## Applications

Consider the expression below:

```
(fruits
    (apple  #id = 1)
    (banana #id = 2)
    (mango  #id = 3)
)
```

List can be used to get the `#id` of the `apple` and `mango` fruits:

```
fruits/[apple, mango]/#id   -- [1, 3]
```

Or to get fruits by their id:

```
{fruits/* #id = [3, 2]}   -- [(mango), (banana)]
```
