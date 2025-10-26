from pathlib import Path
def iter_files(root):
    root = Path(root)
    for p in root.rglob("*.py"):
        if any(part.startswith(".") for part in p.parts): 
            continue
        yield p
