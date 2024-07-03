#!/bin/bash

# Doesn't seem to work

# sudo apt-get install fontforge
# pip install fonttools brotli
# fontforge -lang=ff -c 'Open($1); Generate($1:r + ".fixed.otf")' HanaMinB.otf
# pyftsubset "HanaMinB.fixed.otf" --flavor=woff2 --output-file="HanaMinB.woff2" --unicodes="U+20000-2A6DF" --drop-tables+=FFTM

# This either:

# npm install -g ttf2woff2
# ttf2woff2 < "HanaMinB.otf" > "HanaMinB.woff2"
