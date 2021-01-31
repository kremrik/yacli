from pyparsing import (
    Char,
    Combine,
    Group,
    Optional,
    Word,
    ZeroOrMore,
    alphanums,
    printables,
)

from collections import namedtuple
from typing import List, Optional as Opt


__all__ = ["parse_cli_string"]


d = "-"
dash = Char(d)
arg_identifier = Combine(dash + Optional(dash))
arg_name = Word(alphanums + d)
kwarg = Combine(arg_identifier + arg_name)

value_bgn = "".join(
    [p for p in list(printables) if p != d]
)
value = Combine(
    Char(value_bgn) + ZeroOrMore(Word(printables))
)

kwarg_and_value = kwarg + value
bool_arg = kwarg
varargs_and_values = kwarg + value[2, ...]

arg = (
    kwarg_and_value("kwarg")
    ^ bool_arg("flag")
    ^ varargs_and_values("varargs")
)
cli = ZeroOrMore(Group(arg))


argument = namedtuple(
    typename="argument",
    field_names=["name", "value", "kind"],
)


def parse_cli_string(
    arg_string: str,
) -> List[Opt[argument]]:
    if not arg_string:
        return []

    tokenized = cli.parseString(arg_string)
    output = []

    for token in tokenized:
        token = token.asDict()
        kind = list(token.keys())[0]

        if isinstance(token[kind], list):
            value = token[kind][1:]
            value = value[0] if len(value) == 1 else value
            name = token[kind][0]
        else:
            value = None
            name = token[kind]

        a = argument(name, value, kind)
        output.append(a)

    return output
