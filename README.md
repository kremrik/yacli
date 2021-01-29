# yacli
![coverage](images/coverage.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

_yet another command line interface_

### Why
Half because I wanted to try my hand at some simple "Parsing Expression Grammar", 
half because I just wanted something simpler, more data-driven, and a little more functional than the leading CLI contenders.

### Examples

In its simplest form, `yacli` treats each argument as required:

```python
from yacli import parse_args

template = {
    "--foo": int,
    "--bar": bool
}

parse_args(template, ["--foo", "1", "--bar"])
{"--foo": 1, "--bar": True}

parse_args(template, ["--foo", "1"])
...
RuntimeError: Argument '--bar' expected
```

There are several other descriptors you can use:
- default
- required
- type

```python
from yacli import parse_args

template = {
    "--foo": {
        "required": True,
        "type": int
    },
    "--bar": {
        "required": False,
        "type": float
    },
    "--very-verbose": {
        "required": False,
        "default": False,
        "type": bool
    }
}

parse_args(template, ["--foo", "1"])
{"--foo": 1, "--very-verbose": False}
```
