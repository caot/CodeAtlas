from pathlib import Path
from hydralit_components.Loaders import HyLoader
from codeatlas.report import generate_report

import os, json
import logging
import streamlit as st

st.set_page_config(page_title="CodeAtlas", layout="wide")

st.title('''CodeAtlas

A lightweight codebase atlas for Python repos. Scans files, builds a dependency graph,
and generates a Markdown report. Includes a small Streamlit UI.
''')

root = st.text_input("Repo root", value=os.environ.get("CODEATLAS_ROOT", ""))
out_dir = st.text_input("Output dir", value="out")

logging.info({'    Repo root': root, 'Output dir': out_dir})

# Initialize a session state variable to control the warning's visibility
if 'show_warning' not in st.session_state:
    st.session_state.show_warning = True


# Define a function to hide the warning
def hide_warning():
    st.session_state.show_warning = False


if st.button("Scan", on_click=hide_warning):
    logging.info('    A ...')
    if not root:
        logging.info('    B ...')
        st.error("Provide a repo root")
    else:
        logging.info('    C ...')
        logging.info(f'    ... Scan {out_dir}')

        # with HyLoader("Scanning ...", loader_name="bar", index=1):  # Example using a bar loader
        with st.spinner("Scanning ...", show_time=True):
            res = generate_report(root, out_dir)

        st.success("Scan complete")
        st.code(json.dumps(res, indent=2))

        logging.info('    ... Scan complete!')
else:
    # Display the warning conditionally
    if st.session_state.show_warning:
        st.warning("Scan button not clicked yet.!", icon="⚠️")

if out_dir and Path(out_dir, "report.md").exists():
    logging.info('    D ...')
    st.markdown(Path(out_dir, "report.md").read_text(encoding="utf-8"))
