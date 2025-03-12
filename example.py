import json

from src.constraints import LessThan
from src.distributions import (
    Dirichlet,
    DiscreteGamma,
    Exponential,
    LogNormal,
    PhyloCTMC,
    Sequence,
    Yule,
)
from src.functions import HKY
from src.to_json import to_json

kappa_mixture = LogNormal(meanlog=1.0, sdlog=0.5)

for i in range(2):
    kappa_mixture += LogNormal(meanlog=i, sdlog=0.5)

baseFreqs = Dirichlet(alpha=[1.0, 1.0, 1.0, 1.0])

substModel = HKY(kappa=kappa_mixture, base_frequencies=baseFreqs)

birth_rate = Exponential(rate=10.0)
birth_rate.add_constraint(LessThan(20))

phylogeny = Yule(birth_rate=birth_rate)

siteRates = DiscreteGamma(shape=0.5, categories=4)

sequences = PhyloCTMC(tree=phylogeny, Q=substModel, site_rates=siteRates)
sequences.observe(
    [
        Sequence("ACGTACGTACGTACGTACGTACGT", "human"),
        Sequence("ACGTACGTACGTACGTATGTACGT", "chimp"),
        Sequence("ACGTACGTACGCACGTACGTACG", "gorilla"),
    ],
)

with open("example.json", "w") as handle:
    json.dump(to_json(sequences, "mymodel"), handle, indent=2)
