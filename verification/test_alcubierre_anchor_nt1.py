"""Phase A.6 acceptance test with Nt=1 (anchor convention).

Runs the pipeline twice: once with wf_compat=True (byte-match the published
WarpFactory anchor in warp_factory_repro/alcubierre_textbook.mat), once with
wf_compat=False (default convergent textbook Ricci formula).

The default formula is the SCIENTIFICALLY CORRECT one — the WF anchor is
computed with a typo'd ricciT.m formula that overestimates |R_munu| by ~2x
at the anchor's coarse dx=0.2 (see agent-tools/diag_ricci_alcubierre_convergence.py).
"""
import sys; sys.path.insert(0, '.')
import time
import numpy as np
from warp_factory_py.metrics.alcubierre import metric_alcubierre
from warp_factory_py.solvers.evaluator import eval_metric

NT, NX, NY, NZ = 1, 80, 80, 5
DX = 0.2
DT = 0.001
m = metric_alcubierre(
    (NT, NX, NY, NZ),
    ((NT+1)/2*DT, (NX+1)/2*DX, (NY+1)/2*DX, (NZ+1)/2*DX),
    v=1.0, R=4.0, sigma=8.0,
    grid_scale=(DT, DX, DX, DX),
)

xc = (np.arange(NX)+1)*DX
x0 = (NX+1)/2*DX
X, Y = np.meshgrid(xc, xc, indexing='ij')
in_xy = (X-x0)**2 + (Y-x0)**2 <= 4.25**2
mask = np.zeros((NT, NX, NY, NZ), bool)
mask[0, 2:-2, 2:-2, NZ//2] = in_xy[2:-2, 2:-2]

ANCHOR_PASS = 0.07365439093484419
ANCHOR_MIN = {'null': -9.593e43, 'weak': -9.593e43,
              'dominant': -4.042e43, 'strong': -5.882e43}

for wf_compat in (True, False):
    label = "wf_compat=True (matches WF anchor)" if wf_compat else "wf_compat=False (convergent textbook)"
    print(f"\n========== {label} ==========")
    t0 = time.time()
    res = eval_metric(m, num_angular=100, num_temporal=10, wf_compat=wf_compat)
    print(f'eval_metric: {time.time()-t0:.1f} s')

    print(f'{"cond":>8} {"pass":>10} {"anchor":>10} {"min(mine)":>15} {"min(anchor)":>15} {"rel(min)":>10}')
    print('-' * 80)
    for name in ['null', 'weak', 'dominant', 'strong']:
        arr = res.ec[name]
        arr_clip = np.minimum(arr, 0.0)
        pf = np.sum(arr_clip[mask] >= -1e-12) / mask.sum()
        mn = arr[mask].min()
        rel = abs(mn - ANCHOR_MIN[name]) / abs(ANCHOR_MIN[name])
        print(f'{name:>8} {pf:>10.4f} {ANCHOR_PASS:>10.4f} {mn:>+15.3e} {ANCHOR_MIN[name]:>+15.3e} {rel:>10.2e}')
