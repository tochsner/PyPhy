#  PyPhy: A Python package to specify phylogenetic models

This package allows to specify phylogenetic models in python and to convert them into the JSON interchange format [Codephy](https://github.com/CODEPhylo/codephy).

This is a very early work in progress as an example of a way a phylogenetic interchange format could simplify the specification of phylogenetic models and make MCMC tools more accessible. See the [CODEPhylo repos](https://github.com/CODEPhylo) for more details.

## 👋 Quick start

- See the [examples](examples) folder for some example model specifications.
- Python 3.13 is required (we use modern type hints features like recursive type aliases).
- We use [Poetry](https://python-poetry.org/) for dependency management.
- Install dependencies with `poetry install`.
- Run the examples with `poetry run python examples/simple_hky.py`.
- In order to have type checking and autocompletion, use the [pylance VSCode extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance), [pyright](https://github.com/microsoft/pyright?tab=readme-ov-file), or [mypy](https://github.com/python/mypy).

## 🚀 Key features

- Allows specification of models using a familiar Python syntax, including functions, if-then-else statements, for-loops, or list comprehension.
- Excellent tooling support (autocompletion, static type checking, etc.) thanks to a fully-typed interface.

### JSON export

Define you rmodel in python and then use the `to_json` function to convert into the Codeohy JSON interchange format:

```python
...

sequence_model = PhyloCTMC(tree=phylogeny, Q=subst_model, site_rates=site_rates)

codephy_json = to_json(sequence_model, "mymodel")

with open("example.json", "w") as handle:
    json.dump(codephy_json, handle, indent=2)
```

### Typing

Random variables and scalars (and lists thereof) can be used interchangeably:

```python
# ✅ having a list of floats works
base_frequencies = [1.0, 1.0, 1.0, 1.0]
substModel = HKY(kappa=kappa, base_frequencies=base_frequencies)

# ✅ having a random variable that generates a list of floats works
base_frequencies = Dirichlet(alpha=[1.0, 1.0, 1.0, 1.0])
substModel = HKY(kappa=kappa, base_frequencies=base_frequencies)

# ✅ having a list comprehension generating a list of univariate random variables works
base_frequencies = [LogNormal(meanlog=i, sdlog=0.5) for i in range(4)]
substModel = HKY(kappa=kappa, base_frequencies=base_frequencies)

# ❌ having a list of strings fails type checking
base_frequencies = ["1.0", "1.0", "1.0", "1.0"]
substModel = HKY(kappa=kappa, base_frequencies=base_frequencies)

# ❌ having a list of Dirichlets fails type checking
base_frequencies = [Dirichlet(alpha=[1.0, 1.0, 1.0, 1.0]) for i in range(4)]
substModel = HKY(kappa=kappa, base_frequencies=base_frequencies)
```

Standard operations like addition, multiplication, and subtraction are supported on both scalars and random variables:

```python
kappa = LogNormal(meanlog=1.0, sdlog=0.5)

# ✅ we can add another univariate random variable
kappa += LogNormal(meanlog=2.0, sdlog=0.5)
kappa += Exponential(rate=10.0)

# ✅ we can also use a for loop
for i in range(2):
    kappa += LogNormal(meanlog=i, sdlog=0.5)

# ✅ we can stil pass it to the model
substModel = HKY(kappa=kappa, base_frequencies=base_frequencies)

# ❌ we can't add a Dirichlet to a LogNormal, this fails type checking
kappa += Dirichlet(alpha=[1.0, 1.0, 1.0, 1.0])
```

### Observations

Observations are specified using the `observe` method on the random variables:

```python
sequences = PhyloCTMC(tree=phylogeny, Q=subst_model, site_rates=site_rates)
sequences.observe(
    [
        ObservedSequence("ACGTACGTACGTACGTACGTACGT", taxon="human"),
        ObservedSequence("ACGTACGTACGTACGTATGTACGT", taxon="chimp"),
        ObservedSequence("ACGTACGTACGCACGTACGTACG", taxon="gorilla"),
    ],
)
```
