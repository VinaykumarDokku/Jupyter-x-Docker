"""Validate Jupyter notebook files without external dependencies."""

import json
import sys
from pathlib import Path


def validate_notebook(path):
    errors = []

    try:
        with path.open(encoding="utf-8") as file:
            notebook = json.load(file)
    except (OSError, ValueError) as error:
        return [f"Cannot read notebook: {error}"]

    if not isinstance(notebook, dict):
        return ["Notebook must be a JSON object"]

    if notebook.get("nbformat") != 4:
        errors.append("Expected notebook format version 4")

    if not isinstance(notebook.get("metadata"), dict):
        errors.append("Missing or invalid metadata")

    cells = notebook.get("cells")

    if not isinstance(cells, list):
        return errors + ["Missing or invalid cells list"]

    for index, cell in enumerate(cells, start=1):
        if not isinstance(cell, dict):
            errors.append(f"Cell {index}: must be an object")
            continue

        cell_type = cell.get("cell_type")

        if cell_type not in ("code", "markdown", "raw"):
            errors.append(f"Cell {index}: invalid cell type")

        source = cell.get("source")

        if not (
            isinstance(source, str)
            or (
                isinstance(source, list)
                and all(isinstance(line, str) for line in source)
            )
        ):
            errors.append(f"Cell {index}: invalid source")

        if cell_type == "code":
            if not isinstance(cell.get("outputs"), list):
                errors.append(f"Cell {index}: missing outputs list")

    return errors


def main():
    notebooks = sorted(Path("root").rglob("*.ipynb"))

    if not notebooks:
        print("No notebooks found in root/")
        return 0

    failures = 0

    for notebook in notebooks:
        errors = validate_notebook(notebook)

        if errors:
            failures += 1
            print(f"FAIL: {notebook}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS: {notebook}")

    print(f"\nChecked {len(notebooks)} notebooks")
    print(f"Failed: {failures}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
