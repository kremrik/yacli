from typing import List, Optional


__all__ = ["handle_help"]


HELP_ARGS = ("-h", "--help")


def handle_help(
    template: dict,
    given: dict,
    app_name: Optional[str] = None,
) -> None:
    if not app_name:
        app_name = "CLI Help"

    output = format_help_output(
        template=template, app_name=app_name
    )

    if not given:
        print(output)
        exit(0)

    for h in HELP_ARGS:
        if h in given:
            print(output)
            exit(0)


def format_help_output(
    template: dict, app_name: str
) -> str:
    # main testable function for this module
    args = get_arg_help(template)
    output = f"{app_name}\n{args}\n"
    return output


def get_arg_help(template: dict) -> List[str]:
    indent = 2 * " "
    sep = 4
    max_arg_len = 0
    args = []

    for arg, params in template.items():
        help = get_help(params)
        typ = get_type(params)

        arg_len = len(arg)
        if arg_len > max_arg_len:
            max_arg_len = arg_len

        a = (arg, help, typ, arg_len)
        args.append(a)

    total_arg_space = max_arg_len + sep
    formatted_args = []

    for arg in args:
        name, help, typ, arg_len = arg
        space = (total_arg_space - arg_len) * " "
        a = f"{indent}{name}{typ}{space}{help}".rstrip()
        formatted_args.append(a)

    output = "\n".join(formatted_args)
    return output


# TODO: breaks abstraction
def get_help(params: dict) -> str:
    if not isinstance(params, dict):
        help = ""
    else:
        help = params.get("help")
        if not help:
            help = ""
    return help


# TODO: breaks abstraction
def get_type(params) -> str:
    if isinstance(params, dict):
        typ = params.get("arg_type", "")
    elif params == Ellipsis:
        typ = " [nargs]"
    elif isinstance(params, list):
        typ = f" {str(params)}"
    else:
        typ = f" [{str(params.__name__)}]"
    return typ
