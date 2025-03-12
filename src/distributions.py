from abc import ABC
from typing import TypeVar

from attrs import define

from src.main_types import Matrix, Sequence, Tree
from src.values import Distribution, Value


T = TypeVar("T")


@define
class LogNormal(Distribution[float]):
    meanlog: Value[float]
    sdlog: Value[float]


@define
class Exponential(Distribution[float]):
    rate: Value[float]


@define
class DiscreteGamma(Distribution[list[float]]):
    shape: Value[float]
    categories: Value[int]


@define
class Dirichlet(Distribution[list[float]]):
    alpha: Value[list[float]]


@define
class Yule(Distribution[Tree]):
    birth_rate: Value[float]


@define
class PhyloCTMC(Distribution[list[Sequence]]):
    tree: Value[Tree]
    Q: Value[Matrix]
    site_rates: Value[list[float]]

    def observe(self, observation: list[Sequence]):
        super().observe(observation)
