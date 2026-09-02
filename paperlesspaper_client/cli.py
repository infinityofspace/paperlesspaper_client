import argparse
import inspect
import json
import os
import sys
from typing import Any, Literal, get_args, get_origin

from paperlesspaper_client.client import Client, ClientError

RESOURCE_NAMES = ("accounts", "devices", "organizations", "papers", "users")
ENV_API_KEY_NAME = "PAPERLESSPAPER_API_KEY"
DEFAULT_BASE_URL = "https://api.paperlesspaper.de/v1/"


def _parse_bool(value: str) -> bool:
    truthy = {"1", "true", "yes", "on"}
    falsy = {"0", "false", "no", "off"}
    lowered = value.lower()
    if lowered in truthy:
        return True
    if lowered in falsy:
        return False
    raise argparse.ArgumentTypeError(f"Invalid bool value: {value}")


def _parse_json_dict(value: str) -> dict:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(f"Invalid JSON object: {exc}") from exc
    if not isinstance(parsed, dict):
        raise argparse.ArgumentTypeError("Value must be a JSON object.")
    return parsed


def _parse_key_value(pair: str) -> tuple[str, Any]:
    if "=" not in pair:
        raise argparse.ArgumentTypeError("--param expects the format key=value")
    key, raw_value = pair.split("=", 1)
    key = key.strip()
    if not key:
        raise argparse.ArgumentTypeError("The key in --param must not be empty")
    raw_value = raw_value.strip()
    if raw_value == "":
        return key, ""
    try:
        return key, json.loads(raw_value)
    except json.JSONDecodeError:
        return key, raw_value


def _unwrap_optional(annotation: Any) -> Any:
    origin = get_origin(annotation)
    if origin is None:
        return annotation
    args = [arg for arg in get_args(annotation) if arg is not type(None)]
    if len(args) == 1:
        return args[0]
    return annotation


def _resolve_converter(annotation: Any):
    annotation = _unwrap_optional(annotation)
    origin = get_origin(annotation)

    if annotation in (inspect._empty, str):
        return str
    if annotation is int:
        return int
    if annotation is float:
        return float
    if annotation is bool:
        return _parse_bool
    if annotation is dict:
        return _parse_json_dict
    if origin is Literal:
        literal_args = get_args(annotation)
        sample = literal_args[0] if literal_args else str
        if isinstance(sample, bool):
            return _parse_bool
        if isinstance(sample, int):
            return int
        return str

    return str


def _resolve_choices(annotation: Any) -> list[Any] | None:
    annotation = _unwrap_optional(annotation)
    if get_origin(annotation) is Literal:
        return list(get_args(annotation))
    return None


def _method_name_to_actions(resource: str, method_name: str) -> set[str]:
    actions = {method_name.replace("_", "-")}
    singular = resource.removesuffix("s")

    if method_name == f"list_{resource}":
        actions.add("list")

    for verb in (
        "get",
        "create",
        "update",
        "delete",
        "ping",
        "reboot",
        "register",
        "reset",
    ):
        if method_name in {f"{verb}_{singular}", f"{verb}_{resource}"}:
            actions.add(verb)

    get_prefix = f"get_{singular}_"
    if method_name.startswith(get_prefix):
        actions.add(method_name[len(get_prefix) :].replace("_", "-"))

    suffixes = (f"_{singular}", f"_{resource}")
    for suffix in suffixes:
        if method_name.endswith(suffix):
            actions.add(method_name[: -len(suffix)].replace("_", "-"))

    return {action for action in actions if action}


def _build_action_map(api_obj: Any, resource: str) -> dict[str, str]:
    action_map: dict[str, str] = {}
    method_names = [
        name
        for name in dir(api_obj)
        if not name.startswith("_") and callable(getattr(api_obj, name))
    ]

    for method_name in sorted(method_names):
        for action in _method_name_to_actions(resource, method_name):
            action_map.setdefault(action, method_name)

    return action_map


def _env_api_key() -> str | None:
    return os.getenv(ENV_API_KEY_NAME)


def _build_method_parser(
    resource: str, action: str, method: Any
) -> tuple[argparse.ArgumentParser, list[inspect.Parameter], inspect.Parameter | None]:
    parser = argparse.ArgumentParser(prog=f"paperlesspaper {resource} {action}")

    signature = inspect.signature(method)
    parameters = list(signature.parameters.values())
    normal_params: list[inspect.Parameter] = []
    kwargs_param: inspect.Parameter | None = None

    for parameter in parameters:
        if parameter.kind == inspect.Parameter.VAR_KEYWORD:
            kwargs_param = parameter
            continue

        normal_params.append(parameter)
        converter = _resolve_converter(parameter.annotation)
        choices = _resolve_choices(parameter.annotation)

        if parameter.default is inspect._empty:
            parser.add_argument(parameter.name, type=converter, choices=choices)
            continue

        option_name = f"--{parameter.name.replace('_', '-')}"
        parser.add_argument(
            option_name,
            dest=parameter.name,
            default=None,
            type=converter,
            choices=choices,
        )

    if kwargs_param is not None:
        parser.add_argument(
            "--param",
            action="append",
            default=[],
            metavar="KEY=VALUE",
            help="Arbitrary parameter for **kwargs, e.g. --param role=admin",
        )

    return parser, normal_params, kwargs_param


def _print_json(result: Any) -> None:
    try:
        print(json.dumps(result, indent=2, sort_keys=True))
    except TypeError:
        print(str(result))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="paperlesspaper", description="CLI for the paperlesspaper API"
    )
    parser.add_argument(
        "--api-key",
        "--token",
        dest="api_key",
        default=None,
        help="API key (takes priority over env)",
    )
    parser.add_argument(
        "--base-url",
        dest="base_url",
        default=os.getenv("PAPERLESSPAPER_BASE_URL"),
        help="Optional API base URL",
    )
    parser.add_argument("resource", choices=RESOURCE_NAMES, help="API resource")
    parser.add_argument("action", help="Action on the resource")

    args, remaining = parser.parse_known_args(argv)

    api_key = args.api_key or _env_api_key()
    if not api_key:
        parser.error(
            f"No API key found. Use --api-key or the {ENV_API_KEY_NAME} environment variable."
        )

    client = Client(api_key=api_key, base_url=args.base_url or DEFAULT_BASE_URL)
    api_obj = getattr(client, args.resource)
    action_map = _build_action_map(api_obj, args.resource)

    method_name = action_map.get(args.action)
    if method_name is None:
        available = ", ".join(sorted(action_map.keys()))
        parser.error(
            f"Unknown action '{args.action}' for {args.resource}. Available: {available}"
        )

    method = getattr(api_obj, method_name)
    method_parser, normal_params, kwargs_param = _build_method_parser(
        args.resource, args.action, method
    )
    method_args = method_parser.parse_args(remaining)

    call_kwargs: dict[str, Any] = {}
    for parameter in normal_params:
        value = getattr(method_args, parameter.name)
        if parameter.default is inspect._empty or value is not None:
            call_kwargs[parameter.name] = value

    if kwargs_param is not None:
        for pair in method_args.param:
            key, value = _parse_key_value(pair)
            call_kwargs[key] = value

    try:
        result = method(**call_kwargs)
    except ClientError as exc:
        print(f"Error: {exc}", file=sys.stderr)

        return 1

    _print_json(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
