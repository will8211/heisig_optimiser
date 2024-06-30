import xml.etree.ElementTree as ET
from typing import Dict, List, Literal, Set

from tabulate import tabulate

Level = Literal["Elementary", "Medium", "Advanced"]


def main():
    hsk: Dict[Level, List[str]] = load_hsk_characters()
    chars: List[Dict[str, any]] = load_heisig_data()
    chars = add_hsk_levels_to_data(chars, hsk)
    chars = calculate_required_characters(chars)
    output_to_csv(chars)


def load_hsk_characters() -> Dict[Level, List[str]]:
    """
    Read in the lists HSK characters for the three levels from disk
    """
    hsk: Dict[Level, List[str]] = {}
    levels: List[Level] = ["Elementary", "Medium", "Advanced"]
    for level in levels:
        with open(f"data/{level}.txt", "r") as file:
            hsk[level] = [line.strip() for line in file.readlines()]
    return hsk


def load_heisig_data() -> Dict[Level, List[str]]:
    """
    Read in the Heisig data from the .xml file
    """
    tree = ET.parse("data/rsh.xml")
    root = tree.getroot()
    chars: List[Dict[str, any]] = []
    for frame in root.iter("frame"):
        char = {}
        number = frame.attrib.get("number")
        char["No."] = int(number) if number else None
        char["Character"] = frame.attrib.get("character")
        char["Type"] = frame.attrib.get(
            "{http://www.w3.org/2001/XMLSchema-instance}type"
        )
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

    return chars


def add_hsk_levels_to_data(
    chars: List[Dict[str, any]], hsk: Dict[Level, List[str]]
) -> Dict[Level, List[str]]:
    """
    Add a HSK level of each Heisig character to the data
    """
    for char in chars:
        char["Level"] = None
        for level in hsk.keys():
            if char["Character"] in hsk[level]:
                char["Level"] = level
                break
    return chars


def calculate_required_characters(
    chars: List[Dict[str, any]]
) -> Dict[Level, List[str]]:
    """
    Add the 'Required for' column to the Heisig characters to indicate
    the lowest level for which the character is required as a dependency
    """
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
    return chars


def output_to_csv(chars: List[Dict[str, any]]):
    """
    Write out the enriched Heisig data to a .csv file
    """
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
    csv = "\n".join(
        [line.replace("[", "").replace("]", "") for line in csv.split("\n")]
    )
    with open("out/out.csv", "w") as f:
        f.write(csv)


main()
