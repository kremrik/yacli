from yacli.cli_parser import parse_cli_string
from yacli.exceptions import ValidationException

from collections import namedtuple
from typing import Any, Callable, List, Optional, Tuple


__all__ = ["parse_args"]


cli_arguments = namedtuple(
    typename="cli_arguments",
    field_names=["args", "unexpected"],
)


def parse_args(
    template: dict,
    inpt: Optional[List[str]] = None,
) -> Tuple[dict, dict]:
    if not inpt:
        from sys import argv

        inpt = argv[1:]

    inpt = " ".join(inpt)
    given = parse_cli(inpt)

    args = transform_arguments(
        template=template, given=given
    )
    extras = get_extra_args(template=template, given=given)

    return cli_arguments(args=args, unexpected=extras)


def get_extra_args(template: dict, given: dict) -> dict:
    template_args = set(template)
    given_args = set(given)
    extra_args = given_args - template_args

    if not extra_args:
        return {}

    return {key: given[key] for key in extra_args}


def parse_cli(cli_string: str) -> dict:
    tokenized_input = parse_cli_string(cli_string)
    return {arg.name: arg.value for arg in tokenized_input}


def normalize_cli_results(cli_results: dict) -> dict:
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
        raise ValidationException(msg)

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
        raise ValidationException(msg)


def choice(
    arg: str, from_cli: Any, from_template: Any
) -> Any:
    if from_cli is None:
        return None

    if from_cli not in from_template:
        msg = f"Value '{from_cli}' for arg '{arg}' not permitted, must be one of {from_template}"
        raise ValidationException(msg)

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
        raise ValidationException(msg)

    for o in order:
        if o.__name__ == template_param:
            return o
