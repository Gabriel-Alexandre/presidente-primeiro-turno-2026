"""Bloco A: A1 (resultado), A2 (onde esta a virada), A3 (troca de voto ou comparecimento).

Margem = candidato do partido de Bolsonaro menos candidato do PT, em pontos dos validos (nominais).
Virada V = margem de 2026 menos margem do 1o turno de 2022. Unidade: municipio (exterior como uma unidade por UF 'ZZ').
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente import municipios  # noqa: E402
from presidente.comum import DER, REGIAO, RES, verificar_fontes  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402

PL = {2018: "jair", 2022: "jair", 2026: "flavio"}
PT = {2018: "haddad", 2022: "lula", 2026: "lula"}
NOMES = ("jair", "haddad", "lula", "flavio", "ciro", "tebet", "soraya", "felipe", "alckmin", "amoedo", "marina", "caiado", "cury", "renan", "zema", "outros_nom")


def carregar() -> pd.DataFrame:
    d = pd.read_parquet(DER / "mun_presidente.parquet")
    d = d[d.turno == 1].copy()
    d.loc[d.uf == "ZZ", "mun"] = 0  # exterior: uma unidade
    d = d.groupby(["ano", "uf", "mun"], as_index=False).sum(numeric_only=True)
    d["pl"] = [r[PL[int(r["ano"])]] for _, r in d.iterrows()]
    d["pt"] = [r[PT[int(r["ano"])]] for _, r in d.iterrows()]
    m = municipios.carregar()
    d = d.merge(m, on=["uf", "mun"], how="left")
    d["regiao"] = d.regiao.fillna(d.uf.map(REGIAO)).fillna("Exterior")
    d["capital"] = d.capital.fillna(False).astype(bool)
    d["porte"] = d.porte.fillna("sem par IBGE")
    return d


def margem(x: pd.DataFrame) -> float:
    return 100 * (x.pl.sum() - x.pt.sum()) / x.nominais.sum()


def a1(d: pd.DataFrame) -> None:
    linhas = []
    for ano in (2018, 2022, 2026):
        x = d[d.ano == ano]
        v = x.nominais.sum()
        for col in [c for c in x.columns if c in NOMES]:
            linhas.append({"ano": ano, "candidato": col, "votos": int(x[col].sum()), "pct_validos": 100 * x[col].sum() / v})
        linhas.append({"ano": ano, "candidato": "_validos", "votos": int(v), "pct_validos": 100.0})
        linhas.append({"ano": ano, "candidato": "_aptos", "votos": int(x.aptos.sum()), "pct_validos": np.nan})
        linhas.append({"ano": ano, "candidato": "_comparecimento", "votos": int(x.comparecimento.sum()), "pct_validos": np.nan})
        linhas.append({"ano": ano, "candidato": "_abstencao_pct", "votos": 0, "pct_validos": 100 * (1 - x.comparecimento.sum() / x.aptos.sum())})
        registrar(f"a1.margem_{ano}", margem(x))
        registrar(f"a1.pl_pct_{ano}", 100 * x.pl.sum() / v)
        registrar(f"a1.pt_pct_{ano}", 100 * x.pt.sum() / v)
    tabela("a1_nacional", pd.DataFrame(linhas))
    a, b = d[d.ano == 2022], d[d.ano == 2026]
    registrar("a1.virada_2022_2026", margem(b) - margem(a))
    registrar("a1.virada_2018_2022", margem(a) - margem(d[d.ano == 2018]))
    registrar("a1.pl_ganho_pontos", 100 * b.pl.sum() / b.nominais.sum() - 100 * a.pl.sum() / a.nominais.sum())
    registrar("a1.pt_perda_pontos", 100 * a.pt.sum() / a.nominais.sum() - 100 * b.pt.sum() / b.nominais.sum())
    registrar("a1.pl_votos_variacao", int(b.pl.sum() - a.pl.sum()))
    registrar("a1.pt_votos_variacao", int(b.pt.sum() - a.pt.sum()))
    u = []
    for uf, x in d.groupby("uf"):
        row = {"uf": uf}
        for ano in (2018, 2022, 2026):
            y = x[x.ano == ano]
            row[f"margem_{ano}"] = margem(y) if len(y) else np.nan
            row[f"validos_{ano}"] = int(y.nominais.sum())
        row["virada_2022_2026"] = row["margem_2026"] - row["margem_2022"]
        row["virada_2018_2022"] = row["margem_2022"] - row["margem_2018"]
        u.append(row)
    tabela("a1_uf", pd.DataFrame(u).sort_values("virada_2022_2026", ascending=False))


def deslocamento(d: pd.DataFrame, grupo: str) -> pd.DataFrame:
    """V = soma(peso medio * variacao da margem) + soma(margem media * variacao do peso). Exato."""
    a, b = d[d.ano == 2022], d[d.ano == 2026]

    def pm(x):
        g = x.groupby(grupo).agg(pl=("pl", "sum"), pt=("pt", "sum"), v=("nominais", "sum"))
        g["w"] = g.v / g.v.sum()
        g["m"] = 100 * (g.pl - g.pt) / g.v
        return g

    g0, g1 = pm(a), pm(b)
    idx = g0.index.union(g1.index)
    g0, g1 = g0.reindex(idx).fillna(0), g1.reindex(idx).fillna(0)
    wm = (g0.w + g1.w) / 2
    mm = (g0.m + g1.m) / 2
    out = pd.DataFrame({"peso_2022": g0.w, "peso_2026": g1.w, "margem_2022": g0.m, "margem_2026": g1.m})
    out["dentro"] = wm * (g1.m - g0.m)
    out["composicao"] = mm * (g1.w - g0.w)
    out["contribuicao"] = out.dentro + out.composicao
    out["pct_da_virada"] = 100 * out.contribuicao / out.contribuicao.sum()
    return out.reset_index()


def a2(d: pd.DataFrame) -> None:
    v = margem(d[d.ano == 2026]) - margem(d[d.ano == 2022])
    d = d.assign(capital_ou_interior=np.where(d.uf == "ZZ", "Exterior", np.where(d.capital, "Capital", "Interior")))
    for nome, col in [("regiao", "regiao"), ("uf", "uf"), ("capital_interior", "capital_ou_interior"), ("porte", "porte")]:
        t = deslocamento(d, col)
        soma = t.contribuicao.sum()
        assert abs(soma - v) < 1e-9, (nome, soma, v)
        tabela(f"a2_{nome}", t.rename(columns={col: nome}))
        registrar(f"a2.{nome}.soma_contribuicoes", soma)
        registrar(f"a2.{nome}.dentro_total", t.dentro.sum())
        registrar(f"a2.{nome}.composicao_total", t.composicao.sum())
    r = deslocamento(d, "regiao").set_index("regiao")
    registrar("a2.regiao.por_regiao", {k: round(x, 4) for k, x in r.contribuicao.items()})
    registrar("a2.regiao.pct_da_virada", {k: round(x, 2) for k, x in r.pct_da_virada.items()})
    ci = deslocamento(d, "capital_ou_interior").set_index("capital_ou_interior")
    registrar("a2.capital_interior.pct_da_virada", {k: round(x, 2) for k, x in ci.pct_da_virada.items()})
    registrar("a2.virada_total", v)


def a3(d: pd.DataFrame) -> None:
    a = d[d.ano == 2022].set_index(["uf", "mun"])
    b = d[d.ano == 2026].set_index(["uf", "mun"])
    comuns = a.index.intersection(b.index)
    registrar("a3.municipios_em_comum", len(comuns))
    registrar("a3.municipios_so_2022", int(len(a.index.difference(b.index))))
    registrar("a3.municipios_so_2026", int(len(b.index.difference(a.index))))
    a, b = a.loc[comuns], b.loc[comuns]

    def partes(x):
        A = x.aptos.astype(float)
        return A, x.comparecimento / A, x.nominais / x.comparecimento

    A0, r0, q0 = partes(a)
    A1, r1, q1 = partes(b)
    res = {}
    for nome, c0, c1 in (("pl", a.pl, b.pl), ("pt", a.pt, b.pt)):
        s0, s1 = c0 / a.nominais, c1 / b.nominais
        o1 = {"apto": (A1 - A0) * r0 * q0 * s0, "comparecimento": A1 * (r1 - r0) * q0 * s0, "validos": A1 * r1 * (q1 - q0) * s0, "parcela": A1 * r1 * q1 * (s1 - s0)}
        o2 = {"parcela": A0 * r0 * q0 * (s1 - s0), "validos": A0 * r0 * (q1 - q0) * s1, "comparecimento": A0 * (r1 - r0) * q1 * s1, "apto": (A1 - A0) * r1 * q1 * s1}
        tot = (c1 - c0).sum()
        for k in o1:
            res[(nome, k)] = (o1[k].sum(), o2[k].sum())
        assert abs(sum(o1[k].sum() for k in o1) - tot) < 1e-4
        assert abs(sum(o2[k].sum() for k in o2) - tot) < 1e-4
        res[(nome, "total")] = (tot, tot)
    t = pd.DataFrame([{"candidato": k[0], "termo": k[1], "votos_ordem_a": v[0], "votos_ordem_b": v[1]} for k, v in res.items()])
    tabela("a3_decomposicao", t)
    for cand in ("pl", "pt"):
        x = t[t.candidato == cand].set_index("termo")
        tot = x.loc["total", "votos_ordem_a"]
        registrar(f"a3.{cand}.total", tot)
        registrar(f"a3.{cand}.termos_ordem_a", {k: float(v) for k, v in x.votos_ordem_a.items() if k != "total"})
        registrar(f"a3.{cand}.termos_ordem_b", {k: float(v) for k, v in x.votos_ordem_b.items() if k != "total"})
        registrar(f"a3.{cand}.pct_comparecimento", {"a": 100 * x.loc["comparecimento", "votos_ordem_a"] / tot, "b": 100 * x.loc["comparecimento", "votos_ordem_b"] / tot})
        registrar(f"a3.{cand}.pct_parcela", {"a": 100 * x.loc["parcela", "votos_ordem_a"] / tot, "b": 100 * x.loc["parcela", "votos_ordem_b"] / tot})
    cf_pl = (A1 * r0 * q0 * b.pl / b.nominais).sum()
    cf_pt = (A1 * r0 * q0 * b.pt / b.nominais).sum()
    cf_val = (A1 * r0 * q0).sum()
    registrar("a3.margem_2026_com_comparecimento_de_2022", 100 * (cf_pl - cf_pt) / cf_val)
    registrar("a3.margem_2026_sobre_municipios_comuns", 100 * (b.pl.sum() - b.pt.sum()) / b.nominais.sum())


def main() -> None:
    verificar_fontes()
    d = carregar()
    a1(d)
    a2(d)
    a3(d)
    r = json.load(open(RES / "RESUMO.json", encoding="utf-8"))
    for k in ("a1", "a2", "a3"):
        print(k, json.dumps(r[k], ensure_ascii=False)[:1800])


if __name__ == "__main__":
    main()
