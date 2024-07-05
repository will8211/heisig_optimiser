import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import Dict, List, Literal, Set

from .generate_hierarchies import generate_hierarchies
from .build_html import add_css, add_font, add_js, json_to_html
from .output_spreadsheet import output_to_csv, output_to_json

HskLevel = Literal["Elementary", "Medium", "Advanced"]


def main():
    hsk: Dict[HskLevel, List[str]] = load_hsk_characters()
    chars: List[Dict[str, any]] = load_heisig_data()
    chars = add_hsk_levels_to_data(chars, hsk)
    chars = calculate_required_characters(chars, "Elementary")
    chars = calculate_required_characters(chars, "Medium")
    chars = calculate_required_characters(chars, "Advanced")

    output_to_json(chars)
    output_to_csv(chars)
    generate_hierarchies()
    json_to_html()
    add_js()
    add_css()
    add_font()

    print("Done")


def load_hsk_characters() -> Dict[HskLevel, List[str]]:
    """
    Read in the lists HSK characters for the three levels from disk
    """
    hsk: Dict[HskLevel, List[str]] = {}
    levels: List[HskLevel] = ["Elementary", "Medium", "Advanced"]
    for level in levels:
        try:
            with open(f"data/hsk/{level}.txt", "r") as file:
                hsk[level] = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"Warning: {level}.txt not found. Did you run `./data/populate.sh`?")
            hsk[level] = []
    return hsk


def load_heisig_data() -> List[Dict[str, any]]:
    """
    Read in the Heisig data from the .xml file
    """
    tree = ET.parse("data/heisig/rsh_modified.xml")
    root = tree.getroot()
    chars: List[Dict[str, any]] = []
    order = 0
    for book in root.iter("book"):
        chapter_tags = ["lesson", "compounds", "postscript"]
        chapters = [elem for tag in chapter_tags for elem in book.iter(tag)]
        for chapter in chapters:
            for frame in chapter.iter("frame"):
                char = defaultdict(lambda: None)
                number = frame.attrib.get("number")
                char["Book"] = book.attrib.get("number")
                char["Lesson"] = (
                    chapter.attrib.get("number") if chapter.tag == "lesson" else ""
                )
                char["Number"] = int(number) if number else None
                char["Character"] = frame.attrib.get("character")
                char["Type"] = frame.attrib.get(
                    "{http://www.w3.org/2001/XMLSchema-instance}type"
                )
                char["Keywords"] = [frame.attrib.get("keyword")]
                char["Order"] = order
                order += 1

                alternate_keywords = frame.findall(".//pself")
                for e in alternate_keywords:
                    if e.text not in char["Keywords"]:
                        char["Keywords"].append(e.text)

                cite_elems = frame.findall(".//cite")
                char["Requires"] = []
                for e in cite_elems:
                    char["Requires"].append(e.text)

                chars.append(char)

    return chars


def add_hsk_levels_to_data(
    chars: List[Dict[str, any]], hsk: Dict[HskLevel, List[str]]
) -> List[Dict[str, any]]:
    """
    Add a HSK level of each Heisig character to the data
    """
    for char in chars:
        char["Level"] = None
        for level, characters in hsk.items():
            if char["Character"] in characters:
                char["Level"] = level
                break
    return chars


def calculate_required_characters(
    chars: List[Dict[str, any]], hsk_level: HskLevel
) -> List[Dict[str, any]]:
    """
    Add the 'Required for' column to the Heisig characters to indicate
    the lowest level for which the character is required as a dependency
    """
    requirements: Dict[int, Set[str]] = {}
    depth = 0

    # Initialize the first level of dependencies
    requirements[depth] = set()

    # Go through the characters of this HSK level and get their dependencies
    for c in chars:
        if not c["Required for"] and c["Level"] == hsk_level:
            c["Required for"] = hsk_level
            requirements[depth].update(c["Requires"])

    # Increment depth to start processing subdependencies
    depth += 1

    # Loop through the dependencies and mark them as required, get their subdependencies
    while requirements.get(depth - 1):
        requirements[depth] = set()
        for c in chars:
            if not c["Required for"]:
                for name in c["Keywords"]:
                    if name in requirements[depth - 1]:
                        c["Required for"] = f"{hsk_level}"
                        requirements[depth].update(c["Requires"])
        depth += 1
    return chars


main()
