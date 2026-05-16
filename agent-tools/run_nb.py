"""Execute a notebook in-place via nbclient (no kernel install needed beyond ipykernel).
Usage: python agent-tools/run_nb.py <notebook.ipynb>"""
import sys, json
from pathlib import Path
import nbformat
from nbclient import NotebookClient

nb_path = Path(sys.argv[1])
print(f'Executing {nb_path}...')

nb = nbformat.read(str(nb_path), as_version=4)
client = NotebookClient(nb, timeout=600, kernel_name='python3', resources={'metadata': {'path': str(nb_path.parent)}})
try:
    client.execute()
except Exception as e:
    print(f'Notebook execution FAILED: {e}')
    nbformat.write(nb, str(nb_path))
    sys.exit(1)

nbformat.write(nb, str(nb_path))
print(f'Notebook executed and saved successfully.')
