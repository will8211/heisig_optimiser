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

deps_1 = set()
for c in chars:
    c["degs"] = None
    if c["level"] == "Elementary":
        c["degs"] = 0
        deps_1.update(c["uses"])

for c in chars:
    if c["level"] != "Elementary":
        for name in [c["keyword"]] + c["aka"]:
            if name in deps_1:
                c["degs"] = 1

deps_2 = set()
for c in chars:
    if c["degs"] == 1:
        deps_2.update(c["uses"])

for c in chars:
    if not c["degs"]:
        for name in [c["keyword"]] + c["aka"]:
            if name in deps_2:
                c["degs"] = 2

deps_3 = set()
for c in chars:
    if c["degs"] == 2:
        deps_3.update(c["uses"])

for c in chars:
    if not c["degs"]:
        for name in [c["keyword"]] + c["aka"]:
            if name in deps_3:
                c["degs"] = 3


deps_4 = set()
for c in chars:
    if c["degs"] == 3:
        deps_4.update(c["uses"])

for c in chars:
    if not c["degs"]:
        for name in [c["keyword"]] + c["aka"]:
            if name in deps_4:
                c["degs"] = 4

deps_5 = set()
for c in chars:
    if c["degs"] == 4:
        deps_5.update(c["uses"])

for c in chars:
    if not c["degs"]:
        for name in [c["keyword"]] + c["aka"]:
            if name in deps_5:
                c["degs"] = 5

deps_6 = set()
for c in chars:
    if c["degs"] == 5:
        deps_6.update(c["uses"])

for c in chars:
    if not c["degs"]:
        for name in [c["keyword"]] + c["aka"]:
            if name in deps_6:
                c["degs"] = 6

deps_7 = set()
for c in chars:
    if c["degs"] == 6:
        deps_7.update(c["uses"])

for c in chars:
    if not c["degs"]:
        for name in [c["keyword"]] + c["aka"]:
            if name in deps_7:
                c["degs"] = 7

deps_8 = set()
for c in chars:
    if c["degs"] == 7:
        deps_8.update(c["uses"])

for c in chars:
    if not c["degs"]:
        for name in [c["keyword"]] + c["aka"]:
            if name in deps_8:
                c["degs"] = 8

filtered_rows = []
for c in chars:
    if c["degs"] is not None and c["number"]:
        number = int(c["number"])
        if number > START and number < END:
            filtered_rows.append(c)

csv = tabulate(filtered_rows, headers="keys", tablefmt="tsv", showindex="always")
csv = "\n".join([line.replace("[", "").replace("]", "") for line in csv.split("\n")])

with open("out/out.csv", "w") as f:
    f.write(csv)
