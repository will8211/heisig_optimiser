import json


def parse_requirements(node, parent_id=None, connections=None):
    """
    Recursively parse requirements
    """
    if connections is None:
        connections = []

    current_id = node["id"]
    if parent_id:
        connections.append(f"{current_id} -> {parent_id};")

    if "requirements" in node:
        for req in node["requirements"]:
            parse_requirements(req, current_id, connections)

    return connections


with open("diagrams/test.json", "r") as f:
    data = json.load(f)

# Generate connections
connections = parse_requirements(data)

# Write the blockdiag output
with open("diagrams/output.diag", "w") as f:
    f.write("blockdiag {\n")
    for connection in connections:
        f.write(f"  {connection}\n")
    f.write("}")

print("blockdiag file generated successfully.")
