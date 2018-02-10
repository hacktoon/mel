# Modifiers

[Home](../README.md)

---

[in progress]

## Query

The symbol `@` which means *"at"* is used for data queries. By default the `@` alone means a URI query. The example below can be read as *name is at URL "http://example.com/name"*:

```
name @ "http://example.com/name"
```


## File

The `<` is used for including file contents. The file path is relative to the current Dale file being read.

```
name < "docs/name.txt"
```


## Parse

The `<|` is used for including and parsing a file content. By default it parses Dale files.

```
# docs/name.dl

("John" "Doe")
```

```
name <| "docs/name.dl"
```


## System

## Format
