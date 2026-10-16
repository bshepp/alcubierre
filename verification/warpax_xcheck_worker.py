"""Subprocess worker: evaluate warpax's pointwise LMI energy-condition margins
on a batch of Eulerian-frame stress tensors.

Session 58. warpax (Le 2026a, arXiv:2602.18023; MIT) is NOT a project
dependency -- it lives in a scratch venv whose interpreter is passed via the
``WARPAX_PYTHON`` environment variable. The harness
``test_ec_exact_minimiser.py`` writes ``T_eul`` samples to a ``.npy`` file,
runs this worker with that interpreter, and reads the ``.npz`` result.

Usage:  python warpax_xcheck_worker.py <in.npy> <out.npz>
``in.npy``: float64 array (P, 4, 4), covariant T_ab in an orthonormal frame
(eta = diag(-1, 1, 1, 1)). Output arrays: nec, wec, sec, dec (LMI margins,
negative = violation), typeI (bool).
"""
import sys

import numpy as np


def main(inp: str, out: str) -> None:
    import jax
    import jax.numpy as jnp
    from warpax.energy_conditions import certify_point_lmi, classify_hawking_ellis

    jax.config.update("jax_enable_x64", True)
    T = np.load(inp)
    eta = jnp.asarray(np.diag([-1.0, 1.0, 1.0, 1.0]))
    nec = np.empty(len(T)); wec = np.empty(len(T)); sec = np.empty(len(T)); dec = np.empty(len(T))
    typeI = np.zeros(len(T), dtype=bool)
    for k, Tk in enumerate(T):
        Tj = jnp.asarray(Tk)
        r = certify_point_lmi(Tj, eta)
        nec[k] = float(r["nec"]); wec[k] = float(r["wec"]); sec[k] = float(r["sec"]); dec[k] = float(r["dec"])
        Tm = jnp.asarray(np.diag([-1.0, 1.0, 1.0, 1.0]) @ Tk)
        c = classify_hawking_ellis(Tm, eta)
        t = getattr(c, "type", None)
        if t is None:
            t = getattr(c, "he_type", None)
        try:
            typeI[k] = int(np.asarray(t)) == 1
        except Exception:
            typeI[k] = str(t).strip().upper() in ("I", "1", "TYPE_I", "TYPEI")
    np.savez(out, nec=nec, wec=wec, sec=sec, dec=dec, typeI=typeI)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
