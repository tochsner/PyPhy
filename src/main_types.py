from abc import ABC
from typing import Any, TypeVar, get_args, Sequence as TypingSequence

from attrs import define

T = TypeVar("T")


@define
class ObservedSequence:
    sequence: str
    taxon: str


Matrix = list[list[float]]


class Tree(ABC): ...


def get_base_type_name(python_type: type):
    if isinstance(python_type, type(Tree)):
        return "TREE"
    elif isinstance(python_type, type(float)) or isinstance(python_type, type(int)):
        return "REAL"
    elif isinstance(python_type, type(TypingSequence[Any])) and get_args(python_type)[0] == float:
        return "REAL_VECTOR"
    elif isinstance(python_type, type(list[Any])) and get_args(python_type)[0] == float:
        return "REAL_VECTOR"
    elif isinstance(python_type, type(ObservedSequence)):
        return "SEQUENCE"
    elif (
        isinstance(python_type, type(list[Any]))
        and get_args(python_type)[0] == ObservedSequence
    ):
        return "ALIGNMENT"

    raise ValueError(f"Unknown type {python_type}.")
