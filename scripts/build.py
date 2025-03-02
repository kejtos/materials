#!/usr/bin/env python3

import os
import subprocess
import argparse
from typing import List
from pathlib import Path


def export_html_wasm(notebook_path: str, output_dir: str, as_app: bool = False) -> bool:
    """Export a single marimo notebook to HTML format.

    Returns:
        bool: True if export succeeded, False otherwise
    """
    output_path = notebook_path.replace(".py", ".html")

    cmd = ["marimo", "export", "html-wasm"]
    if as_app:
        print(f"Exporting {notebook_path} to {output_path} as app")
        cmd.extend(["--mode", "run", "--no-show-code"])
    else:
        print(f"Exporting {notebook_path} to {output_path} as notebook")
        cmd.extend(["--mode", "edit"])

    try:
        output_file = os.path.join(output_dir, output_path)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        cmd.extend([notebook_path, "-o", output_file])
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error exporting {notebook_path}:")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error exporting {notebook_path}: {e}")
        return False


def generate_index(notebooks: dict[List[str]], output_dir: str) -> None:
    """Generate the index.html file."""
    print("Generating index.html")

    index_path = os.path.join(output_dir, "index.html")
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(index_path, "w") as f:
            f.write(
                """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>marimo</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  </head>
  <body class="font-sans max-w-4xl mx-auto p-8 leading-relaxed">
    <div class="mb-8">
        <p class="text-sm text-gray-600">All the scripts and apps should run in your browser. However, as a result, some of them might take a few seconds to run, especially if you have got a slow PC.</p>
    </div>
    <div class="grid grid-cols-2 gap-4">
      <div class="flex flex-col">
        <h2 class="text-xl font-bold mb-4">4EK214</h2>"""
            )
            for notebook in notebooks['4EK214']:
                notebook_name = notebook.split("/")[-1].replace(".py", "")
                display_name = notebook_name.replace("_", " ").title()
                print(display_name)

                f.write(
                    f'      <div class="p-4 border border-gray-200 rounded-lg max-w-xs justify-self-start">\n'
                    f'        <h3 class="text-lg font-semibold mb-2">{display_name}</h3>\n'
                    f'        <div class="flex gap-2">\n'
                    f'          <a href="{notebook.replace(".py", ".html")}" class="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded">Open</a>\n'
                    f"        </div>\n"
                    f"      </div>\n"
                )
            f.write(
      """</div>
      <div class="flex flex-col">
        <h2 class="text-xl font-bold mb-4">4EK602</h2>"""
            )

            for notebook in notebooks['4EK602']:
                notebook_name = notebook.split("/")[-1].replace(".py", "")
                display_name = notebook_name.replace("_", " ").title()

                f.write(
                    f'      <div class="p-4 border border-gray-200 rounded-lg max-w-xs justify-self-start">\n'
                    f'        <h3 class="text-lg font-semibold mb-2">{display_name}</h3>\n'
                    f'        <div class="flex gap-2">\n'
                    f'          <a href="{notebook.replace(".py", ".html")}" class="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded">Open</a>\n'
                    f"        </div>\n"
                    f"      </div>\n"
                )

            f.write(
        """</div>
    </div>
  </body>
</html>"""
            )

    except IOError as e:
        print(f"Error generating index.html: {e}")


def export_course(course, dir):
    all_notebooks: List[str] = []
    for directory in [f"{course}/notebooks", f"{course}/apps"]:
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"Warning: Directory not found: {dir_path}")
            continue

    for path in dir_path.rglob("*.py"):
        if "helpers" not in path.parts and not path.parts[-1].startswith('_'):
            all_notebooks.append(str(path))

    if not all_notebooks:
        print("No notebooks found!")
        return

    for nb in all_notebooks:
        export_html_wasm(nb, dir, as_app='apps' in nb)

    return all_notebooks


def main() -> None:
    parser = argparse.ArgumentParser(description="Build marimo notebooks")
    parser.add_argument(
        "--output-dir", default="_site", help="Output directory for built files"
    )
    args = parser.parse_args()

    courses = ['4EK214', '4EK602']
    notebooks = {}
    for course in courses:
        notebooks[course] = export_course(course=course, dir=args.output_dir)

    generate_index(notebooks, args.output_dir)


if __name__ == "__main__":
    main()
