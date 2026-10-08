"""Prefeitos de 2024 por municipio: os dois primeiros da rodada decisiva, o partido, o grupo de campo e a margem (H7).

Fonte: votacao por candidato, municipio e zona de 2024 (dados abertos do TSE). Rodada decisiva = 2o turno quando houve, senao o 1o.
Saida: dados/derivados/prefeitos_2024.parquet. Conferencia: o eleito de cada municipio tem de ser o 1o colocado dos votos nominais.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente import partidos  # noqa: E402
from presidente.comum import BRUTOS, DER  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402


def main() -> None:
    z = zipfile.ZipFile(BRUTOS / "tse" / "votacao_candidato_munzona_2024.zip")
    nome = [n for n in z.namelist() if "BRASIL" in n.upper() and n.endswith(".csv")][0]
    partes = []
    for ch in pd.read_csv(z.open(nome), sep=";", encoding="latin-1", dtype=str, chunksize=400_000,
                          usecols=["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "CD_CARGO", "SQ_CANDIDATO", "SG_PARTIDO", "QT_VOTOS_NOMINAIS", "DS_SIT_TOT_TURNO"]):
        ch = ch[ch.CD_CARGO == "11"]
        ch["v"] = pd.to_numeric(ch.QT_VOTOS_NOMINAIS, errors="coerce").fillna(0)
        partes.append(ch.groupby(["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "SQ_CANDIDATO", "SG_PARTIDO", "DS_SIT_TOT_TURNO"], as_index=False).v.sum())
    d = pd.concat(partes).groupby(["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "SQ_CANDIDATO", "SG_PARTIDO", "DS_SIT_TOT_TURNO"], as_index=False).v.sum()
    d["turno"] = d.NR_TURNO.astype(int)
    d["mun"] = d.CD_MUNICIPIO.astype(int)
    d = d.rename(columns={"SG_UF": "uf"})
    decisiva = d.groupby(["uf", "mun"]).turno.transform("max")
    d = d[d.turno == decisiva]
    d["validos"] = d.groupby(["uf", "mun"]).v.transform("sum")
    d = d.sort_values(["uf", "mun", "v"], ascending=[True, True, False])
    d["pos"] = d.groupby(["uf", "mun"]).cumcount() + 1
    top = d[d.pos <= 2].copy()
    top["pct"] = 100 * top.v / top.validos
    a = top[top.pos == 1].set_index(["uf", "mun"])
    b = top[top.pos == 2].set_index(["uf", "mun"])
    m = pd.DataFrame({"turno": a.turno, "validos": a.validos, "partido_1": a.SG_PARTIDO, "pct_1": a.pct, "sit_1": a.DS_SIT_TOT_TURNO,
                      "partido_2": b.SG_PARTIDO, "pct_2": b.pct}).dropna(subset=["partido_2"]).reset_index()
    m["margem"] = m.pct_1 - m.pct_2
    m["g1"] = m.partido_1.map(partidos.grupo3)
    m["g2"] = m.partido_2.map(partidos.grupo3)
    m["pl1"] = m.partido_1.map(partidos.sigla).eq("PL")
    m["pl2"] = m.partido_2.map(partidos.sigla).eq("PL")
    # conferencia: o 1o colocado tem de constar como eleito
    elei = m.sit_1.fillna("").str.upper().str.contains("ELEITO") & ~m.sit_1.fillna("").str.upper().str.contains("NÃO|NAO")
    registrar("h7.municipios_com_prefeito", int(len(m)))
    registrar("h7.primeiro_colocado_nao_consta_eleito", int((~elei).sum()))
    registrar("h7.decididos_em_2o_turno", int((m.turno == 2).sum()))
    # elegivel para o teste: exatamente um dos dois e de direita e o outro esta classificado e nao e de direita
    c1 = (m.g1 == "direita") & (m.g2.isin(["centro", "esquerda"]))
    c2 = (m.g2 == "direita") & (m.g1.isin(["centro", "esquerda"]))
    m["elegivel"] = c1 | c2
    m["direita_ganhou"] = c1
    m["corrida"] = np.where(c1, m.margem, np.where(c2, -m.margem, np.nan))
    # variante so PL
    p1 = m.pl1 & (m.g2.isin(["centro", "esquerda", "direita"]) & ~m.pl2)
    p2 = m.pl2 & (m.g1.isin(["centro", "esquerda", "direita"]) & ~m.pl1)
    m["elegivel_pl"] = p1 | p2
    m["corrida_pl"] = np.where(p1, m.margem, np.where(p2, -m.margem, np.nan))
    DER.mkdir(exist_ok=True, parents=True)
    m.to_parquet(DER / "prefeitos_2024.parquet", index=False)
    registrar("h7.elegiveis_direita_contra_nao_direita", int(m.elegivel.sum()))
    registrar("h7.elegiveis_pl", int(m.elegivel_pl.sum()))
    registrar("h7.sem_classificacao", int(((m.g1 == "sem classificacao") | (m.g2 == "sem classificacao")).sum()))
    print(len(m), int(m.elegivel.sum()), int(m.elegivel_pl.sum()))
    print(m.g1.value_counts().to_dict())


if __name__ == "__main__":
    main()
