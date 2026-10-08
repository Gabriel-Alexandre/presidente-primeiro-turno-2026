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


FLUXOS = [("jair22", "flavio26"), ("jair22", "lula26"), ("jair22", "abst26"), ("lula22", "lula26"), ("lula22", "flavio26"), ("lula22", "abst26"),
          ("abst22", "flavio26"), ("abst22", "lula26"), ("abst22", "abst26"), ("terceiros22", "flavio26"), ("terceiros22", "lula26"), ("terceiros22", "caiado26"),
          ("terceiros22", "cury26"), ("terceiros22", "renan26"), ("bn22", "flavio26"), ("bn22", "lula26")]
REGIOES = ["Centro-Oeste", "Nordeste", "Norte", "Sudeste", "Sul"]


def estabilidade(t):
    """Marca como robusto o fluxo que passa nos tres criterios (pre-registro, secao 12, emendas 7 e 8):
    (1) amplo e enxuto nacionais diferem em ate 0,03; (2) amplitude entre as cinco regioes de ate 0,15;
    (3) o valor nacional fica dentro do intervalo das regioes (uma media ponderada das regioes nao sai do intervalo delas), folga de 0,01."""
    import numpy as np
    import pandas as pd

    am = t[t.spec == "amplo"].set_index(["ajuste", "origem", "destino"]).B
    en = t[t.spec == "enxuto"].set_index(["ajuste", "origem", "destino"]).B
    linhas = []
    for o, d in FLUXOS:
        b_en = en.get(("nacional", o, d), np.nan)
        b_am = am.get(("nacional", o, d), np.nan)
        reg = [en.get((r, o, d), np.nan) for r in REGIOES]
        lo, hi = np.nanmin(reg), np.nanmax(reg)
        nac = b_en
        linhas.append({"origem": o, "destino": d, "B_amplo": b_am, "B_enxuto": b_en,
                       "dif_amplo_enxuto": abs(b_am - b_en) if not np.isnan(b_am) and not np.isnan(b_en) else np.nan,
                       "min_regioes": lo, "max_regioes": hi, "amplitude_regioes": hi - lo, "nacional_dentro_das_regioes": bool(lo - 0.01 <= nac <= hi + 0.01)})
    est = pd.DataFrame(linhas)
    est["robusto"] = (est.amplitude_regioes <= 0.15) & (est.dif_amplo_enxuto.fillna(0) <= 0.03) & est.nacional_dentro_das_regioes
    return est
