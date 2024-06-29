#!/bin/sh

poetry run python -m heisig_optimiser | sed 's/[][]//g' > out.md
