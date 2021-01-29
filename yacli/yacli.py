from yacli.cli_parser import parse_cli_string

from typing import List, Optional


__all__ = ["parse_args"]


def parse_args(
    template: dict,
    inpt: Optional[List[str]] = None,
    ignore_extra: bool = False,
) -> dict:
    if not inpt:
        from sys import argv

        inpt = argv[1:]
    inpt = " ".join(inpt)

    return _get_cli(
        cli_string=inpt,
        template=template,
        ignore_extra=ignore_extra,
    )


def _get_cli(
    cli_string: str, template: dict, ignore_extra: bool
) -> dict:
    tokenized = _parse_cli(cli_string)
    normalized = _normalize_cli_results(tokenized)

    given_args = set(normalized)
    requested_args = set(template)
    extra_args = given_args - requested_args

    if extra_args and ignore_extra is False:
        raise RuntimeError(
            f"Unexpected argument(s): {extra_args}"
        )

    output = {}
    for arg, prefs in template.items():
        required = prefs["required"]

        if arg not in normalized and required is True:
            raise RuntimeError(
                f"Argument '{arg}' expected"
            )

        if arg not in normalized and required is False:
            continue

        typ = prefs["type"]
        value = typ(normalized[arg]["value"])

        output[arg] = value

    return output


def _parse_cli(cli_string: str) -> dict:
    tokenized_input = parse_cli_string(cli_string)
    fmt_tokens = [tuple(t) for t in tokenized_input]

    output = {}
    for arg in fmt_tokens:
        name = arg[0]

        if len(arg) == 1:
            output[name] = True
        else:
            value = arg[1]
            output[name] = value

    return output


def _normalize_cli_results(cli_results: dict) -> dict:
    output = {}

    for k, v in cli_results.items():
        arg_type = "flag" if isinstance(v, bool) else "arg"
        norm_k = "_".join([x for x in k.split("-") if x])

        value = {
            "normalized": norm_k,
            "type": arg_type,
            "value": v,
        }

        output[k] = value

    return output
