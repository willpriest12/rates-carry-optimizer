from dataclasses import dataclass
import numpy as np

@dataclass
class ZeroCurve:
    tenors: np.ndarray
    zeros: np.ndarray
    compounding: str = "cont"
    day_count: str = "ACT/365"

    def df(self, t: float) -> float:
        z = self.z(t)
        if self.compounding == "cont": return float(np.exp(-z * t))
        return float(1.0 / (1.0 + z * t))

    def z(self, t: float) -> float:
        return float(np.interp(t, self.tenors, self.zeros))

    def forward(self, t1: float, t2: float) -> float:
        return -np.log(self.df(t2)/self.df(t1)) / (t2 - t1)
