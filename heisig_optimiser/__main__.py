import xml.etree.ElementTree as ET
from typing import Dict, Set

from tabulate import tabulate

## Load HSK characters
hsk = {}
levels = ["Elementary", "Medium", "Advanced"]
for level in levels:
    with open(f"data/{level}.txt", "r") as file:
        hsk[level] = [line.strip() for line in file.readlines()]

## Loag Heisig data
chars = []
tree = ET.parse("data/rsh.xml")
root = tree.getroot()
for frame in root.iter("frame"):
    char = {}
    number = frame.attrib.get("number")
    char["No."] = int(number) if number else None
    char["Character"] = frame.attrib.get("character")
    char["Type"] = frame.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}type")
    char["Keywords"] = [frame.attrib.get("keyword")]

    alternate_keywoords = frame.findall(".//pself")
    for e in alternate_keywoords:
        if e.text not in char["Keywords"]:
            char["Keywords"].append(e.text)

    cite_elems = frame.findall(".//cite")
    char["Requires"] = []
    for e in cite_elems:
        char["Requires"].append(e.text)

    chars.append(char)

## Add HSK levels to characters
for char in chars:
    char["Level"] = None
    for level in levels:
        if char["Character"] in hsk[level]:
            char["Level"] = level
            break

## Mark characters needed at an earlier level:
requirements: Dict[int, Set[str]] = {}
depth = 0

# Initialize the first level of dependencies
requirements[depth] = set()

# Go through the elementary characters and get their dependiencies
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
            for name in c["Keywords"]:
                if name in requirements[depth - 1]:
                    c["Required for"] = f"Elementary ({depth})"
                    requirements[depth].update(c["Requires"])
    depth += 1

## Prepare csv output
headers = [
    "No.",
    "Character",
    "Type",
    "Level",
    "Required for",
    "Keywords",
    "Requires",
]

ordered_data = [[row[header] for header in headers] for row in chars]
csv = tabulate(ordered_data, headers=headers, tablefmt="tsv")
csv = "\n".join([line.replace("[", "").replace("]", "") for line in csv.split("\n")])

with open("out/out.csv", "w") as f:
    f.write(csv)
