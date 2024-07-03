import json
import os


def _increment_id(letter: str):
    byte_val = bytes(letter, "utf-8")
    incremented = bytes([byte_val[0] + 1])
    return incremented.decode("utf-8")


# Function to recursively build the hierarchy
def _build_hierarchy(character, character_map, visited=None):
    global id
    if visited is None:
        visited = set()

    if character in visited:
        return None  # Detected a cycle, return None to avoid infinite recursion

    visited.add(character)

    character_data = character_map[character]
    requirements = []
    processed_characters = set()  # Track characters added to requirements
    for req in character_data["Requires"]:
        # Find the character that matches the requirement keyword
        req_character = next(
            (char for char, data in character_map.items() if req in data["Keywords"]),
            None,
        )
        if req_character and req_character not in processed_characters:
            req_hierarchy = _build_hierarchy(req_character, character_map, visited)
            if req_hierarchy:
                requirements.append(req_hierarchy)
                processed_characters.add(
                    req_character
                )  # Mark this character as processed

    visited.remove(character)  # Remove character from visited after processing

    id = _increment_id(id)
    return {
        "number": str(character_data["Number"]) if character_data["Number"] else None,
        "character": character_data["Character"],
        "keyword": character_data["Keywords"][0],
        "level": character_data["Level"],
        "id": id,
        "requirements": requirements,
    }


def generate_hierarchies():
    global id
    id = "A"

    # Read the input JSON
    with open("out/out.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Create a mapping from character names to their data
    character_map = {item["Character"]: item for item in data}

    # Ensure the output directory exists
    output_dir = "out/hierarchies"
    os.makedirs(output_dir, exist_ok=True)

    # Process each character and write the hierarchy to a file
    for character_data in data:
        id = "A"
        character = character_data["Character"]
        number = character_data["Number"]
        first_keyword = character_data["Keywords"][0]
        hierarchy = _build_hierarchy(character, character_map)
        if hierarchy:
            output_file = (
                os.path.join(output_dir, f"{number or 'extra'}_{first_keyword}.json")
                .replace(" ", "_")
                .replace("?", "")
                .replace("'", "_")
                .replace("‡", "")
            )
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(hierarchy, f, ensure_ascii=False, indent=2)

    print("Hierarchical JSON files generated successfully.")
