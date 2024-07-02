#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")

curl https://raw.githubusercontent.com/rouseabout/heisig/master/rsh.xml >"${SCRIPT_DIR}"/heisig/rsh.xml
curl https://raw.githubusercontent.com/krmanik/HSK-3.0/main/HSK%20Handwritten/Elementary.txt >"${SCRIPT_DIR}"/hsk/Elementary.txt
curl https://raw.githubusercontent.com/krmanik/HSK-3.0/main/HSK%20Handwritten/Medium.txt >"${SCRIPT_DIR}"/hsk/Medium.txt
curl https://raw.githubusercontent.com/krmanik/HSK-3.0/main/HSK%20Handwritten/Advanced.txt >"${SCRIPT_DIR}"hsk/Advanced.txt
