from abc import ABC

from attrs import define


class Constraint(ABC): ...


@define
class LessThan(Constraint):
    left: float
