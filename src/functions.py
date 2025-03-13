from typing import Sequence
from attrs import define

from src.main_types import Matrix
from src.values import Function, Value


@define
class HKY(Function[Matrix]):
    kappa: Value[float]
    base_frequencies: Value[Sequence[Value[float]]]


@define
class GTR(Function[Matrix]):
    rate_matrix: Value[Sequence[Value[float]]]
    base_frequencies: Value[Sequence[Value[float]]]
