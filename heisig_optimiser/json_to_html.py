import json
import os

from jinja2 import Environment, FileSystemLoader

input_dir = "out/hierarchies"
output_dir = "d3/html"
env = Environment(loader=FileSystemLoader("d3"))


def json_to_diag():
    # Directory containing the JSON input files

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
            template = env.get_template("template.jinja")

            # Render the template with your data
            rendered_html = template.render(data_json=json.dumps(data))

            # Write the output to a new HTML file
            with open(output_path, "w") as f:
                f.write(rendered_html)

            print(f"html file generated successfully for {filename}")

    _make_index_file()


def _make_index_file():
    # List all HTML files in the directory
    html_files = [f for f in os.listdir(output_dir) if f.endswith(".html")]

    # sort numerically by filename if name.split('_')[0] is a number
    # take into account 199 is smaller than 1000
    # include non-numeric at the end
    # don't include index.html
    html_files = sorted(
        html_files,
        key=lambda x: (
            int(x.split("_")[0]) if x.split("_")[0].isdigit() else float("inf"),
            x,
        ),
    )

    html_files = [os.path.splitext(f)[0] for f in html_files]

    template = env.get_template("index.jinja")

    # Render the template with your data
    rendered_html = template.render(files=html_files)

    # Write the output to a new HTML file
    with open(f"{output_dir}/index.html", "w") as f:
        f.write(rendered_html)

    print(f"html file generated successfully for index.html")


json_to_diag()
