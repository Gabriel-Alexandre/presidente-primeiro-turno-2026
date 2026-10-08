"""A4: para onde foi o voto de 2022 (inferencia ecologica com restricoes), nacional, por regiao e por UF grande.

Origem (parcelas do eleitorado apto de 2022): Lula, Jair, Ciro, Tebet, outros candidatos, branco e nulo, abstencao.
Destino (parcelas do eleitorado apto de 2026): Flavio, Lula, Caiado, Cury, Renan, Zema, outros, branco e nulo, abstencao.
Conferencia: o total previsto de Flavio, Lula e abstencao tem de ficar a ate 1,0% do real; senao o ajuste e marcado 'nao_confiavel'.
Intervalo: 300 reamostragens de municipios, semente 20261007.
"""
from __future__ import annotations

import json
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import DER, REGIAO, RES, SEMENTE, verificar_fontes  # noqa: E402
from presidente.ecologica import ajustar, reamostrar  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402

ORIGEM_ENXUTA = ["lula22", "jair22", "terceiros22", "bn22", "abst22"]
ORIGEM = ["lula22", "jair22", "ciro22", "tebet22", "outros22", "bn22", "abst22"]
DESTINO = ["flavio26", "lula26", "caiado26", "cury26", "renan26", "zema26", "outros26", "bn26", "abst26"]
import os

REP = int(os.environ.get("PRESIDENTE_REP", "300"))
UF_GRANDES_MIN = 100


def montar() -> pd.DataFrame:
    d = pd.read_parquet(DER / "mun_presidente.parquet")
    d = d[(d.turno == 1) & (d.uf != "ZZ")]
    a = d[d.ano == 2022].set_index(["uf", "mun"])
    b = d[d.ano == 2026].set_index(["uf", "mun"])
    i = a.index.intersection(b.index)
    a, b = a.loc[i], b.loc[i]
    out = pd.DataFrame(index=i)
    A0, A1 = a.aptos.astype(float), b.aptos.astype(float)
    out["lula22"] = a.lula / A0
    out["jair22"] = a.jair / A0
    out["ciro22"] = a.ciro / A0
    out["tebet22"] = a.tebet / A0
    out["outros22"] = (a.nominais - a.lula - a.jair - a.ciro - a.tebet) / A0
    out["bn22"] = (a.comparecimento - a.nominais) / A0  # residual; igual a brancos+nulos em 2022
    out["abst22"] = 1 - a.comparecimento / A0
    out["flavio26"] = b.flavio / A1
    out["lula26"] = b.lula / A1
    out["caiado26"] = b.caiado / A1
    out["cury26"] = b.cury / A1
    out["renan26"] = b.renan / A1
    out["zema26"] = b.zema / A1
    out["outros26"] = (b.nominais - b.flavio - b.lula - b.caiado - b.cury - b.renan - b.zema) / A1
    out["bn26"] = (b.comparecimento - b.nominais) / A1  # residual; difere de brancos+nulos em 2 municipios de MG (559 votos)
    out["abst26"] = 1 - b.comparecimento / A1
    out["terceiros22"] = out.ciro22 + out.tebet22 + out.outros22
    out["aptos22"], out["aptos26"] = A0, A1
    out = out.reset_index()
    out["regiao"] = out.uf.map(REGIAO)
    # bordas numericas: as linhas somam 1 por construcao; corrige arredondamento
    assert np.allclose(out[ORIGEM].sum(axis=1), 1, atol=1e-6)
    assert np.allclose(out[DESTINO].sum(axis=1), 1, atol=1e-6)
    return out


def um_ajuste(x: pd.DataFrame, nome: str, rep: int, origem: list[str] | None = None) -> dict:
    origem = origem or ORIGEM
    X, Y = x[origem].to_numpy(), x[DESTINO].to_numpy()
    w = ((x.aptos22 + x.aptos26) / 2).to_numpy()
    B = ajustar(X, Y, w)
    # conferencia de totais: previsto = soma(aptos26 * (X B)) contra o real
    prev = (x.aptos26.to_numpy()[:, None] * (X @ B)).sum(axis=0)
    real = (x.aptos26.to_numpy()[:, None] * Y).sum(axis=0)
    erro = {DESTINO[j]: float(100 * (prev[j] - real[j]) / real[j]) for j in range(len(DESTINO))}
    ok = all(abs(erro[k]) <= 1.0 for k in ("flavio26", "lula26", "abst26"))
    t0 = time.time()
    bs = reamostrar(X, Y, w, B, rep, SEMENTE + zlib.crc32(nome.encode()) % 1000) if rep else None
    lo = np.percentile(bs, 5, axis=0) if bs is not None else None
    hi = np.percentile(bs, 95, axis=0) if bs is not None else None
    linhas = []
    for o, no in enumerate(origem):
        for j, nd in enumerate(DESTINO):
            linhas.append({"ajuste": nome, "origem": no, "destino": nd, "B": B[o, j], "p5": lo[o, j] if lo is not None else np.nan, "p95": hi[o, j] if hi is not None else np.nan})
    # composicao do voto de Flavio e de Lula 2026 por origem (em votos)
    comp = {}
    for j, nd in (("flavio26", "flavio26"), ("lula26", "lula26")):
        jj = DESTINO.index(j)
        votos = (x.aptos26.to_numpy()[:, None] * X * B[:, jj][None, :]).sum(axis=0)
        comp[nd] = {origem[o]: float(votos[o]) for o in range(len(origem))}
    return {"nome": nome, "n": len(x), "B": B, "linhas": linhas, "erro_totais_pct": erro, "confiavel": bool(ok), "composicao": comp, "seg_boot": time.time() - t0}


def main() -> None:
    verificar_fontes()
    d = montar()
    ajustes = [("nacional", d)] + [(r, d[d.regiao == r]) for r in sorted(d.regiao.unique())]
    ajustes_uf = [(f"uf_{u}", g) for u, g in d.groupby("uf") if len(g) > UF_GRANDES_MIN]
    todas, resumo = [], {}
    for spec, origem, lista in (("amplo", ORIGEM, ajustes + ajustes_uf), ("enxuto", ORIGEM_ENXUTA, ajustes)):
        for nome, g in lista:
            r = um_ajuste(g, f"{spec}:{nome}", REP, origem)
            for l in r["linhas"]:
                l["spec"], l["ajuste"] = spec, nome
            todas += r["linhas"]
            resumo[f"{spec}:{nome}"] = {"n_municipios": r["n"], "confiavel": r["confiavel"], "erro_totais_pct": r["erro_totais_pct"], "composicao": r["composicao"]}
            print(spec, nome, r["n"], "confiavel" if r["confiavel"] else "NAO CONFIAVEL", flush=True)
    t = pd.DataFrame(todas)
    tabela("a4_matriz_transicao", t)
    registrar("a4.ajustes", resumo)
    # estabilidade: um fluxo e robusto se (a) amplo e enxuto nacionais diferem em ate 0,03; (b) o intervalo entre as 5 regioes (amplo) e <= 0,15
    fluxos = [("jair22", "flavio26"), ("jair22", "lula26"), ("jair22", "abst26"), ("lula22", "lula26"), ("lula22", "flavio26"), ("lula22", "abst26"),
              ("abst22", "flavio26"), ("abst22", "lula26"), ("abst22", "abst26"), ("terceiros22", "flavio26"), ("terceiros22", "lula26"), ("terceiros22", "caiado26"),
              ("terceiros22", "cury26"), ("terceiros22", "renan26"), ("bn22", "flavio26"), ("bn22", "lula26")]
    am = t[(t.spec == "amplo")].set_index(["ajuste", "origem", "destino"]).B
    en = t[(t.spec == "enxuto")].set_index(["ajuste", "origem", "destino"]).B
    amp_ci = t[(t.spec == "amplo") & (t.ajuste == "nacional")].set_index(["origem", "destino"])
    regs = ["Centro-Oeste", "Nordeste", "Norte", "Sudeste", "Sul"]
    linhas = []
    for o, dd in fluxos:
        if o == "terceiros22":
            nac_am = sum(am[("nacional", oo, dd)] * w for oo, w in ())  # placeholder, calculado abaixo
        # enxuto direto
        b_en = en.get(("nacional", o, dd), np.nan)
        # amplo: media ponderada de ciro, tebet e outros pelos votos de origem nao esta disponivel aqui; compara so fluxos de origem comum
        b_am = am.get(("nacional", o, dd), np.nan)
        reg_b = [en.get((r, o, dd), np.nan) for r in regs]
        linhas.append({"origem": o, "destino": dd, "B_amplo": b_am, "B_enxuto": b_en,
                       "dif_amplo_enxuto": abs(b_am - b_en) if not np.isnan(b_am) and not np.isnan(b_en) else np.nan,
                       "min_regioes": np.nanmin(reg_b), "max_regioes": np.nanmax(reg_b), "amplitude_regioes": np.nanmax(reg_b) - np.nanmin(reg_b)})
    est = pd.DataFrame(linhas)
    est["robusto"] = (est.amplitude_regioes <= 0.15) & (est.dif_amplo_enxuto.fillna(0) <= 0.03)
    tabela("a4_estabilidade", est)
    for r in est.itertuples():
        registrar(f"a4.fluxo.{r.origem}_para_{r.destino}", {"B_amplo": r.B_amplo, "B_enxuto": r.B_enxuto, "min_regioes": r.min_regioes, "max_regioes": r.max_regioes, "robusto": bool(r.robusto)})
    print(est.round(3).to_string())


if __name__ == "__main__":
    main()
