# Examples

[Home](../README.md)

---

## A simple data record

This example show how Dale can represent data:

```
-- Let's define a "person" object.
(person
    -- This object has an id equal to 5,
    (#id 5)

    -- a property "name" with value "John" and
    (name "John")

    -- a property "surname" with value "Doe".
    (surname "Doe")

    -- Set "fullname" using defined properties.
    (fullname @name " " @surname)

    -- Define the "age" property as 45.
    (age 45)
)

```

It shows how properties can be defined using groups (using parentheses) for composed values. The `fullname` property is a concatenation of previously defined properties with a space character.

## Web component

```
(component (@type "thumbnail")
    (?desc "this is a component for thumbnails")
    (~page {Query "/site/page[current]"})

    (a
        (img (@src "http://thumbnails.com/3444") (@alt "A random image"))
    )
)component)
```


## Representing nested HTML



```
(li/a (@href "http://foo.bar") 'content')
```

can be used to represent this HTML snippet:

```
<li>
    <a href="http://foo.bar">content</a>
</div>
```