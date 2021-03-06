# yacli
![coverage](images/coverage.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

_yet another command line interface_

### Why
I wanted to try my hand at some simple "Parsing Expression Grammar", and parsing command line arguments seemed like a fun way to start.

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
ValidationException: Argument '--bar' expected
```

There are several other descriptors you can use:
- default
- help
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
        "arg_type": [2.72, 1.62],
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

Finally, help functionality is available by default (but can be turned off if desired):

```python
template = {
    "--foo": {
        "help": "does foo-y things"
        "arg_type": int
    },
    "--bar": float
}

parse_args(template, app_name="cool-app", inpt=["-h"])  # "--help" will work, too
cool-app
  --foo    does foo-y things
  --bar
```
