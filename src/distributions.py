from abc import ABC
from typing import Sequence, TypeVar

from attrs import define

from src.main_types import Matrix, ObservedSequence, Tree
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
    alpha: Value[Sequence[Value[float]]]


@define
class CTMCRateMatrix(Distribution[Matrix]):
    dimension: Value[int]
    prior: Value[float]


@define
class DiscreteTrait(Distribution[Matrix]):
    states: Value[Sequence[Value[str]]]
    rateMatrix: Value[Matrix]


@define
class Yule(Distribution[Tree]):
    birth_rate: Value[float]


@define
class BirthDeath(Distribution[Tree]):
    birth_rate: Value[float]
    death_rate: Value[float]


@define
class PhyloCTMC(Distribution[list[ObservedSequence]]):
    tree: Value[Tree]
    Q: Value[Matrix]
    site_rates: Value[Sequence[Value[float]]]

    def observe(self, observation: list[ObservedSequence]):
        super().observe(observation)


@define
class DiscreteTraitPhyloCTMC(Distribution[list[ObservedSequence]]):
    tree: Value[Tree]
    Q: Value[Matrix]

    def observe(self, observation: list[ObservedSequence]):
        super().observe(observation)
