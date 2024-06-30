#!/bin/sh

poetry run python -m isort heisig_optimiser
poetry run python -m black heisig_optimiser
