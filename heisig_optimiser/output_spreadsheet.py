import csv
import json
from typing import Dict, List


def _format_cell(cell):
    """
    Convert lists to strings without square brackets
    """
    if isinstance(cell, list):
        return '"' + '", "'.join(cell) + '"' if cell else None
    return cell


def output_to_json(chars: List[Dict[str, any]]):
    """
    Write the data out to a json file
    """
    with open("out/out.json", "w", newline="", encoding="utf-8") as f:
        json.dump(chars, f, indent=2, ensure_ascii=False)


def output_to_csv(chars: List[Dict[str, any]]):
    """
    Write out the enriched Heisig data to a .csv file
    """
    headers = [
        "Book",
        "Lesson",
        "Number",
        "Character",
        "Type",
        "Level",
        "Required for",
        "Keywords",
        "Requires",
    ]

    formatted_data = [
        [_format_cell(row.get(header)) for header in headers] for row in chars
    ]

    with open("out/out.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(formatted_data)
