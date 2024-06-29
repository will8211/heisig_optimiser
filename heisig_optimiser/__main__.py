import xml.etree.ElementTree as ET
from typing import Dict, Set

from tabulate import tabulate

START = 0
END = 3000
BOOK_ONE_ONLY = False

tree = ET.parse("data/rsh.xml")
root = tree.getroot()


if BOOK_ONE_ONLY:
    scope = root.findall("book")[0]
else:
    scope = root

chars = []

levels = ["Elementary", "Medium", "Advanced"]
hsk = {}
for level in levels:
    with open(f"data/{level}.txt", "r") as file:
        hsk[level] = [line.strip() for line in file.readlines()]

for frame in root.iter("frame"):
    char = {}
    char["No."] = frame.attrib.get("number")
    char["Char."] = frame.attrib.get("character")
    char["Type"] = frame.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}type")

    char["Level"] = None
    for level in levels:
        if char["Char."] in hsk[level]:
            char["Level"] = level
            break

    char["Keyword"] = frame.attrib.get("keyword")

    pself_elems = frame.findall(".//pself")
    char["A.K.A."] = []
    for e in pself_elems:
        if e.text != char["Keyword"]:
            char["A.K.A."].append(e.text)

    cite_elems = frame.findall(".//cite")
    char["Requires"] = []
    for e in cite_elems:
        char["Requires"].append(e.text)

    chars.append(char)


deps: Dict[int, Set[str]] = {}
depth = 0

# Initialize the first level of dependencies
deps[depth] = set()

# Go through the elementary characters and get their deps
for c in chars:
    c["Required for"] = None
    if c["Level"] == "Elementary":
        c["Required for"] = f"Elementary ({depth})"
        deps[depth].update(c["Requires"])

# Increment depth to start processing subdependencies
depth += 1

# Loop through the dependencies and mark them as required, get their subdependencies
while deps[depth - 1]:
    deps[depth] = set()
    for c in chars:
        if not c["Required for"]:
            for name in [c["Keyword"]] + c["A.K.A."]:
                if name in deps[depth - 1]:
                    c["Required for"] = f"Elementary ({depth})"
                    deps[depth].update(c["Requires"])
    depth += 1


filtered_rows = []
for c in chars:
    if c["Required for"] is not None and c["No."]:
        number = int(c["No."])
        if number > START and number < END:
            filtered_rows.append(c)

csv = tabulate(filtered_rows, headers="keys", tablefmt="tsv")
csv = "\n".join([line.replace("[", "").replace("]", "") for line in csv.split("\n")])

with open("out/out.csv", "w") as f:
    f.write(csv)
