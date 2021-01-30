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

from typing import List, Tuple, Optional as Opt


__all__ = ["parse_cli_string"]


d = "-"
dash = Char(d)
arg_identifier = Combine(dash + Optional(dash))
arg_name = Word(alphanums + d)
kwarg = Combine(arg_identifier + arg_name)

value_bgn = "".join([p for p in list(printables) if p != d])
value = Combine(Char(value_bgn) + ZeroOrMore(Word(printables)))

kwarg_and_value = kwarg + value
bool_arg = kwarg

arg = kwarg_and_value ^ bool_arg
cli = ZeroOrMore(Group(arg))


def parse_cli_string(arg_string: str) -> List[Opt[Tuple[str]]]:
    if arg_string:
        tokenized = cli.parseString(arg_string)
        return [tuple(t) for t in tokenized]

    return []
