[![Build Status](https://travis-ci.org/hacktoon/dale.svg?branch=master)](https://travis-ci.org/hacktoon/dale)

# Dale

Dale is a data language. It can be used for configuration files and representing any tree-like data structure like HTML and CSS.


## Requirements

* make
* Python 3.5+


## How to use


```
dale examples/thumbnail.dl
```


## Syntax

Dale's syntax is similar to Lisp. The example below shows an expression structure:

```
(person :id 4
    (name "Alice")
    (age 25)
)
```


### Types

#### Integers and floats

```
4
-5.7
0.08
-1
4.66e2

```

#### Strings

Strings can use single or double quotes.

```
'a single quoted string'

"a double quoted string"

```

#### Boolean

```
true
false

```