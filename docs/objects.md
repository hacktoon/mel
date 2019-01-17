# Objects

[Home](../README.md)

---

Objects are any kind of self-contained value, like structs, names and literals.


## Booleans

Booleans are reserved names and are written in lowercase:

```
true
false
(active true)
(active false)

```


## Strings

Strings can use double or single quotes as delimiters:

```
"this string uses double quotes"

'and this string uses single quotes'
```

Strings also can span many lines:

```
"Lorem Ipsum is simply dummy string of the printing and typesetting industry.

Lorem Ipsum has been the industry's standard dummy string ever since the 1500s,

when an unknown printer took a galley of type and scrambled it to make a type specimen book."
```


## Integers

```
0
1
-7
+99
```

## Floats

Floats support scientific notation:

```
-56.2e-5
+0.33e+2
0.7e5
```


## Ranges

Ranges are used to represent a interval of integers or indexes.

```
5..10     -- from 5 to 10

-9..0     -- from -9 to 0

-20..     -- starting from -20

..-20     -- from 0 to -20
```

The more common use for ranges are filtering items in lists:

```
movies/0..5   -- lists the first 4 movies
```