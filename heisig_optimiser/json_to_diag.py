import json
import os

DEFAULT_FONTSIZE = 70  # default value is 11
NODE_WIDTH = 800  # default value is 128
NODE_HEIGHT = 250  # default value is 40
SPAN_WIDTH = 250  # default value is 64
SPAN_HEIGHT = 150  # default value is 40


# Function to recursively parse requirements
def _parse_requirements(frame, parent_id=None, connections=None, nodes=None):
    if connections is None:
        connections = []
    if nodes is None:
        nodes = {}

    number = str(frame["number"]) if frame["number"] else "primitive"
    keyword = frame["keyword"].replace("‡", "")
    character = frame["character"].replace("囧", "").replace("－", "minus")
    level = frame["level"]
    current_id = frame["id"]

    label = f'"{character}\\n{keyword} ({number})"'
    background = f'"../../assets/{level}.png"'

    nodes[current_id] = {"label": label, "background": background}

    if parent_id:
        connections.append(f"{current_id} -- {parent_id} [thick];")

    if "requirements" in frame:
        for req in frame["requirements"]:
            _parse_requirements(req, current_id, connections, nodes)

    return connections, nodes


def json_to_diag():
    # Directory containing the JSON input files
    input_dir = "out/hierarchies"
    output_dir = "out/diagrams"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each JSON file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(
                output_dir, f"{os.path.splitext(filename)[0]}.diag"
            )

            # Read the JSON input
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Generate connections and labels
            connections, nodes = _parse_requirements(data)

            # Write the blockdiag output
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("blockdiag {\n")
                f.write(f"  default_fontsize = {DEFAULT_FONTSIZE}\n")
                f.write(f"  node_width = {NODE_WIDTH}\n")
                f.write(f"  node_height = {NODE_HEIGHT}\n")
                f.write(f"  span_width = {SPAN_WIDTH}\n")
                f.write(f"  span_height = {SPAN_HEIGHT}\n")
                f.write("\n")
                for node_id, node in nodes.items():
                    label = node["label"]
                    background = node["background"]
                    f.write(
                        f"  {node_id} [label = {label}, background = {background}];\n"
                    )
                if len(connections):
                    f.write("\n")
                for connection in connections:
                    f.write(f"  {connection}\n")
                f.write("}\n")

            print(f"blockdiag file generated successfully for {filename}")
