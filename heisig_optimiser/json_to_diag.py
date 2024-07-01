import json
import os


# Function to recursively parse requirements
def parse_requirements(node, parent_id=None, connections=None, labels=None):
    if connections is None:
        connections = []
    if labels is None:
        labels = {}

    current_character = node["character"]
    number = str(node["number"]) if node["number"] else "*"
    current_label = f"{node['character']}\\n{number} {node['keyword']}"
    labels[current_character] = current_label

    if parent_id:
        connections.append(f"{current_character} -> {parent_id};")

    if "requirements" in node:
        for req in node["requirements"]:
            parse_requirements(req, current_character, connections, labels)

    return connections, labels


# Directory containing the JSON input files
input_dir = "out/decomposition"
output_dir = "diagrams"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process each JSON file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.diag")

        # Read the JSON input
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Generate connections and labels
        connections, labels = parse_requirements(data)

        # Write the blockdiag output
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("blockdiag {\n")
            for node_id, label in labels.items():
                f.write(f'  {node_id} [label = "{label}"];\n')
            for connection in connections:
                f.write(f"  {connection}\n")
            f.write("}")

        print(f"blockdiag file generated successfully for {filename}")
