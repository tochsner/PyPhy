from abc import ABC
from typing import Any, Generic, TypeVar, get_args

from attrs import define

T = TypeVar("T")


@define
class Sequence:
    sequence: str
    taxon: str


Matrix = list[list[float]]


class Tree(ABC): ...


from src.main_types import Tree


def get_base_type_name(python_type: type):
    if isinstance(python_type, type(Tree)):
        return "TREE"
    elif isinstance(python_type, type(Sequence)):
        return "SEQUENCE"
    elif isinstance(python_type, type(list[Any])) and get_args(python_type)[0] == float:
        return "REAL_VECTOR"
    elif isinstance(python_type, type(list[Any])) and get_args(python_type)[0] == Sequence:
        return "ALIGNMENT"
    elif isinstance(python_type, type(float)) or isinstance(python_type, type(int)):
        return "REAL"

    raise ValueError(f"Unknown type {python_type}.")
