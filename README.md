# CodeAtlas

A lightweight codebase atlas for Python repos. Scans files, builds a dependency graph,
and generates a Markdown report. Includes a small Streamlit UI.

## Quickstart
```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .
codeatlas scan --root ./examples/sample_project --out ./out
codeatlas web --root ./examples/sample_project
```
