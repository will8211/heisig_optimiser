import xml.etree.ElementTree as ET
from typing import Dict, Set

from tabulate import tabulate

START = 0
END = 500001
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
    number = frame.attrib.get("number")
    char["No."] = int(number) if number else None
    char["Character"] = frame.attrib.get("character")
    char["Type"] = frame.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}type")

    char["Level"] = None
    for level in levels:
        if char["Character"] in hsk[level]:
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


requirements: Dict[int, Set[str]] = {}
depth = 0

# Initialize the first level of dependencies
requirements[depth] = set()

# Go through the elementary characters and get their deps
for c in chars:
    c["Required for"] = None
    if c["Level"] == "Elementary":
        c["Required for"] = f"Elementary"
        requirements[depth].update(c["Requires"])

# Increment depth to start processing subdependencies
depth += 1

# Loop through the dependencies and mark them as required, get their subdependencies
while requirements[depth - 1]:
    requirements[depth] = set()
    for c in chars:
        if not c["Required for"]:
            for name in [c["Keyword"]] + c["A.K.A."]:
                if name in requirements[depth - 1]:
                    c["Required for"] = f"Elementary ({depth})"
                    requirements[depth].update(c["Requires"])
    depth += 1

add_to_filtered = False
filtered_rows = []
for c in chars:
    number = c["No."]
    if number and number > END:
        add_to_filtered = False
    elif number and number >= START:
        add_to_filtered = True
    if add_to_filtered:
        filtered_rows.append(c)

headers = [
    "No.",
    "Character",
    "Type",
    "Level",
    "Required for",
    "Keyword",
    "A.K.A.",
    "Requires",
]

ordered_data = [[row[header] for header in headers] for row in filtered_rows]

csv = tabulate(ordered_data, headers=headers, tablefmt="tsv")
csv = "\n".join([line.replace("[", "").replace("]", "") for line in csv.split("\n")])

with open("out/out.csv", "w") as f:
    f.write(csv)
