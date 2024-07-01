import json


# Function to recursively parse requirements
def parse_requirements(node, parent_id=None, connections=None, labels=None):
    if connections is None:
        connections = []
    if labels is None:
        labels = {}

    current_id = node["id"]
    current_label = node.get("label", "")
    if current_label:
        parts = current_label.split("\n")
        full_label = f"{parts[0]}\\n{current_id} {parts[1]}"
    else:
        full_label = str(current_id)
    labels[current_id] = full_label

    if parent_id:
        connections.append(f"{current_id} -> {parent_id};")

    if "requirements" in node:
        for req in node["requirements"]:
            parse_requirements(req, current_id, connections, labels)

    return connections, labels


# Read the JSON input
with open("diagrams/test.json", "r") as f:
    data = json.load(f)

# Generate connections and labels
connections, labels = parse_requirements(data)

# Write the blockdiag output
with open("diagrams/output.diag", "w") as f:
    f.write("blockdiag {\n")
    for node_id, label in labels.items():
        f.write(f'  {node_id} [label = "{label}"];\n')
    for connection in connections:
        f.write(f"  {connection}\n")
    f.write("}")

print("blockdiag file generated successfully.")
