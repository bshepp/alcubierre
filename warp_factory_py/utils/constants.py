"""Physical constants in SI (CODATA 2018, matching WarpFactory defaults)."""

# Speed of light, m/s
c = 299_792_458.0

# Newtonian gravitational constant, m^3 kg^-1 s^-2
G = 6.67430e-11

# 8 pi G / c^4, the Einstein-equation prefactor (T_munu = (c^4 / 8 pi G) G_munu).
EINSTEIN_PREFACTOR = c**4 / (8.0 * 3.141592653589793 * G)
