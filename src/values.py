from __future__ import annotations
from abc import ABC
from typing import Generic, TypeVar, get_args

from attrs import define

from src.main_types import get_base_type_name
from src.naming import pascal_to_camel_case
from src.constraints import Constraint

T = TypeVar("T")


class Node(ABC, Generic[T]):
    _used_names: set[str] = set()
    _wrapped_value_type: type

    def __attrs_post_init__(self):
        name = pascal_to_camel_case(type(self).__name__)

        suffix = 2
        while name in self._used_names:
            name = pascal_to_camel_case(f"{type(self).__name__}{suffix}")
            suffix += 1

        Node._used_names.add(name)
        self._name = name

    def __init_subclass__(cls) -> None:
        # this is a bit of a hack to determine the type of the generic parameter
        # in the subclasses of Node
        cls._wrapped_value_type = get_args(cls.__orig_bases__[0])[0]  # type: ignore

    def __add__(self, other: Node[T]):
        return ChainedValues(self, other, "+")

    def __sub__(self, other: Node[T]):
        return ChainedValues(self, other, "-")

    def __mul__(self, other: Node[T]):
        return ChainedValues(self, other, "*")

    def name(self):
        return self._name

    def producedType(self):
        return get_base_type_name(self._wrapped_value_type)


class Function(Generic[T], Node[T]): ...


class Distribution(Generic[T], Node[T]):
    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        self._constraints = []
        self._observation = None

    def observe(self, observation):
        self._observation = observation

    def get_observation(self):
        return self._observation

    def add_constraint(self, constraint: Constraint):
        self._constraints.append(constraint)


@define
class ChainedValues(Distribution[T]):
    left: Node[T]
    right: Node[T]
    operator: str

    def name(self):
        return f"{self.left.name()} {self.operator} {self.right.name()}"


type Value[T] = T | ChainedValues[T] | Distribution[T] | Function[T] | Node[
    T
] | ChainedValues[Value[T]]
