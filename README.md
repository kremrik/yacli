# yacli
![coverage](images/coverage.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

_yet another command line interface_

### Why
Half because I wanted to try my hand at some simple "Parsing Expression Grammar", 
half because I just wanted something simpler, more data-driven, and a little more functional than the leading CLI contenders.
<br><br>
Many of said CLI frameworks for Python are either either entirely language-specific or very opinionated.
For example, `click` is not a language-agnostic implementation of a CLI tool, and it's also heavily geared towards coupling your business logic (the options/arguments) with the application logic (the functions you're decorating).
<br><br>
`yacli` tries to be unsurprising and intuitive, getting our of your way as soon as possible, and relying entirely on native Python objects. 

### Basics
`yacli` works by exposing one function, `parse_args`, that takes an input template (of type `dict`),
and (optionally) an argument `inpt` for passing something like `sys.argv[1:]`.
If the latter is not supplied, it will be populated with `sys.argv[1:]`.
<br><br>
`parse_args` then returns a tuple of two dicts:
1. the validated, expected arguments defined in the aforementioned template
2. any unexpected, extra arguments that were not defined in the template

This allows you to decide what you want to do with any arguments you didn't expect.
For example, if you wanted to do some fuzzy-matching to see if an arg was simply misspelled.


### Examples

In its simplest form, `yacli` treats each argument as required:

```python
from yacli import parse_args

template = {
    "--foo": int,
    "--bar": bool
}

parse_args(template, ["--foo", "1", "--bar"])
({"--foo": 1, "--bar": True}, {})

parse_args(template, ["--foo", "1", "--bar", "-v"])
({"--foo": 1, "--bar": True}, {"-v": None})

parse_args(template, ["--foo", "1"])
...
RuntimeError: Argument '--bar' expected
```

There are several other descriptors you can use:
- choice
- default
- required
- arg_type

```python
template = {
    "--foo": {
        "required": True,
        "arg_type": int
    },
    "--bar": {
        "required": False,
        "arg_type": float,
        "choice": [2.72, 1.62]
    },
    "--very-verbose": {
        "required": False,
        "default": False,
        "arg_type": bool
    }
}

parse_args(template, ["--foo", "1"])
({"--foo": 1, "--very-verbose": False}, {})
```

Additionally, you may use the `Ellipses` (`...`) to signify a "nargs"-like input:

```python
template = {
    "--foo": ...
}

parse_args(template, ["--foo", "1", "2"])
({"--foo": ["1", "2"]}, {})
```
