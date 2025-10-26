import ast
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any
from .utils import iter_files

@dataclass
class Symbol:
    name: str
    kind: str
    lineno: int
    doc: str | None = None

@dataclass
class FileInfo:
    path: str
    module: str
    imports: List[str]
    symbols: List[Symbol]
    doc: str | None = None

def parse_py(path: Path) -> FileInfo:
    src = path.read_text(encoding="utf-8", errors="ignore")
    tree = ast.parse(src, filename=str(path))
    imports, symbols = [], []
    doc = ast.get_docstring(tree)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports += [n.name for n in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.module: imports.append(node.module)
        elif isinstance(node, ast.ClassDef):
            symbols.append(Symbol(node.name, "class", getattr(node,"lineno",0), ast.get_docstring(node)))
        elif isinstance(node, ast.FunctionDef):
            symbols.append(Symbol(node.name, "function", getattr(node,"lineno",0), ast.get_docstring(node)))
    imports = sorted(set(i for i in imports if i))

    return FileInfo(str(path), path.as_posix(), imports, symbols, doc)

def scan_repo(root: str) -> Dict[str, Any]:
    files = []

    for p in iter_files(root):
        try:
            files.append(parse_py(p))
        except SyntaxError:
            continue
    return {
        "root": str(Path(root).resolve()),
        "files": [{
            "path": f.path,
            "module": f.module,
            "imports": f.imports,
            "symbols": [asdict(s) for s in f.symbols],
            "doc": f.doc,
        } for f in files]
    }
