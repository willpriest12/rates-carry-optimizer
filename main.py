from src.curves.zero_curve import ZeroCurve
from src.pricing.bond import Bond, price_bond, dv01_bond
import numpy as np

def demo():
    tenors = np.array([0.5, 1, 2, 3, 5, 7, 10])
    zeros  = np.array([0.045, 0.046, 0.047, 0.048, 0.049, 0.0495, 0.05])
    curve  = ZeroCurve(tenors=tenors, zeros=zeros)
    bond = Bond(coupon=0.05, freq=2, maturity=5.0, face=100.0)
    price = price_bond(bond, curve)
    dv01  = dv01_bond(bond, curve)
    print("Demo OK"); print(f"Price ~ {price:.4f}"); print(f"DV01  ~ {dv01:.6f} $/bp")

if __name__ == "__main__": demo()
