"""Bloco B: B1 (trajetoria), B2 (erro por instituto contra 2018 e 2022), B3 (migracao dos 'outros'), B4 (decomposicao do erro).

Valido de uma pesquisa de 2026: pct / (100 - branco, nulo e indeciso). Valido de 2022: renormalizado entre os candidatos nominais do cenario
(Pindograma). Valido de 2018: o 'pct' do Pindograma. Margem de pesquisa = Flavio (ou Jair) menos Lula (ou Haddad), em pontos.
Erro = margem da pesquisa menos margem da urna; negativo = a pesquisa mostrou o candidato do PL pior do que ele teve.
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import CONGRESSO, DER, RES, verificar_fontes  # noqa: E402
from presidente.saida import ler, registrar, tabela  # noqa: E402

ELEICAO_2026 = date(2026, 10, 4)
ELEICAO_2022 = date(2022, 10, 2)
ELEICAO_2018 = date(2018, 10, 7)


def melhor_cenario() -> pd.DataFrame:
    """Uma linha por pesquisa, com o cenario de Lula e Flavio que tem mais candidatos."""
    d = pd.read_parquet(DER / "pesquisas_2026.parquet")
    d = d[d.entra]
    cen = d.groupby(["pesquisa", "cenario"]).agg(n=("cand", "nunique"), conjunto=("cand", lambda s: "+".join(sorted(s)))).reset_index()
    cen = cen.sort_values(["pesquisa", "n", "cenario"], ascending=[True, False, True]).drop_duplicates("pesquisa")
    x = d.merge(cen[["pesquisa", "cenario"]], on=["pesquisa", "cenario"])
    p = x.pivot_table(index=["pesquisa", "instituto", "campo_fim", "via", "vespera_verificada", "bni"], columns="cand", values=["valido", "pct"], aggfunc="first")
    p.columns = [f"{a}_{b}" for a, b in p.columns]
    p = p.reset_index().merge(cen[["pesquisa", "n", "conjunto"]], on="pesquisa")
    p["campo_fim"] = pd.to_datetime(p.campo_fim)
    p["margem"] = p.valido_Flavio - p.valido_Lula
    p["outros_valido"] = 100 - p.valido_Lula - p.valido_Flavio
    return p.sort_values("campo_fim").reset_index(drop=True)


def efeito_casa(p: pd.DataFrame) -> pd.Series:
    """Desvio medio de cada instituto em relacao a media dos OUTROS institutos numa janela de +-7 dias."""
    dev = {}
    for i, r in p.iterrows():
        o = p[(p.instituto != r.instituto) & ((p.campo_fim - r.campo_fim).abs() <= pd.Timedelta(days=7))]
        if len(o) >= 2:
            dev[i] = r.margem - o.margem.mean()
    s = pd.Series(dev)
    return p.loc[s.index].assign(dev=s).groupby("instituto").dev.mean()


def b1(p: pd.DataFrame) -> pd.DataFrame:
    h = efeito_casa(p)
    p = p.assign(casa=p.instituto.map(h).fillna(0.0))
    p["margem_aj"] = p.margem - p.casa
    p = p[p.campo_fim >= "2025-12-01"].copy()
    sem = p.assign(semana=p.campo_fim.dt.to_period("W-SUN").dt.start_time).groupby("semana").agg(
        pesquisas=("pesquisa", "size"), institutos=("instituto", "nunique"), margem_flavio_menos_lula=("margem_aj", "mean"),
        lula=("valido_Lula", "mean"), flavio=("valido_Flavio", "mean"), outros=("outros_valido", "mean")).reset_index()
    tabela("b1_efeito_casa", h.rename("desvio_medio_pontos").reset_index())
    tabela("b1_semanal_2026", sem)
    tabela("b1_pesquisas", p[["pesquisa", "instituto", "campo_fim", "via", "n", "conjunto", "valido_Lula", "valido_Flavio", "outros_valido", "margem", "casa", "margem_aj"]])
    registrar("b1.pesquisas_na_serie_dez2025_em_diante", int(p.pesquisa.nunique()))
    registrar("b1.institutos", sorted(p.instituto.unique()))
    registrar("b1.efeito_casa_pontos", {k: round(v, 2) for k, v in h.items()})
    # marcos: primeira semana, ponto de virada (primeira semana com margem ajustada > 0), ultima
    pos = sem[sem.margem_flavio_menos_lula > 0]
    registrar("b1.primeira_semana", {"semana": str(sem.iloc[0].semana.date()), "margem": float(sem.iloc[0].margem_flavio_menos_lula)})
    registrar("b1.ultima_semana", {"semana": str(sem.iloc[-1].semana.date()), "margem": float(sem.iloc[-1].margem_flavio_menos_lula)})
    registrar("b1.primeira_semana_com_flavio_na_frente", str(pos.iloc[0].semana.date()) if len(pos) else None)
    registrar("b1.semanas_com_flavio_na_frente", int(len(pos)))
    # ultimos 60 dias, por semana
    registrar("b1.margem_por_semana_ultimos_60_dias", {str(r.semana.date()): round(float(r.margem_flavio_menos_lula), 2) for r in sem[sem.semana >= pd.Timestamp(ELEICAO_2026 - timedelta(days=63))].itertuples()})
    return p


def pindograma_2022() -> pd.DataFrame:
    d = pd.read_csv(CONGRESSO / "dados/brutos/capturas/pindograma-late-polls-2022.csv", low_memory=False)
    d = d[(d.CD_CARGO == 1) & (d.turno == 1) & (d.polled_UE == "BR") & (d.estimulada == 1) & (d.NUMERO_CANDIDATO > 0)]
    d["fim"] = pd.to_datetime(d.DT_FIM_PESQUISA)
    g = d.groupby(["NR_IDENTIFICACAO_PESQUISA", "scenario_id"])
    d["soma"] = g.result.transform("sum")
    d["valido"] = 100 * d.result / d.soma
    d["instituto"] = d.pretty_name
    p = d.pivot_table(index=["NR_IDENTIFICACAO_PESQUISA", "scenario_id", "instituto", "fim"], columns="NUMERO_CANDIDATO", values="valido", aggfunc="first").reset_index()
    p = p.rename(columns={13: "Lula", 22: "Jair"}).dropna(subset=["Lula", "Jair"])
    p["margem"] = p.Jair - p.Lula
    p["outros"] = 100 - p.Lula - p.Jair
    return p


def pindograma_2018() -> pd.DataFrame:
    a = pd.read_csv(CONGRESSO / "dados/brutos/capturas/pindograma-late-polls-2012-2018.csv", low_memory=False)
    a = a[(a.year == 2018) & (a.CD_CARGO == 1) & (a.turno == 1) & (a.polled_UE == "BR") & (a.estimulada == 1)]
    a["fim"] = pd.to_datetime(a.DT_FIM_PESQUISA)
    p = a.pivot_table(index=["NR_IDENTIFICACAO_PESQUISA", "scenario_id", "pretty_name", "fim"], columns="NUMERO_CANDIDATO", values="pct", aggfunc="first").reset_index()
    p = p.rename(columns={13: "Haddad", 17: "Jair", "pretty_name": "instituto"}).dropna(subset=["Haddad", "Jair"])
    p["margem"] = p.Jair - p.Haddad
    p["outros"] = 100 - p.Haddad - p.Jair
    return p


def b2_b3(p26: pd.DataFrame) -> None:
    urna = {2026: (ler("a1.pt_pct_2026"), ler("a1.pl_pct_2026")), 2022: (ler("a1.pt_pct_2022"), ler("a1.pl_pct_2022")), 2018: (ler("a1.pt_pct_2018"), ler("a1.pl_pct_2018"))}
    m_urna = {a: v[1] - v[0] for a, v in urna.items()}
    o_urna = {a: 100 - v[0] - v[1] for a, v in urna.items()}
    linhas = []
    # 2026: ultima pesquisa de cada instituto na vespera (campo de 28/set a 3/out), so as verificadas em fonte
    v = p26[(p26.campo_fim >= "2026-09-28") & (p26.campo_fim <= "2026-10-03")]
    for nome, x in v.groupby("instituto"):
        r = x.sort_values("campo_fim").iloc[-1]
        linhas.append({"ano": 2026, "instituto": nome, "campo_fim": r.campo_fim.date(), "pt": r.valido_Lula, "pl": r.valido_Flavio, "outros": r.outros_valido, "verificada": bool(r.vespera_verificada), "fonte_dupla": bool(r.vespera_verificada)})
    for ano, df, ptc, plc, ele, janela in ((2022, pindograma_2022(), "Lula", "Jair", ELEICAO_2022, 8), (2018, pindograma_2018(), "Haddad", "Jair", ELEICAO_2018, 8)):
        w = df[(df.fim >= pd.Timestamp(ele - timedelta(days=janela)))]
        for nome, x in w.groupby("instituto"):
            r = x.sort_values("fim").iloc[-1]
            linhas.append({"ano": ano, "instituto": nome, "campo_fim": r.fim.date(), "pt": r[ptc], "pl": r[plc], "outros": r.outros, "verificada": True, "fonte_dupla": False})
    e = pd.DataFrame(linhas)
    e["margem_pesquisa"] = e.pl - e.pt
    e["margem_urna"] = e.ano.map(m_urna)
    e["erro_margem"] = e.margem_pesquisa - e.margem_urna
    e["erro_pt"] = e.pt - e.ano.map(lambda a: urna[a][0])
    e["erro_pl"] = e.pl - e.ano.map(lambda a: urna[a][1])
    e["outros_urna"] = e.ano.map(o_urna)
    e["queda_outros"] = e.outros_urna - e.outros  # negativo: os outros tiveram menos na urna do que na pesquisa
    # fracao da queda dos outros que foi para o candidato do PL: ganho do PL / (-queda dos outros)
    e["pl_ganho_sobre_pesquisa"] = -e.erro_pl
    e["fracao_pl"] = np.where(e.queda_outros < 0, e.pl_ganho_sobre_pesquisa / (-e.queda_outros), np.nan)
    tabela("b2_erro_por_instituto", e)
    for ano in (2018, 2022, 2026):
        x = e[(e.ano == ano) & e.verificada]
        registrar(f"b2.{ano}", {"institutos": int(len(x)), "erro_margem_medio": float(x.erro_margem.mean()), "erro_margem_mediano": float(x.erro_margem.median()),
                                  "erro_pl_medio": float(x.erro_pl.mean()), "erro_pt_medio": float(x.erro_pt.mean()),
                                  "institutos_com_pl_subestimado": int((x.erro_pl < 0).sum()), "institutos_com_pt_subestimado": int((x.erro_pt < 0).sum()),
                                  "queda_outros_media": float(x.queda_outros.mean()), "fracao_pl_media": float(x.fracao_pl.mean()), "fracao_pl_mediana": float(x.fracao_pl.median())})
    registrar("b2.2026_apenas_fonte_dupla_ou_verificada", int(e[(e.ano == 2026) & e.verificada].shape[0]))
    # institutos presentes em varios anos
    pres = e[e.verificada].pivot_table(index="instituto", columns="ano", values="erro_margem", aggfunc="first")
    tabela("b2_erro_margem_por_instituto_e_ano", pres.reset_index())


def b3_serie_final(p: pd.DataFrame) -> None:
    """A serie dos ultimos 21 dias dos tres institutos com mais rodadas na campanha."""
    x = p[(p.campo_fim >= pd.Timestamp(ELEICAO_2026 - timedelta(days=21)))]
    top = x.groupby("instituto").size().sort_values(ascending=False).head(5).index
    t = x[x.instituto.isin(top)][["instituto", "campo_fim", "valido_Lula", "valido_Flavio", "outros_valido", "margem", "vespera_verificada"]].sort_values(["instituto", "campo_fim"])
    tabela("b3_ultimos_21_dias", t)
    # variacao dos outros do primeiro ao ultimo ponto de cada instituto na janela
    res = {}
    for nome, g in t.groupby("instituto"):
        if len(g) >= 2:
            res[nome] = {"pesquisas": int(len(g)), "outros_inicio": float(g.iloc[0].outros_valido), "outros_fim": float(g.iloc[-1].outros_valido),
                         "margem_inicio": float(g.iloc[0].margem), "margem_fim": float(g.iloc[-1].margem), "dias": int((g.iloc[-1].campo_fim - g.iloc[0].campo_fim).days)}
    registrar("b3.ultimos_21_dias", res)


def b4(p: pd.DataFrame) -> None:
    """Decomposicao do erro de margem na vespera: parte 'mudanca de ultima hora' (extrapolacao linear do mesmo instituto) e residuo.
    Comparecimento diferencial (correlacao do erro da UF) so e possivel com pesquisa por UF; fica fora (dito no relatorio)."""
    m_urna = ler("a1.pl_pct_2026") - ler("a1.pt_pct_2026")
    linhas = []
    for nome, g in p[(p.campo_fim >= pd.Timestamp(ELEICAO_2026 - timedelta(days=21)))].groupby("instituto"):
        g = g.sort_values("campo_fim")
        v = g[(g.campo_fim >= "2026-09-28")]
        if len(g) < 3 or v.empty:
            continue
        ult = v.iloc[-1]
        if not bool(ult.vespera_verificada):
            continue
        dias = (g.campo_fim - g.campo_fim.iloc[0]).dt.days.to_numpy().astype(float)
        a, b = np.polyfit(dias, g.margem.to_numpy(), 1)
        ate_urna = (pd.Timestamp(ELEICAO_2026) - g.campo_fim.iloc[0]).days
        extrap = a * ate_urna + b
        erro = ult.margem - m_urna
        mudanca = min(abs(extrap - ult.margem), abs(erro)) * np.sign(-erro) if abs(erro) > 0 else 0.0
        linhas.append({"instituto": nome, "pesquisas_21d": len(g), "inclinacao_pontos_por_dia": a, "margem_ultima": ult.margem, "margem_extrapolada": extrap, "margem_urna": m_urna,
                       "erro_ultima": erro, "parte_ultima_hora_limitada_ao_erro": mudanca, "residuo": erro - mudanca, "verificada": bool(ult.vespera_verificada)})
    t = pd.DataFrame(linhas)
    tabela("b4_decomposicao_erro", t)
    if len(t):
        registrar("b4.institutos", int(len(t)))
        registrar("b4.erro_medio", float(t.erro_ultima.mean()))
        registrar("b4.parte_ultima_hora_media", float(t.parte_ultima_hora_limitada_ao_erro.mean()))
        registrar("b4.residuo_medio", float(t.residuo.mean()))


def main() -> None:
    verificar_fontes()
    p = melhor_cenario()
    p1 = b1(p)
    b2_b3(p)
    b3_serie_final(p)
    b4(p)
    import json
    r = json.load(open(RES / "RESUMO.json", encoding="utf-8"))
    for k in ("b1", "b2", "b3", "b4"):
        print(k, json.dumps(r.get(k), ensure_ascii=False)[:1800])


if __name__ == "__main__":
    main()
