def naive_summary(file_payload):
    title = file_payload["module"]
    doc = file_payload.get("doc") or ""
    symbols = file_payload.get("symbols", [])
    lines = [f"### {title}",""]

    if doc:
        lines += ["**Module docstring:**", doc.strip(), ""]

    if symbols:
        lines.append("**Symbols:**")

        for s in symbols[:50]:
            nm, kind = s["name"], s["kind"]
            snip = (s.get("doc") or "").strip().splitlines()[:2]
            preview = (" — " + " ".join(snip)) if snip else ""
            lines.append(f"- `{kind}` `{nm}`{preview}")

    if not symbols and not doc:
        lines.append("_No docstrings or symbols detected._")

    return "\n".join(lines)

def summarize_scan(scan):
    parts = [f"# CodeAtlas Report\n\nRoot: `{scan['root']}`\n"]

    for f in sorted(scan["files"], key=lambda x: x["module"]):
        parts.append(naive_summary(f)); parts.append("")

    return "\n".join(parts)
