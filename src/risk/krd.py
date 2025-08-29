import numpy as np
from src.pricing.bond import price_bond

def krd_vector(bond, curve, key_tenors=(2,3,5,7,10,20,30), bp=1e-4):
    base_price = price_bond(bond, curve)
    krds = []
    for T in key_tenors:
        bumped_zeros = curve.zeros.copy()
        sigma = 1.0
        kernel = np.exp(-0.5 * ((curve.tenors - T)/sigma)**2)
        kernel /= kernel.max()
        bumped_zeros = bumped_zeros + bp * kernel
        bumped_curve = curve.__class__(curve.tenors, bumped_zeros, curve.compounding, curve.day_count)
        p_bump = price_bond(bond, bumped_curve)
        krds.append((base_price - p_bump))
    return np.array(krds)
