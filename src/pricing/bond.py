from dataclasses import dataclass
import numpy as np

@dataclass
class Bond:
    coupon: float
    freq: int
    maturity: float
    face: float = 100.0

def price_bond(bond: Bond, curve, settle_to_next_cf: float = 0.0) -> float:
    times = np.arange(1/bond.freq, bond.maturity + 1e-9, 1/bond.freq)
    cfs = np.full_like(times, bond.coupon * bond.face / bond.freq, dtype=float)
    cfs[-1] += bond.face
    dfs = np.array([curve.df(float(t)) for t in times])
    return float(np.dot(cfs, dfs))

def dv01_bond(bond: Bond, curve, bp: float = 1e-4) -> float:
    bumped_up = curve.__class__(curve.tenors, curve.zeros + bp, curve.compounding, curve.day_count)
    bumped_dn = curve.__class__(curve.tenors, curve.zeros - bp, curve.compounding, curve.day_count)
    p_up = price_bond(bond, bumped_up)
    p_dn = price_bond(bond, bumped_dn)
    return float((p_dn - p_up) / 2.0)
