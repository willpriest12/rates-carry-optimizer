from src.pricing.bond import Bond, price_bond
def expected_carry_roll(bond, curve, repo_rate: float, horizon_years: float) -> float:
    price_now = price_bond(bond, curve)
    aged = Bond(coupon=bond.coupon, freq=bond.freq, maturity=max(1e-6, bond.maturity - horizon_years), face=bond.face)
    price_aged = price_bond(aged, curve)
    roll = price_aged - price_now
    accrual = bond.coupon * bond.face * horizon_years
    funding = - repo_rate * horizon_years * price_now
    return float(accrual + roll + funding)
