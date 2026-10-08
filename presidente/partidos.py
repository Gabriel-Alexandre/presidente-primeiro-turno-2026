"""Partidos nos grupos de campo pela AUTODECLARACAO e a regra de tres grupos do autor.

Copiado do projeto congresso-e-governos-eleicoes-2026 (ferramentas/analise-11-pl-e-blocos.py, commit f6a1f9e), onde a fonte e o Valor
Economico (ago/2026, como cada partido se define). Regra de tres grupos (autor, 07/out/2026): direita = direita + centro-direita;
centro = so centro; esquerda = esquerda + centro-esquerda.
"""
from __future__ import annotations

import re
import unicodedata

AUTO = {
    "PL": "direita", "NOVO": "direita", "MISSAO": "direita",
    "PP": "centro-direita", "REPUBLICANOS": "centro-direita", "UNIAO": "centro-direita", "PRD": "centro-direita",
    "MDB": "centro", "PSD": "centro", "SOLIDARIEDADE": "centro", "AVANTE": "centro", "MOBILIZA": "centro", "DEMOCRATA": "centro",
    "PSDB": "centro", "CIDADANIA": "centro", "AGIR": "centro", "PODE": "centro", "DC": "centro", "PRTB": "centro",
    "PSB": "centro-esquerda", "PDT": "centro-esquerda", "REDE": "centro-esquerda",
    "PT": "esquerda", "PCDOB": "esquerda", "PV": "esquerda", "PSOL": "esquerda", "PCB": "esquerda", "PSTU": "esquerda", "UP": "esquerda", "PCO": "esquerda",
}
HERDEIRO = {
    "DEM": "UNIAO", "PSL": "UNIAO", "PFL": "UNIAO", "PTB": "PRD", "PATRIOTA": "PRD", "PATRI": "PRD", "PEN": "PRD", "PRP": "PRD", "PAN": "PRD",
    "PR": "PL", "PRONA": "PL", "PRB": "REPUBLICANOS", "PPB": "PP", "PMDB": "MDB", "PROS": "SOLIDARIEDADE", "SD": "SOLIDARIEDADE",
    "PSC": "PODE", "PHS": "PODE", "PTN": "PODE", "PODEMOS": "PODE", "PPL": "PCDOB", "PC DO B": "PCDOB", "PSDC": "DC", "PPS": "CIDADANIA",
    "PMN": "MOBILIZA", "PTC": "AGIR", "PT DO B": "AVANTE", "UNIAO BRASIL": "UNIAO", "PODEMOS ": "PODE", "PCDOB ": "PCDOB",
}
TRES = {"direita": "direita", "centro-direita": "direita", "centro": "centro", "centro-esquerda": "esquerda", "esquerda": "esquerda"}


def sigla(p: str) -> str:
    s = unicodedata.normalize("NFKD", str(p)).encode("ascii", "ignore").decode().upper().strip()
    return re.sub(r"\s+", " ", s.replace("�", ""))


def grupo5(p: str) -> str:
    s = sigla(p)
    s = HERDEIRO.get(s, s)
    return AUTO.get(s, "sem classificacao")


def grupo3(p: str) -> str:
    return TRES.get(grupo5(p), "sem classificacao")
