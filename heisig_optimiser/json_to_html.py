import json
import os

from jinja2 import Environment, FileSystemLoader


def json_to_diag():
    # Directory containing the JSON input files
    input_dir = "out/hierarchies"
    output_dir = "d3/html"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each JSON file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(
                output_dir, f"{os.path.splitext(filename)[0]}.html"
            )

            # Read the JSON input
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Load the template
            env = Environment(loader=FileSystemLoader("d3"))
            template = env.get_template("template.jinja")

            # Render the template with your data
            rendered_html = template.render(data_json=json.dumps(data))

            # Write the output to a new HTML file
            with open(output_path, "w") as f:
                f.write(rendered_html)

            print(f"html file generated successfully for {filename}")
            input()


json_to_diag()
