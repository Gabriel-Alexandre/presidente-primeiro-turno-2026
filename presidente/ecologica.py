"""Regressao ecologica com restricoes (docs/PRE_REGISTRO.md, A4).

y_i = x_i B por municipio, com B >= 0 e cada linha de B somando 1 (todo mundo vai para algum destino).
Minimos quadrados ponderados; solver SLSQP com gradiente analitico. Intervalo por reamostragem de municipios.
E INFERENCIA ECOLOGICA: estima fluxos entre lugares, nao o voto de ninguem.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize


def ajustar(X: np.ndarray, Y: np.ndarray, w: np.ndarray, B0: np.ndarray | None = None) -> np.ndarray:
    n, p = X.shape
    q = Y.shape[1]
    w = w / w.sum()
    if B0 is None:
        B0 = np.tile(np.average(Y, axis=0, weights=w), (p, 1))
    sw = w[:, None]

    def f(v):
        B = v.reshape(p, q)
        R = Y - X @ B
        return float((sw * R * R).sum())

    def g(v):
        B = v.reshape(p, q)
        R = Y - X @ B
        return (-2 * X.T @ (sw * R)).ravel()

    # restricao: cada linha soma 1
    A = np.zeros((p, p * q))
    for o in range(p):
        A[o, o * q:(o + 1) * q] = 1
    cons = [{"type": "eq", "fun": lambda v: A @ v - 1, "jac": lambda v: A}]
    r = minimize(f, B0.ravel(), jac=g, bounds=[(0, 1)] * (p * q), constraints=cons, method="SLSQP", options={"maxiter": 300, "ftol": 1e-12})
    return r.x.reshape(p, q)


def reamostrar(X, Y, w, B0, rep: int, semente: int):
    rng = np.random.default_rng(semente)
    n = len(w)
    out = np.empty((rep,) + B0.shape)
    for k in range(rep):
        idx = rng.integers(0, n, n)
        out[k] = ajustar(X[idx], Y[idx], w[idx], B0)
    return out
