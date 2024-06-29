import xml.etree.ElementTree as ET

from tabulate import tabulate

tree = ET.parse("data/rsh.xml")
root = tree.getroot()
book = root.findall("book")[0]
chars = []

levels = ["Elementary", "Medium", "Advanced"]
hsk = {}
for level in levels:
    with open(f"data/{level}.txt", "r") as file:
        hsk[level] = [line.strip() for line in file.readlines()]

for frame in book.iter("frame"):
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

print(tabulate(chars, headers="keys", tablefmt="github"))
