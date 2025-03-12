from functools import singledispatch

from src.distributions import Sequence
from src.values import ChainedValues, Distribution, Function


@singledispatch
def _to_json(
    obj, random_variables: dict[str, dict], deterministic_functions: dict[str, dict]
):
    return obj


@_to_json.register(Distribution)
def _(
    distribution: Distribution,
    random_variables: dict[str, dict],
    deterministic_functions: dict[str, dict],
):
    fields = [
        field
        for field in dir(distribution)
        if not field.startswith("_") and not callable(getattr(distribution, field))
    ]

    parameters = {
        field: _to_json(
            getattr(distribution, field), random_variables, deterministic_functions
        )
        for field in fields
    }

    random_variables[distribution.name()] = {
        "distribution": {
            "type": type(distribution).__name__,
            "generates": distribution.producedType(),
            "parameters": parameters,
        }
    }

    if distribution.get_observation() is not None:
        observation = _to_json(
            distribution.get_observation(), random_variables, deterministic_functions
        )
        random_variables[distribution.name()]["distribution"]["observedValue"] = observation

    return {"variable": distribution.name()}


@_to_json.register(list)
def _(
    obj: list,
    random_variables: dict[str, dict],
    deterministic_functions: dict[str, dict],
):
    return [_to_json(item, random_variables, deterministic_functions) for item in obj]


@_to_json.register(Function)
def _(
    function: Function,
    random_variables: dict[str, dict],
    deterministic_functions: dict[str, dict],
):
    fields = [
        field
        for field in dir(function)
        if not field.startswith("_") and not callable(getattr(function, field))
    ]

    parameters = {
        field: _to_json(
            getattr(function, field), random_variables, deterministic_functions
        )
        for field in fields
    }

    deterministic_functions[function.name()] = {
        "function": function.name(),
        "arguments": parameters,
    }

    return {"variable": function.name()}


@_to_json.register(Sequence)
def _(
    sequence: Sequence,
    random_variables: dict[str, dict],
    deterministic_functions: dict[str, dict],
):
    return {
        "taxon": sequence.taxon,
        "sequence": sequence.sequence,
    }


@_to_json.register(ChainedValues)
def _(
    chain: ChainedValues,
    random_variables: dict[str, dict],
    deterministic_functions: dict[str, dict],
):
    _to_json(chain.left, random_variables, deterministic_functions)
    _to_json(chain.right, random_variables, deterministic_functions)

    return {"variable": f"{chain.left.name()} {chain.operator} {chain.right.name()}"}


def to_json(obj, model_name: str):
    random_variables = {}
    deterministic_functions = {}

    _to_json(obj, random_variables, deterministic_functions)

    return {
        "model": model_name,
        "randomVariables": random_variables,
        "deterministicFunctions": deterministic_functions,
    }
