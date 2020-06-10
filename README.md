# EIP1559 Simulations

**Requires [poetry](https://python-poetry.org/docs/#system-requirements)**

## Quick start:
1. poetry install
2. poetry run python seasonality.py 4 32 60

## Scripts Explanation

- `back_to_normal` prints how many blocks of a certain size are needed to get back to the initial basefee amount after a prolonged period of congestion
- `exponential` prints an exponential graph of y=1.125^x where x is the number of blokcs since the start of the experiment
- `path` shows that EIP1559 is path independent for same-length paths, but path dependent favoring smaller paths with smaller basefee increases
- `seasonality` shows the behavior of the basefee when there's a seasonality (e.g. 4h of low demand, 4h of high demand)
- `utils` contains various utilities for calculating fees etc.
