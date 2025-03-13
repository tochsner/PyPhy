import json

from src.constraints import LessThan
from src.distributions import (
    BirthDeath,
    CTMCRateMatrix,
    Dirichlet,
    DiscreteGamma,
    DiscreteTrait,
    DiscreteTraitPhyloCTMC,
    Exponential,
    LogNormal,
    PhyloCTMC,
    DNASequence,
    Yule,
)
from src.functions import GTR
from src.to_json import to_json

# Discrete trait evolution model (PhyloSpec-aligned)
# This example demonstrates a model for the evolution of a discrete trait
# (geographic location) along with sequence evolution.

# --- Substitution Model for Sequence Data ---

# GTR substitution model
base_frequencies = Dirichlet(alpha=[1.0, 1.0, 1.0, 1.0])
rate_params = [Exponential(rate=10.0) for _ in range(6)]

seq_model = GTR(rate_matrix=rate_params, base_frequencies=base_frequencies)

# --- Tree Prior ---

# Birth-death parameters
birth_rate = Exponential(rate=10.0)
death_rate = Exponential(rate=20.0)

# Create birth-death tree
phylogeny = BirthDeath(birth_rate=birth_rate, death_rate=death_rate)

# --- Trait Evolution Model ---

# Define possible geographic regions
regions = ["Africa", "Asia", "Europe", "North_America"]

# Asymmetric transition rates between regions
qMatrix = CTMCRateMatrix(dimension=4, prior=Exponential(rate=10.0))

# Trait substitution model
traitModel = DiscreteTrait(states=regions, rateMatrix=qMatrix)

# --- Trait Data ---

# Simulate trait evolution
geoTraits = DiscreteTraitPhyloCTMC(tree=phylogeny, Q=traitModel)
geoTraits.observe(
    [
        DNASequence("Africa", "taxon1"),
        DNASequence("Africa", "taxon2"),
        DNASequence("Asia", "taxon3"),
        DNASequence("Asia", "taxon4"),
        DNASequence("Asia", "taxon5"),
        DNASequence("Europe", "taxon6"),
        DNASequence("Europe", "taxon7"),
        DNASequence("Europe", "taxon8"),
        DNASequence("North_America", "taxon9"),
        DNASequence("North_America", "taxon10"),
        DNASequence("Africa", "taxon11"),
        DNASequence("Asia", "taxon12"),
        DNASequence("Asia", "taxon13"),
        DNASequence("Europe", "taxon14"),
        DNASequence("North_America", "taxon15"),
        DNASequence("North_America", "taxon16"),
        DNASequence("Asia", "taxon17"),
        DNASequence("Europe", "taxon18"),
        DNASequence("Europe", "taxon19"),
        DNASequence("North_America", "taxon20"),
    ]
)

# --- Sequence Data ---

# Create phylogenetic CTMC model for sequences
sequences = PhyloCTMC(tree=phylogeny, Q=seq_model, site_rates=[1.0, 1.0, 1.0, 1.0])
# sequences.observe()

with open("example.json", "w") as handle:
    json.dump(to_json(sequences, "mymodel"), handle, indent=2)
