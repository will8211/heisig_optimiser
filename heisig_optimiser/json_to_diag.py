import json
import os


def sanitize_cjk(string):
    if not string:
        return string
    for char in string:
        if not char == "－" and not "\u4E00" <= char <= "\u9FFF":
            # return str(sum([ord(x) for x in string]))
            return f'"{string}"'
    return string


# Function to recursively parse requirements
def parse_requirements(node, parent_id=None, connections=None, labels=None):
    if connections is None:
        connections = []
    if labels is None:
        labels = {}

    current_character = node["character"]
    safe_current_character = sanitize_cjk(current_character)
    safe_parent_id = sanitize_cjk(parent_id)
    number = str(node["number"]) if node["number"] else "*"
    current_label = f"{node['character']}\\n{number} {node['keyword']}"
    labels[safe_current_character] = current_label

    if parent_id:
        connections.append(f"{safe_current_character} -> {safe_parent_id} [thick];")

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
            f.write("  default_fontsize = 110\n")  # default value is 11
            f.write("  node_width = 1280\n")  # default value is 128
            f.write("  node_height = 400\n")  # default value is 40
            f.write("  span_width = 640\n")  # default value is 64
            f.write("  span_height = 400\n")  # default value is 40
            f.write("\n")
            for node_id, label in labels.items():
                f.write(f'  {node_id} [label = "{label}"];\n')
            if len(connections):
                f.write("\n")
            for connection in connections:
                f.write(f"  {connection}\n")
            f.write("}")

        print(f"blockdiag file generated successfully for {filename}")
