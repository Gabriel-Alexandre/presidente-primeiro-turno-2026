"""Ponte municipio TSE -> IBGE, populacao, capital, porte e regiao. Le o municipios.parquet do projeto do Congresso (por hash)."""
from __future__ import annotations

import pandas as pd

from .comum import CONGRESSO, REGIAO

# codigos IBGE das 27 capitais (dado de referencia do IBGE; conferido por nome em carregar())
CAPITAIS = {
    "AC": ("1200401", "Rio Branco"), "AL": ("2704302", "Maceió"), "AM": ("1302603", "Manaus"), "AP": ("1600303", "Macapá"),
    "BA": ("2927408", "Salvador"), "CE": ("2304400", "Fortaleza"), "DF": ("5300108", "Brasília"), "ES": ("3205309", "Vitória"),
    "GO": ("5208707", "Goiânia"), "MA": ("2111300", "São Luís"), "MG": ("3106200", "Belo Horizonte"), "MS": ("5002704", "Campo Grande"),
    "MT": ("5103403", "Cuiabá"), "PA": ("1501402", "Belém"), "PB": ("2507507", "João Pessoa"), "PE": ("2611606", "Recife"),
    "PI": ("2211001", "Teresina"), "PR": ("4106902", "Curitiba"), "RJ": ("3304557", "Rio de Janeiro"), "RN": ("2408102", "Natal"),
    "RO": ("1100205", "Porto Velho"), "RR": ("1400100", "Boa Vista"), "RS": ("4314902", "Porto Alegre"), "SC": ("4205407", "Florianópolis"),
    "SE": ("2800308", "Aracaju"), "SP": ("3550308", "São Paulo"), "TO": ("1721000", "Palmas"),
}


def carregar() -> pd.DataFrame:
    m = pd.read_parquet(CONGRESSO / "dados" / "derivados" / "municipios.parquet")
    m = m.copy()
    m["mun"] = m["mun"].astype(int)
    cap = {v[0]: (u, v[1]) for u, v in CAPITAIS.items()}
    m["capital"] = m.ibge.astype(str).isin(cap)
    achadas = m[m.capital]
    ruins = [(r.ibge, r.nome_ibge) for r in achadas.itertuples() if cap[str(r.ibge)][1] != r.nome_ibge]
    if ruins:
        raise RuntimeError(f"capital com nome diferente: {ruins}")
    if len(achadas) != 27:
        raise RuntimeError(f"capitais achadas: {len(achadas)}")
    m["porte"] = pd.cut(m["pop"], [0, 20_000, 100_000, 500_000, 1e12], labels=["ate 20 mil", "20 a 100 mil", "100 a 500 mil", "acima de 500 mil"], right=False).astype(str)
    m["regiao"] = m.uf.map(REGIAO)
    return m[["uf", "mun", "ibge", "nome_ibge", "pop", "capital", "porte", "regiao"]]
