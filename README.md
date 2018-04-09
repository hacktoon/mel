[![Build Status](https://travis-ci.org/hacktoon/dale.svg?branch=master)](https://travis-ci.org/hacktoon/dale)

# DALE

Dale is a _**da**ta description **l**anguag**e**_ which describes the metadata, context and relations in a data model. Dale can be used to generate data like HTML, CSS, XML, JSON and other tree structures, using a common language.


## Main objectives
 * Provide a uniform interface for building webapps
 * Build and represent different types of information
 * Automatize data generation with different outputs

---

## Setup & run

### Dependencies

 * Python 3.x
 * Pip
 * GNU Make
 * Docker (optional)

It's recommended to use a virtual environment tool like [pyenv](https://github.com/pyenv/pyenv) and/or [pipenv](https://github.com/pypa/pipenv).


### How to run

```
make install
make test
make inspect
python cli.py examples/person.dl
```


### Using Docker

```
docker build -t dale .
docker run dale examples/thumbnail.dl
```


## Documentation

 * [Syntax rules](docs/syntax-rules.md)
 * [Keys](docs/keys.md)
 * [Values](docs/values.md)
 * [Scopes](docs/scopes.md)
 * [Modifiers](docs/modifiers.md)


## License

Dale is distributed under the terms of the **MIT** license. See [LICENSE](LICENSE.md).
