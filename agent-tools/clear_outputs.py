"""Clear all output and execution_count from a notebook.
Usage: python agent-tools/clear_outputs.py <notebook.ipynb>"""
import sys, json
from pathlib import Path

nb_path = Path(sys.argv[1])
nb = json.loads(nb_path.read_text(encoding='utf-8'))
for c in nb['cells']:
    if c.get('cell_type') == 'code':
        c['outputs'] = []
        c['execution_count'] = None
nb_path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
print(f'Cleared outputs in {nb_path}')
