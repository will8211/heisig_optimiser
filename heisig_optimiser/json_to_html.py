import json
import os

import lxml.html as LH
from jinja2 import Environment, FileSystemLoader

input_dir = "out/hierarchies"
output_dir = "d3/html"
env = Environment(loader=FileSystemLoader("d3"))


def json_to_diag():
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(
                output_dir, f"{os.path.splitext(filename)[0]}.html"
            )

            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            template = env.get_template("template.jinja")
            hierarchy = json.dumps(data["hierarchy"])
            order = data["order"]
            rendered_html = template.render(hierarchy=hierarchy, order=order)

            with open(output_path, "w") as f:
                f.write(rendered_html)

            print(f"html file generated successfully for {filename}")

    _make_index_file()


def _make_index_file():
    html_files = [f for f in os.listdir(output_dir) if f.endswith(".html")]

    # sort by the numeric value of the id attribute on the top level html tag
    html_files = sorted(
        html_files,
        key=lambda f: int(
            LH.parse(os.path.join(output_dir, f))
            .getroot()
            .attrib["id"]
            .replace("hierarchy", "")
        ),
    )

    html_files = [os.path.splitext(f)[0] for f in html_files]
    template = env.get_template("index.jinja")
    rendered_html = template.render(files=html_files)

    with open(f"{output_dir}/index.html", "w") as f:
        f.write(rendered_html)

    print(f"html file generated successfully for index.html")


json_to_diag()
