from __future__ import annotations
from abc import ABC
from typing import Generic, TypeVar

from attrs import define

from src.constraints import Constraint

T = TypeVar("T")


class Node(ABC, Generic[T]):
    _used_names: set[str] = set()

    def __add__(self, other: Node[T]):
        return ChainedValues(self, other, "+")

    def __sub__(self, other: Node[T]):
        return ChainedValues(self, other, "-")

    def __mul__(self, other: Node[T]):
        return ChainedValues(self, other, "*")

    def name(self):
        if hasattr(self, "_name"):
            return self._name

        name = type(self).__name__

        suffix = 2
        while name in self._used_names:
            name = f"{type(self).__name__}_{suffix}"
            suffix += 1

        self._used_names.add(name)
        self._name = name

        return name


class Function(Generic[T], Node[T]): ...


class Distribution(Generic[T], Node[T]):

    def observe(self, observation):
        self._observation = observation

    def get_observation(self):
        return self._observation if hasattr(self, "_observation") else None

    def add_constraint(self, constraint: Constraint):
        if not hasattr(self, "_observation"):
            self._constraints = []

        self._constraints.append(constraint)


@define
class ChainedValues(Distribution[T]):
    left: Node[T]
    right: Node[T]
    operator: str

    def name(self):
        return f"{self.left.name()} {self.operator} {self.right.name()}"


type Value[T] = T | ChainedValues[T] | Distribution[T] | Function[T] | Node[T] | ChainedValues[Value[T]]
