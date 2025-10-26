import networkx as nx


def build_graph(scan):
    G = nx.DiGraph()
    for f in scan["files"]:
        mod = f["module"]
        G.add_node(mod, type="module", path=f["path"])
        for imp in f["imports"]:
            G.add_edge(mod, imp, type="imports")
        for s in f["symbols"]:
            sym = f'{mod}:{s["kind"]}:{s["name"]}'
            G.add_node(sym, type=s["kind"])
            G.add_edge(mod, sym, type="defines")
    return G


def export_graph_json(G):
    return {
        "nodes": [{"id": n, **G.nodes[n]} for n in G.nodes],
        "edges": [{"source": u, "target": v, **G.edges[u,v]} for u,v in G.edges],
    }
