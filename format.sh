#!/bin/sh

echo "Formatting python files..."
poetry run python -m isort heisig_optimiser
poetry run python -m black heisig_optimiser

echo "Formatting jinja files..."
poetry run python -m djlint 'template/index.jinja' 'template/template.jinja' --reformat

echo "Formatting js and css files..."
poetry run python -m prettier \
    --write 'template/**/*.{js,css,json,html}' \
    --ignore-path .gitignore
