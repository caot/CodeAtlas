import argparse
from pathlib import Path
from rich.console import Console
from .report import generate_report
from .scanner import scan_repo

import logging

console = Console()

def cmd_scan(args):
    res = generate_report(args.root, args.out)
    console.print(f"[green]Wrote[/] report: {res['report_path']}")
    console.print(f"[green]Wrote[/] graph:  {res['graph_path']}")

def cmd_dump(args):
    data = scan_repo(args.root)
    out = Path(args.out)
    out.write_text(__import__("json").dumps(data, indent=2), encoding="utf-8")
    console.print(f"[green]Wrote[/] {out}")

def cmd_web(args):
    import subprocess, sys, os
    app = Path(__file__).resolve().parents[2] / "webapp" / "app.py"
    env = os.environ.copy(); env["CODEATLAS_ROOT"] = str(Path(args.root).resolve())
    
    logging.info(f'    CODEATLAS_ROOT = {env["CODEATLAS_ROOT"]}')
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app)], env=env, check=True)

def main():
    p = argparse.ArgumentParser("codeatlas")
    sub = p.add_subparsers()

    s1 = sub.add_parser("scan"); s1.add_argument("--root", required=True); s1.add_argument("--out", default="out"); s1.set_defaults(func=cmd_scan)
    s2 = sub.add_parser("dump"); s2.add_argument("--root", required=True); s2.add_argument("--out", default="scan.json"); s2.set_defaults(func=cmd_dump)
    s3 = sub.add_parser("web"); s3.add_argument("--root", required=True); s3.set_defaults(func=cmd_web)

    args = p.parse_args()
    if hasattr(args, "func"): args.func(args)
    else: p.print_help()

if __name__ == "__main__":
    main()
