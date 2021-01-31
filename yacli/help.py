from typing import List


__all__ = ["format_help"]


def format_help(app_name: str, template: dict) -> str:
    args = get_arg_help(template)
    output = f"{app_name}\n{args}\n"
    return output


def underline(text: str) -> str:
    return "-" * len(text)


def get_arg_help(template: dict) -> List[str]:
    indent = 2 * " "
    sep = 4
    max_arg_len = 0
    args = []

    for arg, params in template.items():
        if not isinstance(params, dict):
            help = ""
        else:
            help = params.get("help")
            if not help:
                help = ""

        arg_len = len(arg)
        if arg_len > max_arg_len:
            max_arg_len = arg_len

        a = (arg, help, arg_len)
        args.append(a)

    total_arg_space = max_arg_len + sep
    formatted_args = []

    for arg in args:
        name, help, arg_len = arg
        space = (total_arg_space - arg_len) * " "
        a = f"{indent}{name}{space}{help}".rstrip()
        formatted_args.append(a)

    output = "\n".join(formatted_args)
    return output
