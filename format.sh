#!/bin/sh

echo "Formatting python files..."
poetry run python -m isort heisig_optimiser
poetry run python -m black heisig_optimiser

echo "Formatting jinja files..."
poetry run python -m djlint template/*.jinja --reformat

echo "Formatting js and css files..."
poetry run js-beautify --end-with-newline --indent-size 2 --replace template/*.js
poetry run css-beautify --end-with-newline --indent-size 2 --replace template/*.css
