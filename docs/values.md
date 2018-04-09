[Home](../README.md)

---

# Values

## Constants



## Boolean

```
TRUE

FALSE
```


## Text

Texts can use double or single quotes as delimiters:

```
"this text uses double quotes"

'and this text uses single quotes'
```

You can write a double-quote character `"` inside a double-quoted text by repeating the character `"`:

```
"She said ""Hello"" yesterday."
```

Texts also can span many lines:

```
"Lorem Ipsum is simply dummy text of the printing and typesetting industry.

Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,

when an unknown printer took a galley of type and scrambled it to make a type specimen book."
```


## Numbers

Integers and floats are supported as expected.

```
1
-7
+99
4.535
-0.9
```

Floats support scientific notation:

```
-56.2e-5
+0.33e+2
0.7e5
```

Binary values are suffixed with `b`:

```
0b

-10b

1101010b

001b
```

Octals are prefixed with `8x`:

```
8x0

8x71

8x55634

-8x12
```

Hexadecimals start with `0x`:

```
0xFFF

0x00A345

0x334123
```

Digital information values

```
1Kb      # 1 kilobit
1Mb      # 1 megabit
2KB      # 2 kilobytes
11MB     # 11 megabytes
5GB      # 5 gigabytes
```

Time unit values have suffixes that identify its type:

```
132ms       # 132 milliseconds
400ns       # 400 nanoseconds
1s          # a second
0s          # zero second
-1s         # minus one second

345s        # 345 seconds
4m          # 4 minutes
6h          # 6 hours

3h4m7s      # a complete time value (must be within a compound value)
-2h40m7ns   # minus two hours, 40 minutes and 7 nanoseconds
6m5s        # implicit hours means 0h
8h41s       # as well as minutes
10h4m       # and seconds
```

Date values

```
14d   # 14 days
2mo   # 2 months
52w   # 52 weeks
1y    # one year
-6y   # minus 6 years
```


Miscelany units values
```
34px   # pixels
10em   # relative
```


## Lists

Lists can have different values and are enclosed by square brackets:

```
[]

[1, 2, 4]

["foo", 55, "bar"]

```

Commas are optional to separate list items, but you need at least one whitespace to separate items:

```
[1  2  3]

["foo"  5  10]
```
