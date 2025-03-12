from attrs import define

from src.main_types import Matrix
from src.values import Function, Value


@define
class HKY(Function[Matrix]):
    kappa: Value[float]
    base_frequencies: Value[list[float]]
