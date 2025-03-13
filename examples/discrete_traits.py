"""Discrete trait evolution model
This example demonstrates a model for the evolution of a discrete trait
(geographic location) along with sequence evolution.
"""
import json

from src.distributions import (
    BirthDeath,
    CTMCRateMatrix,
    Dirichlet,
    DiscreteTrait,
    DiscreteTraitPhyloCTMC,
    Exponential,
    PhyloCTMC,
    ObservedSequence,
)
from src.functions import GTR
from src.to_json import to_json


# Substitution Model for Sequence Data

base_frequencies = Dirichlet(alpha=[1.0, 1.0, 1.0, 1.0])
rate_params = [Exponential(rate=10.0) for _ in range(6)]

seq_model = GTR(rates=rate_params, base_frequencies=base_frequencies)

# Tree Prior

birth_rate = Exponential(rate=10.0)
death_rate = Exponential(rate=20.0)

phylogeny = BirthDeath(birth_rate=birth_rate, death_rate=death_rate)

# Trait Evolution Model

regions = ["Africa", "Asia", "Europe", "North_America"]
qMatrix = CTMCRateMatrix(dimension=4, prior=Exponential(rate=10.0))

traitModel = DiscreteTrait(states=regions, rateMatrix=qMatrix)

# Trait Data

geoTraits = DiscreteTraitPhyloCTMC(tree=phylogeny, Q=traitModel)
geoTraits.observe(
    [
        ObservedSequence("Africa", "taxon1"),
        ObservedSequence("Africa", "taxon2"),
        ObservedSequence("Asia", "taxon3"),
        ObservedSequence("Asia", "taxon4"),
        ObservedSequence("Asia", "taxon5"),
        ObservedSequence("Europe", "taxon6"),
        ObservedSequence("Europe", "taxon7"),
        ObservedSequence("Europe", "taxon8"),
        ObservedSequence("North_America", "taxon9"),
        ObservedSequence("North_America", "taxon10"),
        ObservedSequence("Africa", "taxon11"),
        ObservedSequence("Asia", "taxon12"),
        ObservedSequence("Asia", "taxon13"),
        ObservedSequence("Europe", "taxon14"),
        ObservedSequence("North_America", "taxon15"),
        ObservedSequence("North_America", "taxon16"),
        ObservedSequence("Asia", "taxon17"),
        ObservedSequence("Europe", "taxon18"),
        ObservedSequence("Europe", "taxon19"),
        ObservedSequence("North_America", "taxon20"),
    ]
)

# Sequence Data

sequences = PhyloCTMC(tree=phylogeny, Q=seq_model, site_rates=[1.0, 1.0, 1.0, 1.0])
# sequences.observeFromFile("sequences.fasta")

with open("example.json", "w") as handle:
    json.dump(to_json(sequences, "mymodel"), handle, indent=2)
