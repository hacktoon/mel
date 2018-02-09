[![Build Status](https://travis-ci.org/hacktoon/dale.svg?branch=master)](https://travis-ci.org/hacktoon/dale)

# DALE

Dale is a _**da**ta description **l**anguag**e**_ which describes the metadata, context and relations in a data model. Dale can be used to generate data like HTML, CSS, XML, JSON and other tree structures, using a common language.

## Main objectives
 * Provide a uniform interface for building webapps
 * Build and represent different types of information
 * Automatize data generation to different outputs

---

## Setup

### Dependencies
 * Python 3.x
 * Pip
 * GNU Make
 * Docker (optionally)
 
### Setup and run using Docker
```
docker build -t dale .
docker run dale examples/thumbnail.dl
```

## Documentation

* [Basic syntax](docs/basic-syntax.md)
* [Basic types](docs/basic-types.md)


## License

Dale is distributed under the terms of the MIT license. See [LICENSE](LICENSE.md).
