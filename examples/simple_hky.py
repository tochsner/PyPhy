"""Basic HKY model with Yule tree prior
This example specifies an HKY substitution model with a Yule tree prior"
"""

import json

from src.constraints import LessThan
from src.distributions import (
    Dirichlet,
    DiscreteGamma,
    Exponential,
    LogNormal,
    PhyloCTMC,
    ObservedSequence,
    Yule,
)
from src.functions import HKY
from src.to_json import to_json

kappa = LogNormal(meanlog=1.0, sdlog=0.5) + Exponential(rate=1.0)
base_freqs = Dirichlet(alpha=[1.0, 1.0, 1.0, 1.0])

subst_model = HKY(kappa=kappa, base_frequencies=base_freqs)

birth_rate = Exponential(rate=10.0)
birth_rate.add_constraint(LessThan(20))

phylogeny = Yule(birth_rate=birth_rate)

site_rates = DiscreteGamma(shape=0.5, categories=4)

sequences = PhyloCTMC(tree=phylogeny, Q=subst_model, site_rates=site_rates)
sequences.observe(
    [
        ObservedSequence("ACGTACGTACGTACGTACGTACGT", "human"),
        ObservedSequence("ACGTACGTACGTACGTATGTACGT", "chimp"),
        ObservedSequence("ACGTACGTACGCACGTACGTACG", "gorilla"),
    ],
)

with open("example.json", "w") as handle:
    json.dump(to_json(sequences, "mymodel"), handle, indent=2)
