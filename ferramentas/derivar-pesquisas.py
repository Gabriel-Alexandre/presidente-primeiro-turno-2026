"""Serie de pesquisas de presidente de 2025 e 2026: Wikipedia (indice) casada com o registro do TSE (existencia).

Entra na serie so a pesquisa que (i) aparece no registro do TSE pelo mesmo instituto e com data de fim de campo a ate 3 dias,
e (ii) tem Lula e Flavio no mesmo cenario. O que nao casa sai e fica contado em resultados/pesq_nao_casadas.csv.
EMENDA 1 (pre-registro, 12): o registro do TSE de 2026 so tem pesquisa registrada a partir de 1/jan/2026 (a lei exige registro no
ano eleitoral). Pesquisa com fim de campo ate 31/dez/2025 NAO tem como casar e entra por outra via: a fonte citada precisa
ter sido capturada e conter os valores de Lula e do outro candidato (ferramentas/verificar-pesquisas.py).
Saidas: dados/derivados/pesquisas_2026.parquet (um registro por cenario e candidato) e resultados/pesq_*.csv.
"""
from __future__ import annotations

import re
import sys
from datetime import date
import unicodedata
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import BRUTOS, DER, RES  # noqa: E402
from presidente.pesquisas import ler_tabelas  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402


def norm(t: str) -> str:
    t = unicodedata.normalize("NFKD", str(t)).encode("ascii", "ignore").decode().upper()
    return re.sub(r"[^A-Z0-9 ]", " ", t)


ALIAS = {
    "Datafolha": ["DATAFOLHA"], "Quaest": ["QUAEST"], "AtlasIntel": ["ATLAS"], "Futura": ["FUTURA", "100 CIDADES"], "Nexus": ["NEXUS"],
    "Ideia": ["IDEIA"], "PoderData": ["PODERDATA", "PODER DATA"], "Real Time": ["REAL TIME"], "Vox Brasil": ["VOX"],
    "Palver": ["PALVER"], "Indexa": ["INDEXA"], "MDA": ["CNT", "MDA"], "Paraná Pesquisas": ["PARANA DE PESQUISAS", "PARANA PESQUISAS"],
    "Gerp": ["GERP"], "Veritá": ["VERITA"], "Ipespe": ["IPESPE"], "Ipec": ["IPEC"], "Doxa": ["DOXA"],
    "Genial/Quaest": ["QUAEST"], "Atlas": ["ATLAS"], "Ipsos-Ipec": ["IPEC", "IPSOS"], "Meio/Ideia": ["IDEIA"],
}


def registro() -> pd.DataFrame:
    z = zipfile.ZipFile(BRUTOS / "tse" / "pesquisa_eleitoral_2026.zip")
    d = pd.read_csv(z.open("pesquisa_eleitoral_2026_BRASIL.csv"), sep=";", encoding="latin-1", dtype=str)
    d = d[d.DS_CARGO.str.contains("Presidente", na=False)].copy()
    d["fim"] = pd.to_datetime(d.DT_FIM_PESQUISA, errors="coerce").dt.date
    d["ini"] = pd.to_datetime(d.DT_INICIO_PESQUISA, errors="coerce").dt.date
    d["nome"] = (d.NM_EMPRESA.fillna("") + " " + d.NM_EMPRESA_FANTASIA.fillna("")).map(norm)
    return d


def casar(p: pd.DataFrame, reg: pd.DataFrame) -> pd.DataFrame:
    """p: uma linha por pesquisa. Devolve a coluna 'protocolo' (ou NaN)."""
    achou = []
    for r in p.itertuples():
        aliases = ALIAS.get(r.instituto) or [norm(r.instituto)]
        m = reg[reg.nome.apply(lambda n: any(a in n for a in aliases))]
        m = m[m.fim.apply(lambda d: d is not None and abs((d - r.campo_fim).days) <= 3)]
        achou.append(m.NR_PROTOCOLO_REGISTRO.iloc[0] if len(m) else None)
    p = p.copy()
    p["protocolo"] = achou
    return p


def main() -> None:
    d = ler_tabelas(BRUTOS / "wikipedia" / "pesquisas-2026-en-html.json", {1: 2026, 2: 2026, 3: 2026, 4: 2025, 5: 2025})
    # as duas colunas de nome de candidato: normaliza para um rotulo curto
    curto = {"Luiz Inácio Lula da Silva": "Lula", "Flávio Bolsonaro": "Flavio", "Tarcísio de Freitas": "Tarcisio", "Ciro Gomes": "Ciro",
             "Ratinho Júnior": "Ratinho", "Romeu Zema": "Zema", "Ronaldo Caiado": "Caiado", "Renan Santos": "Renan", "Augusto Cury": "Cury",
             "Eduardo Leite": "Leite", "Michelle Bolsonaro": "Michelle"}
    d["cand"] = d.candidato.map(curto).fillna(d.candidato)
    # so cenarios com Lula e Flavio
    tem = d.groupby("cenario").cand.apply(lambda s: {"Lula", "Flavio"} <= set(s))
    cen_ok = set(tem[tem].index)
    # pesquisas (para o casamento)
    pesq = d.drop_duplicates("pesquisa")[["pesquisa", "instituto", "campo_ini", "campo_fim", "amostra", "url"]].reset_index(drop=True)
    reg = registro()
    pesq = casar(pesq, reg)
    pesq["antes_do_registro"] = pesq.campo_fim.apply(lambda x: x < date(2026, 1, 1))
    pesq["casou"] = pesq.protocolo.notna()
    d = d.merge(pesq[["pesquisa", "protocolo", "casou", "antes_do_registro"]], on="pesquisa", how="left")
    d["tem_lula_flavio"] = d.cenario.isin(cen_ok)
    d["entra"] = (d.casou | d.antes_do_registro) & d.tem_lula_flavio
    d["via"] = d.casou.map({True: "registro_tse"}).fillna(d.antes_do_registro.map({True: "fonte_citada_2025"}))
    # valido: pct / (100 - bni); sem bni, pct / (soma dos candidatos + outros)
    soma = d.groupby("cenario").pct.transform("sum") + d.outros.fillna(0)
    den = (100 - d.bni).where(d.bni.notna(), soma)
    d["valido"] = 100 * d.pct / den
    d["base_valido"] = den
    DER.mkdir(parents=True, exist_ok=True)
    d.drop(columns=["tabela", "ordem"]).to_parquet(DER / "pesquisas_2026.parquet", index=False)
    nc = pesq[~pesq.casou & ~pesq.antes_do_registro].copy()
    tabela("pesq_nao_casadas", nc[["instituto", "campo_ini", "campo_fim", "amostra", "url"]])
    tot = len(pesq)
    por_inst = pesq.groupby("instituto").agg(pesquisas=("pesquisa", "size"), casadas=("casou", "sum"), de_2025=("antes_do_registro", "sum"))
    tabela("pesq_casamento_por_instituto", por_inst.reset_index())
    ent = d[d.entra]
    registrar("b0.pesquisas_wikipedia", tot)
    registrar("b0.pesquisas_casadas_no_registro_tse", int(pesq.casou.sum()))
    registrar("b0.pesquisas_de_2025_fora_do_registro_por_lei", int(pesq.antes_do_registro.sum()))
    registrar("b0.pesquisas_de_2026_fora_do_registro", int((~pesq.casou & ~pesq.antes_do_registro).sum()))
    registrar("b0.pesquisas_na_serie", int(ent.pesquisa.nunique()))
    registrar("b0.cenarios_na_serie", int(ent.cenario.nunique()))
    print("pesquisas", tot, "casadas", int(pesq.casou.sum()), "na serie", ent.pesquisa.nunique(), "cenarios", ent.cenario.nunique())
    print(por_inst.sort_values("pesquisas", ascending=False).to_string())


if __name__ == "__main__":
    main()
