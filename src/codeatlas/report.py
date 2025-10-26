from pathlib import Path
from .graph import build_graph, export_graph_json
from .summarizer import summarize_scan
from .scanner import scan_repo

import logging
import json

def generate_report(root: str, out_dir: str):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)

    logging.info(f'     Generate report, Repo root={root}, Output dir={out_dir}, out={out}')

    scan = scan_repo(root)
    (out/"scan.json").write_text(json.dumps(scan, indent=2), encoding="utf-8")
    
    G = build_graph(scan)
    (out/"graph.json").write_text(json.dumps(export_graph_json(G), indent=2), encoding="utf-8")

    md = summarize_scan(scan)
    (out/"report.md").write_text(md, encoding="utf-8")

    return {"scan_path": str(out/"scan.json"), "graph_path": str(out/"graph.json"), "report_path": str(out/"report.md")}
