from abc import ABC
from typing import Generic, TypeVar

T = TypeVar("T")


class Tree(ABC): ...


class Matrix(Generic[T]): ...

