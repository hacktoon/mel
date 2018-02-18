# Examples

[Home](../README.md)

---

## A simple data record

This example show how Dale can represent data:

```
(person                              # Let's define a "person" object.
    :id 5                            # This object has an id equal to 5,
    name "John"                      # a property "name" with value "John" and
    surname "Doe"                    # a property "surname" with value "Doe".
    (fullname @name ' ' @surname)    # Set "fullname" using defined properties.
    age 45                           # Define the "age" property as 45.
)

```

It shows how properties can be defined using groups (using parentheses) for composed values. For definitions with single values the parentheses are optional. The `fullname` property is a concatenation of previously defined properties with a space character.


## Web component

```
(component :type "thumbnail"
    (? "this is a component for thumbnails")

    = page @ "/site/page[current]"
    (a (image :src "http://thumbnails.com/3444" :alt "A random image"))
)component)
```






