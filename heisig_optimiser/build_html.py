import json
import os

import lxml.html as LH
from jinja2 import Environment, FileSystemLoader
from jsmin import jsmin

input_dir = "out/hierarchies"
output_dir = "public/characters"
env = Environment(loader=FileSystemLoader("template"))


def json_to_html():
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

    with open(f"public/index.html", "w") as f:
        f.write(rendered_html)

    print(f"html file generated successfully for index.html")


def add_js():
    # Path to the input JavaScript file
    input_js_file = "template/script.js"

    # Path to the output minified JavaScript file
    output_js_file = "public/script.min.js"

    with open(input_js_file, "r") as js_file:
        minified_js = jsmin(js_file.read())

    with open(output_js_file, "w") as js_file:
        js_file.write(minified_js)

    print(f"Minified JavaScript has been written to {output_js_file}")


def add_font():
    # Path to the input font file
    input_font_file = "fonts/HanaMinB.otf"

    # Path to the output font file
    output_font_file = "public/HanaMinB.otf"

    with open(input_font_file, "rb") as font_file:
        font_data = font_file.read()

    with open(output_font_file, "wb") as font_file:
        font_file.write(font_data)

    print(f"Font file has been written to {output_font_file}")


def add_css():
    # Path to the input font file
    input_font_file = "template/style.css"

    # Path to the output font file
    output_font_file = "public/style.css"

    with open(input_font_file, "rb") as font_file:
        font_data = font_file.read()

    with open(output_font_file, "wb") as font_file:
        font_file.write(font_data)

    print(f"CSS file has been written to {output_font_file}")