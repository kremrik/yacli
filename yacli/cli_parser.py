from pyparsing import (
    Char,
    Combine,
    Group,
    Optional,
    Word,
    ZeroOrMore,
    alphanums,
    printables
)

from typing import List, Tuple


__all__ = ["parse_cli_string"]


d = "-"
dash = Char(d)
arg_identifier = Combine(dash + Optional(dash))
arg_name = Word(alphanums + d)
kwarg = Combine(arg_identifier + arg_name)
value = Word(printables)

kwarg_and_value = kwarg + value
bool_arg = kwarg

arg = kwarg_and_value ^ bool_arg
cli = ZeroOrMore(Group(arg))


def parse_cli_string(arg_string: str) -> List[Tuple[str]]:
    if arg_string:
        return cli.parseString(arg_string)
