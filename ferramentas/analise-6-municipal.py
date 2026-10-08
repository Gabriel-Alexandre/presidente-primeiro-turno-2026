"""Hipoteses por lugar: H1 (heranca), H3 (economia), H7 (maquina local, descontinuidade), H8 (religiao), H9 (governadores aliados), H13 (renovacao).

Variavel de resultado: virada municipal V = margem(Flavio - Lula, 2026) - margem(Jair - Lula, 2022), em pontos dos validos.
Placebo: V0 = margem(Jair - Lula, 2022) - margem(Jair - Haddad, 2018). Pesos: validos de 2026. Erro padrao agrupado por UF.
Coeficientes por 1 desvio-padrao do preditor. LUGAR NAO E PESSOA: toda relacao e entre municipios.
Criterio de 'mesmo sinal e tamanho' no placebo (esclarecimento da regra do pre-registro, secao 7): mesmo sinal e modulo de pelo menos 50% do efeito.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import APURACAO, BRUTOS, DER, RES, SEMENTE, verificar_fontes  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402

UF_COD = {"ac": 12, "al": 27, "am": 13, "ap": 16, "ba": 29, "ce": 23, "df": 53, "es": 32, "go": 52, "ma": 21, "mg": 31, "ms": 50, "mt": 51, "pa": 15, "pb": 25,
          "pe": 26, "pi": 22, "pr": 41, "rj": 33, "rn": 24, "ro": 11, "rr": 14, "rs": 43, "sc": 42, "se": 28, "sp": 35, "to": 17}
COD_UF = {v: k.upper() for k, v in UF_COD.items()}


def base() -> pd.DataFrame:
    d = pd.read_parquet(DER / "mun_presidente.parquet")
    d = d[(d.turno == 1) & (d.uf != "ZZ")]
    a18, a22, a26 = (d[d.ano == y].set_index(["uf", "mun"]) for y in (2018, 2022, 2026))
    i = a22.index.intersection(a26.index).intersection(a18.index)
    a18, a22, a26 = a18.loc[i], a22.loc[i], a26.loc[i]
    m = pd.DataFrame(index=i)
    m["v26"], m["v22"], m["v18"] = a26.nominais, a22.nominais, a18.nominais
    m["m26"] = 100 * (a26.flavio - a26.lula) / a26.nominais
    m["m22"] = 100 * (a22.jair - a22.lula) / a22.nominais
    m["m18"] = 100 * (a18.jair - a18.haddad) / a18.nominais
    m["V"], m["V0"] = m.m26 - m.m22, m.m22 - m.m18
    m["jair18"], m["jair22"], m["flavio26"] = 100 * a18.jair / a18.nominais, 100 * a22.jair / a22.nominais, 100 * a26.flavio / a26.nominais
    m["haddad18"], m["lula22"], m["lula26"] = 100 * a18.haddad / a18.nominais, 100 * a22.lula / a22.nominais, 100 * a26.lula / a26.nominais
    m["aptos22"], m["aptos26"] = a22.aptos, a26.aptos
    m = m.reset_index()
    cov = pd.read_parquet(Path(__file__).resolve().parent.parent.parent / "congresso-e-governos-eleicoes-2026" / "dados" / "derivados" / "municipios.parquet")
    cov["mun"] = cov["mun"].astype(int)
    m = m.merge(cov[["uf", "mun", "pop", "pct_urbana", "pct_pretos_pardos", "pct_60mais", "pct_superior", "pct_evangelicos", "pct_catolicos", "log_pib_pc", "bf_por_100hab"]], on=["uf", "mun"], how="left")
    pf = pd.read_parquet(DER / "perfil_eleitorado.parquet")
    pf["jov"] = pf.p_i16_17.fillna(0) + pf.p_i18_24.fillna(0)
    q = pf.pivot_table(index=["uf", "mun"], columns="ano", values=["jov", "p_i60_mais", "p_e_superior", "p_feminino"])
    q.columns = [f"{a}_{b}" for a, b in q.columns]
    q = q.reset_index()
    for c in ("jov", "p_i60_mais", "p_e_superior", "p_feminino"):
        q[f"d_{c}"] = 100 * (q[f"{c}_2026"] - q[f"{c}_2022"])
    m = m.merge(q[["uf", "mun", "d_jov", "d_p_i60_mais", "d_p_e_superior", "d_p_feminino"]], on=["uf", "mun"], how="left")
    return m


def z(s: pd.Series) -> pd.Series:
    return (s - s.mean()) / s.std()


def ajustar(df: pd.DataFrame, y: str, xs: list[str], fe: bool = True, pesos: bool = True):
    df = df.dropna(subset=[y] + xs).copy()
    X = df[xs].copy()
    if fe:
        X = pd.concat([X, pd.get_dummies(df.uf, drop_first=True, dtype=float)], axis=1)
    X = sm.add_constant(X)
    w = df.v26 if pesos else np.ones(len(df))
    g = pd.Categorical(df.uf).codes
    return sm.WLS(df[y], X, weights=w).fit(cov_type="cluster", cov_kwds={"groups": g})


def linha(f, nome: str) -> dict:
    return {"coef": float(f.params[nome]), "se": float(f.bse[nome]), "p": float(f.pvalues[nome]), "n": int(f.nobs)}


def spec(df: pd.DataFrame, xs: list[str], foco: str, ufs_fora: list[str]) -> dict:
    out = {}
    out["principal"] = linha(ajustar(df, "V", xs), foco)
    out["placebo_2018_2022"] = linha(ajustar(df, "V0", xs), foco)
    out["sem_5_maiores_ufs"] = linha(ajustar(df[~df.uf.isin(ufs_fora)], "V", xs), foco)
    out["sem_efeito_fixo_de_uf"] = linha(ajustar(df, "V", xs, fe=False), foco)
    out["sem_pesos"] = linha(ajustar(df, "V", xs, pesos=False), foco)
    pr, pl = out["principal"]["coef"], out["placebo_2018_2022"]["coef"]
    out["placebo_parecido"] = bool(np.sign(pr) == np.sign(pl) and abs(pl) >= 0.5 * abs(pr))
    out["sinal_mantido_nas_sensibilidades"] = bool(all(np.sign(out[k]["coef"]) == np.sign(pr) for k in ("sem_5_maiores_ufs", "sem_efeito_fixo_de_uf", "sem_pesos")))
    return out


def corr_w(a: pd.Series, b: pd.Series, w: pd.Series) -> float:
    ma, mb = np.average(a, weights=w), np.average(b, weights=w)
    cov = np.average((a - ma) * (b - mb), weights=w)
    return float(cov / np.sqrt(np.average((a - ma) ** 2, weights=w) * np.average((b - mb) ** 2, weights=w)))


def h1(m: pd.DataFrame) -> None:
    w = m.v26
    r = {"jair22_flavio26": corr_w(m.jair22, m.flavio26, w), "jair18_jair22": corr_w(m.jair18, m.jair22, w), "lula22_lula26": corr_w(m.lula22, m.lula26, w), "haddad18_lula22": corr_w(m.haddad18, m.lula22, w),
         "V_com_jair22": corr_w(m.V, m.jair22, w), "V_com_lula22": corr_w(m.V, m.lula22, w)}
    registrar("h1.correlacoes_municipais_ponderadas", r)
    # inclinacao: quanto do voto de Jair em 2022 'passa' para Flavio por ponto, com efeito fixo de UF
    m = m.assign(j=m.jair22)
    f = ajustar(m, "flavio26", ["j"])
    registrar("h1.inclinacao_flavio26_sobre_jair22", linha(f, "j"))
    # onde a virada foi maior: por faixa de voto de Jair em 2022
    m["faixa"] = pd.cut(m.jair22, [0, 25, 35, 45, 55, 65, 100]).astype(str)
    t = m.groupby("faixa").apply(lambda g: pd.Series({"municipios": len(g), "validos_2026": g.v26.sum(), "V_medio": np.average(g.V, weights=g.v26), "jair22": np.average(g.jair22, weights=g.v26), "flavio26": np.average(g.flavio26, weights=g.v26)}), include_groups=False).reset_index()
    tabela("h1_virada_por_faixa_de_jair22", t)


def h8_h13(m: pd.DataFrame, ufs_fora: list[str]) -> dict:
    m = m.copy()
    for c in ("pct_evangelicos", "pct_urbana", "pct_superior", "pct_pretos_pardos", "log_pib_pc", "d_jov", "d_p_i60_mais", "d_p_e_superior"):
        m["z_" + c] = z(m[c])
    r8 = spec(m, ["z_pct_evangelicos", "z_pct_urbana", "z_pct_superior", "z_pct_pretos_pardos", "z_log_pib_pc"], "z_pct_evangelicos", ufs_fora)
    registrar("h8.evangelicos_por_dp", r8)
    registrar("h8.dp_pct_evangelicos_pontos", float(m.pct_evangelicos.std()))
    out = {"H8_evangelicos": r8}
    for nome, c in (("jovens_16_a_24", "z_d_jov"), ("60_mais", "z_d_p_i60_mais"), ("superior", "z_d_p_e_superior")):
        r = spec(m, ["z_d_jov", "z_d_p_i60_mais", "z_d_p_e_superior", "z_pct_urbana"], c, ufs_fora)
        registrar(f"h13.{nome}_por_dp", r)
        out[f"H13_{nome}"] = r
    registrar("h13.dp_variacao_pontos", {"jov": float(m.d_jov.std()), "60_mais": float(m.d_p_i60_mais.std()), "superior": float(m.d_p_e_superior.std())})
    ponder = lambda s: float(np.average(s.dropna(), weights=m.loc[s.dropna().index, "v26"]))
    registrar("h13.variacao_media_ponderada_pontos", {"jov": ponder(m.d_jov), "60_mais": ponder(m.d_p_i60_mais), "superior": ponder(m.d_p_e_superior)})
    return out


def rd(df: pd.DataFrame, y: str, run: str, h: float):
    s = df[df[run].abs() <= h].dropna(subset=[y, run]).copy()
    k = 1 - s[run].abs() / h
    T = (s[run] >= 0).astype(float)
    X = sm.add_constant(pd.DataFrame({"T": T, "r": s[run], "Tr": T * s[run]}))
    f = sm.WLS(s[y], X, weights=k).fit(cov_type="cluster", cov_kwds={"groups": pd.Categorical(s.uf).codes})
    return {"efeito": float(f.params["T"]), "se": float(f.bse["T"]), "p": float(f.pvalues["T"]), "n": int(len(s)), "n_esq": int((T == 0).sum()), "n_dir": int((T == 1).sum())}


def h7(m: pd.DataFrame) -> dict:
    pr = pd.read_parquet(DER / "prefeitos_2024.parquet")
    d = m.merge(pr[["uf", "mun", "elegivel", "corrida", "elegivel_pl", "corrida_pl", "validos"]], on=["uf", "mun"], how="inner")
    out = {}
    for var, run, rot in (("direita_vs_nao_direita", "corrida", "elegivel"), ("so_PL", "corrida_pl", "elegivel_pl")):
        x = d[d[rot]].copy()
        for h in (5, 3, 10):
            out[f"{var}_h{h}"] = {"V": rd(x, "V", run, h), "placebo_V0": rd(x, "V0", run, h)}
        j = x[x[run].abs() <= 5]
        out[f"{var}_densidade_h5"] = {"abaixo": int((j[run] < 0).sum()), "acima": int((j[run] >= 0).sum())}
        a, b = out[f"{var}_densidade_h5"]["abaixo"], out[f"{var}_densidade_h5"]["acima"]
        from scipy.stats import binomtest
        out[f"{var}_densidade_h5"]["p_binomial"] = float(binomtest(b, a + b, 0.5).pvalue) if a + b else None
        out[f"{var}_balanco_covariaveis_h5"] = {c: rd(x, c, run, 5) for c in ("pct_evangelicos", "pct_urbana", "log_pib_pc")}
    registrar("h7.resultados", out)
    registrar("h7.poder_ok_direita_h5", bool(out["direita_vs_nao_direita_h5"]["V"]["n"] >= 200))
    return out


def uf_nivel(m: pd.DataFrame) -> pd.DataFrame:
    g = m.groupby("uf").apply(lambda x: pd.Series({
        "v26": x.v26.sum(), "m26": 100 * (np.average(x.flavio26, weights=x.v26) - np.average(x.lula26, weights=x.v26)) / 100 * 1.0, "V": np.average(x.V, weights=x.v26), "V0": np.average(x.V0, weights=x.v26),
    }), include_groups=False).reset_index()
    return g


def h9(m: pd.DataFrame) -> dict:
    ap = pd.read_csv(APURACAO / "dados" / "apoios.csv", dtype=str)
    u = uf_nivel(m)
    out = {}
    rng = np.random.default_rng(SEMENTE)
    for ano, col, a_flavio, a_lula in ((2026, "V", "Flavio", "Lula"), (2022, "V0", "Bolsonaro", "Lula")):
        x = ap[ap.ano == str(ano)][["uf", "apoio"]].merge(u, on="uf")
        x["grupo"] = x.apoio.map({a_flavio: "bolsonarista", a_lula: "lula"}).fillna("outro")
        g = x[x.grupo.isin(["bolsonarista", "lula"])]
        if g.grupo.nunique() < 2:
            continue
        dif = np.average(g[g.grupo == "bolsonarista"][col], weights=g[g.grupo == "bolsonarista"].v26) - np.average(g[g.grupo == "lula"][col], weights=g[g.grupo == "lula"].v26)
        perm = []
        vals, pes, lab = g[col].to_numpy(), g.v26.to_numpy(), (g.grupo == "bolsonarista").to_numpy()
        for _ in range(10000):
            l = rng.permutation(lab)
            perm.append(np.average(vals[l], weights=pes[l]) - np.average(vals[~l], weights=pes[~l]))
        p = float((np.abs(perm) >= abs(dif)).mean())
        out[str(ano)] = {"ufs_bolsonaristas": g[g.grupo == "bolsonarista"].uf.tolist(), "ufs_lula": g[g.grupo == "lula"].uf.tolist(),
                         "virada_media_bolsonaristas": float(np.average(g[g.grupo == "bolsonarista"][col], weights=g[g.grupo == "bolsonarista"].v26)),
                         "virada_media_lula": float(np.average(g[g.grupo == "lula"][col], weights=g[g.grupo == "lula"].v26)),
                         "diferenca": float(dif), "p_permutacao": p, "n_ufs": int(len(g)),
                         "medida": "virada 2022 para 2026 (2026)" if ano == 2026 else "virada 2018 para 2022 (placebo, apoio de 2022)"}
    registrar("h9.resultados", out)
    return out


def sidra(arq: str) -> pd.DataFrame:
    j = json.load(open(BRUTOS / "economia" / arq, encoding="utf-8"))
    d = pd.DataFrame(j[1:])
    d["valor"] = pd.to_numeric(d.V, errors="coerce")
    return d


def h3(m: pd.DataFrame) -> dict:
    u = uf_nivel(m)
    de = sidra("desocupacao_uf.json")
    re_ = sidra("rendimento_uf.json")
    def delta(d, col):
        t = d.pivot_table(index="D1C", columns="D3C", values="valor", aggfunc="first")
        t["uf"] = [COD_UF.get(int(i)) for i in t.index]
        return t.set_index("uf")
    a, b = delta(de, "d"), delta(re_, "r")
    x = pd.DataFrame({"d_desocup": a["202602"] - a["202202"], "d_renda_pct": 100 * (b["202602"] / b["202202"] - 1)}).reset_index().merge(u, on="uf")
    X = sm.add_constant(x[["d_desocup", "d_renda_pct"]])
    f = sm.WLS(x.V, X, weights=x.v26).fit(cov_type="HC3")
    out = {"n_ufs": int(len(x)), "d_desocupacao_pontos": linha(f, "d_desocup"), "d_renda_real_pct": linha(f, "d_renda_pct"), "r2": float(f.rsquared)}
    f0 = sm.WLS(x.V0, X, weights=x.v26).fit(cov_type="HC3")
    out["placebo_2018_2022"] = {"d_desocupacao_pontos": linha(f0, "d_desocup"), "d_renda_real_pct": linha(f0, "d_renda_pct")}
    registrar("h3.por_uf", out)
    tabela("h3_uf", x)
    # descritivo nacional (nao e teste)
    ipca = sidra("ipca_12m_geral_e_alimentos.json")
    reg = {}
    for cod, nome in (("7169", "geral"), ("7170", "alimentacao_e_bebidas")):
        s = ipca[ipca.D4C == cod].set_index("D3C").valor
        reg[nome] = {"set2022": float(s.get("202209", np.nan)), "set2026": float(s.get("202609", np.nan)) if "202609" in s.index else float(s.iloc[-1]), "max_no_periodo": float(s.max()), "mes_do_max": str(s.idxmax())}
    de_br = sidra("desocupacao_brasil.json")
    tr = de_br.set_index("D3C").valor
    tr = tr[tr.index >= "202201"]
    reg["desocupacao_trimestral"] = {"t2_2022": float(tr["202202"]), "t2_2026": float(tr["202602"]), "min_desde_2022": float(tr.min()), "trimestre_do_min": str(tr.idxmin())}
    re_br = sidra("rendimento_brasil.json").set_index("D3C").valor
    reg["rendimento_real_reais"] = {"t2_2022": float(re_br["202202"]), "t2_2026": float(re_br["202602"]), "variacao_pct": float(100 * (re_br["202602"] / re_br["202202"] - 1))}
    selic = pd.DataFrame(json.load(open(BRUTOS / "economia" / "selic_meta.json", encoding="utf-8")))
    selic["valor"] = pd.to_numeric(selic.valor, errors="coerce")
    selic["data"] = pd.to_datetime(selic.data, format="%d/%m/%Y")
    reg["selic_meta"] = {"out2022": float(selic[selic.data <= "2022-10-02"].valor.iloc[-1]), "set2026": float(selic[selic.data <= "2026-09-30"].valor.iloc[-1]), "max": float(selic.valor.max())}
    registrar("h3.nacional_descritivo", reg)
    return out


def h6_municipal(m: pd.DataFrame, ufs_fora: list[str]) -> dict:
    """B3c: onde os 'outros' (nem PT nem partido de Bolsonaro) cairam mais, quanto o candidato do PL e Lula ganharam. Identidade: dFlavio + dLula + dOutros = 0."""
    d = m.copy()
    d["d_outros"] = (100 - d.flavio26 - d.lula26) - (100 - d.jair22 - d.lula22)
    d["d_flavio"] = d.flavio26 - d.jair22
    d["d_lula"] = d.lula26 - d.lula22
    fl = ajustar(d, "d_flavio", ["d_outros"])
    lu = ajustar(d, "d_lula", ["d_outros"])
    out = {"d_outros_medio_ponderado": float(np.average(d.d_outros, weights=d.v26)), "d_flavio_medio_ponderado": float(np.average(d.d_flavio, weights=d.v26)), "d_lula_medio_ponderado": float(np.average(d.d_lula, weights=d.v26)),
           "flavio_sobre_d_outros": linha(fl, "d_outros"), "lula_sobre_d_outros": linha(lu, "d_outros"),
           "flavio_sobre_d_outros_sem_5_maiores": linha(ajustar(d[~d.uf.isin(ufs_fora)], "d_flavio", ["d_outros"]), "d_outros")}
    registrar("h6.municipal", out)
    return out


def bh(pvals: dict[str, float], alfa: float = 0.05) -> dict:
    nomes = sorted(pvals, key=lambda k: pvals[k])
    n = len(nomes)
    cut = 0
    for i, k in enumerate(nomes, 1):
        if pvals[k] <= alfa * i / n:
            cut = i
    return {k: bool(i <= cut) for i, k in enumerate(nomes, 1)}


def main() -> None:
    verificar_fontes()
    m = base()
    registrar("h1.municipios_na_analise", int(len(m)))
    registrar("h1.municipios_sem_covariaveis", int(m.pct_evangelicos.isna().sum()))
    maiores = m.groupby("uf").v26.sum().sort_values(ascending=False).head(5).index.tolist()
    registrar("bh.cinco_maiores_ufs_por_validos_2026", maiores)
    h1(m)
    r = h8_h13(m, maiores)
    r7 = h7(m)
    h6_municipal(m, maiores)
    r9 = h9(m)
    r3 = h3(m)
    p = {"H3_desocupacao_uf": r3["d_desocupacao_pontos"]["p"], "H3_renda_uf": r3["d_renda_real_pct"]["p"], "H7_h5": r7["direita_vs_nao_direita_h5"]["V"]["p"],
         "H8_evangelicos": r["H8_evangelicos"]["principal"]["p"], "H13_jovens": r["H13_jovens_16_a_24"]["principal"]["p"], "H13_60_mais": r["H13_60_mais"]["principal"]["p"], "H13_superior": r["H13_superior"]["principal"]["p"]}
    b = bh(p)
    registrar("bh.p_valores", p)
    registrar("bh.passa_a_5pct", b)
    print(json.dumps({"bh": b, "p": {k: round(v, 4) for k, v in p.items()}}, ensure_ascii=False, indent=1))
    for k in ("h1", "h3", "h7", "h8", "h9", "h13"):
        print(k, json.dumps(json.load(open(RES / "RESUMO.json", encoding="utf-8")).get(k), ensure_ascii=False)[:2300])


if __name__ == "__main__":
    main()
