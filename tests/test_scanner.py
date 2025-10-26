from codeatlas.scanner import scan_repo
from pathlib import Path

def test_scan():
    root = Path(__file__).resolve().parents[1] / 'examples' / 'sample_project'
    data = scan_repo(str(root))
    assert data['files']
