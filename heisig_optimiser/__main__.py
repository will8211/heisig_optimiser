from ast import keyword
import xml.etree.ElementTree as ET

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
    char["number"] = frame.attrib.get("number")
    char["character"] = frame.attrib.get("character")
    char["type"] = frame.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}type")

    char["level"] = None
    for level in levels:
        if char["character"] in hsk[level]:
            char["level"] = level
            break

    char["keyword"] = frame.attrib.get("keyword")

    pself_elems = frame.findall(".//pself")
    char["aka"] = []
    for e in pself_elems:
        if e.text != char["keyword"]:
            char["aka"].append(e.text)

    cite_elems = frame.findall(".//cite")
    char["uses"] = []
    for e in cite_elems:
        char["uses"].append(e.text)

    chars.append(char)


deps = {}

depth = 0

# Go through the elementary characters and get their deps
deps[1] = set()
for c in chars:
    c["required"] = None
    if c["level"] == "Elementary":
        c["required"] = f"Elementary ({depth})"
        deps[1].update(c["uses"])

# Find the dependencies, mark them as requires, and get their subdependencies
deps[2] = set()
for c in chars:
     if not c["required"]:
        for name in [c["keyword"]] + c["aka"]:
            if name in deps[depth + 1]:
                c["required"] = f"Elementary ({depth + 1})"
                deps[depth + 2].update(c["uses"])


while len(deps[depth + 1]):
    depth += 1
    deps[depth + 2] = set()
    for c in chars:
        if not c["required"]:
            for name in [c["keyword"]] + c["aka"]:
                if name in deps[depth + 1]:
                    c["required"] = f"Elementary ({depth + 1})"
                    deps[depth + 2].update(c["uses"])

filtered_rows = []
for c in chars:
    if c["required"] is not None and c["number"]:
        number = int(c["number"])
        if number > START and number < END:
            filtered_rows.append(c)

csv = tabulate(filtered_rows, headers="keys", tablefmt="tsv", showindex="always")
csv = "\n".join([line.replace("[", "").replace("]", "") for line in csv.split("\n")])

with open("out/out.csv", "w") as f:
    f.write(csv)
