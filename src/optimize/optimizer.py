import numpy as np
import cvxpy as cp
def optimize_portfolio(alphas, dv01s, krds, dv01_target=0.0, krd_bands=0.0, size_caps=None):
    n, K = krds.shape
    w = cp.Variable(n)
    obj = cp.Maximize(alphas @ w)
    cons = [dv01s @ w == dv01_target]
    if krd_bands is not None: cons += [cp.abs(krds.T @ w) <= krd_bands]
    if size_caps is not None: cons += [w <= size_caps, w >= -size_caps]
    prob = cp.Problem(obj, cons); prob.solve(solver=cp.ECOS, verbose=False)
    return np.array(w.value), prob.value
