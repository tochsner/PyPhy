# PyPhy: A Python package to specify phylogenetic models

This package allows to specify phylogenetic models in python and to convert them into the JSON interchange format [Codephy](https://github.com/CODEPhylo/codephy).

This is a very early work in progress as an example of a way a phylogenetic interchange format could simplify the specification of phylogenetic models and make MCMC tools more accessible. See the [CODEPhylo repos](https://github.com/CODEPhylo) for more details.

## Key features

- Allows specification of models using a familiar Python syntax, including functions, if-then-else statements, for-loops, or list comprehension.
- Excellent tooling support (autocompletion, static type checking, etc.) thanks to a fully-typed interface.

## Getting started

- Python 3.13 is required (we use modern type hints features like recursive type aliases).
- We use [Poetry](https://python-poetry.org/) for dependency management.
- Install dependencies with `poetry install`.
- Run the examples with `poetry run python examples/simple_hky.py`.
- In order to have type checking and autocompletion, use the [pylance VSCode extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance), [pyright](https://github.com/microsoft/pyright?tab=readme-ov-file), or [mypy](https://github.com/python/mypy).