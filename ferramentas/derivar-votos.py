"""Votos de presidente por municipio (e exterior), 2018, 2022 e 2026, a partir dos derivados do projeto da apuracao.

Le dados/derivados/{uf,historico}/*.parquet de ../apuracao-eleicoes-2026 (hash do manifesto conferido antes).
Saida: dados/derivados/mun_presidente.parquet, uma linha por (ano, turno, uf, mun), com aptos, comparecimento,
brancos, nulos e os votos de cada candidato em colunas canonicas.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import DER, UFS, derivado_apuracao, verificar_fontes  # noqa: E402
from presidente.saida import registrar  # noqa: E402

# numero do candidato -> coluna
COLS = {
    (2026, 1): {22: "flavio", 13: "lula", 55: "caiado", 70: "cury", 14: "renan", 30: "zema"},
    (2022, 1): {22: "jair", 13: "lula", 12: "ciro", 15: "tebet", 44: "soraya", 30: "felipe"},
    (2022, 2): {22: "jair", 13: "lula"},
    (2018, 1): {17: "jair", 13: "haddad", 12: "ciro", 45: "alckmin", 30: "amoedo", 18: "marina"},
    (2018, 2): {17: "jair", 13: "haddad"},
}


def um(ano: int, turno: int, uf: str) -> pd.DataFrame:
    vp, sp = derivado_apuracao(uf, None if ano == 2026 else ano, turno)
    v = pd.read_parquet(vp)
    v = v[v.cargo.astype(str) == "1"]
    s = pd.read_parquet(sp)
    if ano == 2026:
        v = v.rename(columns={"mun_cd": "mun"})
        s = s.rename(columns={"mun_cd": "mun"})
    v["mun"] = v["mun"].astype(int)
    s["mun"] = s["mun"].astype(int)
    chave = ["uf", "mun"]
    s = s.groupby(chave, as_index=False)[["aptos", "comparecimento"]].sum()
    nom = v[v.tipo.astype(str) == "1"].copy()
    nom["col"] = nom.numero.astype(int).map(COLS[(ano, turno)]).fillna("outros_nom")
    w = nom.groupby(chave + ["col"], as_index=False).votos.sum().pivot_table(index=chave, columns="col", values="votos", fill_value=0).reset_index()
    br = v[v.tipo.astype(str) == "2"].groupby(chave, as_index=False).votos.sum().rename(columns={"votos": "brancos"})
    nu = v[v.tipo.astype(str) == "3"].groupby(chave, as_index=False).votos.sum().rename(columns={"votos": "nulos"})
    m = s.merge(w, on=chave, how="outer").merge(br, on=chave, how="left").merge(nu, on=chave, how="left")
    m["ano"], m["turno"] = ano, turno
    return m


def main() -> None:
    verificar_fontes()
    partes = []
    for (ano, turno) in COLS:
        for uf in UFS + ["ZZ"]:
            partes.append(um(ano, turno, uf))
        print(ano, turno, "ok", flush=True)
    d = pd.concat(partes, ignore_index=True).fillna(0)
    for c in d.columns:
        if c not in ("uf",):
            d[c] = pd.to_numeric(d[c], errors="coerce").fillna(0).astype("int64") if c not in ("uf",) else d[c]
    nomes = [c for c in d.columns if c not in ("uf", "mun", "aptos", "comparecimento", "brancos", "nulos", "ano", "turno")]
    d["nominais"] = d[nomes].sum(axis=1)
    DER.mkdir(parents=True, exist_ok=True)
    d.to_parquet(DER / "mun_presidente.parquet", index=False)
    g = d.groupby(["ano", "turno"])[["aptos", "comparecimento", "brancos", "nulos", "nominais"]].sum()
    print(g.to_string())
    for (ano, turno), r in g.iterrows():
        registrar(f"a1.soma_boletins.{ano}_{turno}", {k: int(r[k]) for k in g.columns})


if __name__ == "__main__":
    main()
