from yacli.cli_parser import parse_cli_string

from typing import Any, Callable, List, Optional, Tuple


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

        typ = prefs["arg_type"]
        value = typ(normalized[arg]["value"])

        output[arg] = value

    return output


def _parse_cli(cli_string: str) -> dict:
    tokenized_input = parse_cli_string(cli_string)
    return {arg.name: arg.value for arg in tokenized_input}


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


# input validation
# ---------------------------------------------------------
def required(
    arg: str, from_cli: Any, from_template: Any
) -> Any:
    if not from_cli and from_template:
        msg = f"Argument '{arg}' required"
        raise RuntimeError(msg)

    return from_cli


def arg_type(
    arg: str, from_cli: Any, from_template: Any
) -> Any:
    if from_cli is None:
        return None

    if from_template is bool:
        return True

    if from_template is Ellipsis:
        if not isinstance(from_cli, list):
            return [from_cli]
        return from_cli

    try:
        return from_template(from_cli)
    except ValueError:
        typ = from_template.__name__
        msg = f"Value '{from_cli}' for arg '{arg}' cannot be cast to type '{typ}'"
        raise RuntimeError(msg)


def choice(
    arg: str, from_cli: Any, from_template: Any
) -> Any:
    if from_cli is None:
        return None

    if from_cli not in from_template:
        msg = f"Value '{from_cli}' for arg '{arg}' not permitted, must be one of {from_template}"
        raise RuntimeError(msg)

    return from_cli


def default(
    arg: str, from_cli: Any, from_template: Any
) -> Any:
    if not from_cli:
        return from_template

    return from_cli


order = [required, arg_type, choice, default]
order_names = [o.__name__ for o in order]


def transform_arguments(
    template: dict, given: dict
) -> dict:
    output = []
    for arg, params in template.items():
        value = transform_argument(
            arg, params, given.get(arg)
        )

        if value is not None:
            output.append(value)

    return dict(output)


def transform_argument(
    arg: str, params: dict, given: str
) -> Tuple[str, Any]:
    if not isinstance(params, dict):
        passes_req = required(arg, given, params)
        value = arg_type(arg, passes_req, params)
        return arg, value

    temp = given
    for param_name, param_value in params.items():
        temp = pick_check(param_name)(
            arg, temp, param_value
        )

    if temp is None:
        return None

    return arg, temp


def pick_check(template_param: str) -> Callable:
    if template_param not in order_names:
        msg = f"Template parameter '{template_param}' not permitted"
        raise RuntimeError(msg)

    for o in order:
        if o.__name__ == template_param:
            return o
