"""Validacao por dois caminhos (docs/PRE_REGISTRO.md, secao 9): votos por municipio dos boletins contra o resultado oficial.

2018 e 2022: arquivo de votacao por candidato, municipio e zona dos dados abertos do TSE.
2026: JSON oficial por municipio (c0001 = presidente, 1o turno) capturado pelo projeto da apuracao (oficial.sqlite).
Saidas: resultados/val_votos_<ano>.csv (diferencas) e chaves em RESUMO.json (a1.validacao.*).
"""
from __future__ import annotations

import gzip
import json
import sqlite3
import sys
import zipfile
import zlib
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import APURACAO, BRUTOS, DER  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402

COLS = {
    (2026, 1): {22: "flavio", 13: "lula", 55: "caiado", 70: "cury", 14: "renan", 30: "zema"},
    (2022, 1): {22: "jair", 13: "lula", 12: "ciro", 15: "tebet", 44: "soraya", 30: "felipe"},
    (2022, 2): {22: "jair", 13: "lula"},
    (2018, 1): {17: "jair", 13: "haddad", 12: "ciro", 45: "alckmin", 30: "amoedo", 18: "marina"},
    (2018, 2): {17: "jair", 13: "haddad"},
}


def oficial_historico(ano: int) -> pd.DataFrame:
    z = zipfile.ZipFile(BRUTOS / "tse" / f"votacao_candidato_munzona_{ano}.zip")
    nome = f"votacao_candidato_munzona_{ano}_BRASIL.csv"
    partes = []
    for ch in pd.read_csv(z.open(nome), sep=";", encoding="latin-1", dtype=str, chunksize=400_000,
                          usecols=["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "CD_CARGO", "NR_CANDIDATO", "QT_VOTOS_NOMINAIS"]):
        ch = ch[ch.CD_CARGO == "1"]
        ch["v"] = pd.to_numeric(ch.QT_VOTOS_NOMINAIS, errors="coerce").fillna(0)
        partes.append(ch.groupby(["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_CANDIDATO"], as_index=False).v.sum())
    d = pd.concat(partes).groupby(["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_CANDIDATO"], as_index=False).v.sum()
    d.columns = ["turno", "uf", "mun", "numero", "votos"]
    d["turno"] = d.turno.astype(int)
    d["mun"] = d.mun.astype(int)
    d["numero"] = d.numero.astype(int)
    return d


def oficial_2026() -> pd.DataFrame:
    c = sqlite3.connect(APURACAO / "dados" / "brutos" / "oficial.sqlite")
    linhas = []
    for url, body in c.execute("select url, body from raw where url like '%/dados/%-c0001-e006257-u.json' and status = 200"):
        nome = url.rsplit("/", 1)[1]
        pre = nome.split("-")[0]
        if pre == "br" or len(pre) < 7:  # br ou uf; municipio e uf(2)+codigo(5)
            continue
        uf, mun = pre[:2].upper(), int(pre[2:])
        try:
            b = gzip.decompress(body)
        except Exception:
            try:
                b = zlib.decompress(body)
            except Exception:
                b = body
        j = json.loads(b)
        for ag in j["carg"][0]["agr"]:
            for p in ag["par"]:
                for cd in p["cand"]:
                    linhas.append((1, uf, mun, int(cd["n"]), int(cd["vap"])))
    return pd.DataFrame(linhas, columns=["turno", "uf", "mun", "numero", "votos"])


def comparar(ano: int, turno: int, ofi: pd.DataFrame, mine: pd.DataFrame) -> None:
    mapa = COLS[(ano, turno)]
    o = ofi[ofi.turno == turno].copy()
    o["col"] = o.numero.map(mapa)
    o = o.dropna(subset=["col"])
    m = mine[(mine.ano == ano) & (mine.turno == turno)]
    longo = m.melt(id_vars=["uf", "mun"], value_vars=list(mapa.values()), var_name="col", value_name="meu")
    x = longo.merge(o[["uf", "mun", "col", "votos"]], on=["uf", "mun", "col"], how="outer").fillna(0)
    x["dif"] = x.meu - x.votos
    iguais = int((x.dif == 0).sum())
    chave = f"a1.validacao.{ano}_{turno}"
    registrar(chave, {
        "pares_municipio_candidato": len(x), "iguais": iguais, "pct_iguais": round(100 * iguais / len(x), 3),
        "dif_total_votos": int(x.dif.sum()), "dif_absoluta_maxima": int(x.dif.abs().max()),
        "municipios_com_diferenca": int(x[x.dif != 0].mun.nunique()),
        "nacional_meu": {k: int(v) for k, v in x.groupby("col").meu.sum().items()},
        "nacional_oficial": {k: int(v) for k, v in x.groupby("col").votos.sum().items()},
    })
    tabela(f"val_votos_{ano}_{turno}", x[x.dif != 0].sort_values("dif"))
    print(ano, turno, "pares", len(x), "iguais", iguais, "dif total", int(x.dif.sum()), "max", int(x.dif.abs().max()), flush=True)


def main() -> None:
    mine = pd.read_parquet(DER / "mun_presidente.parquet")
    for ano in (2022, 2018):
        ofi = oficial_historico(ano)
        for turno in (1, 2):
            comparar(ano, turno, ofi, mine)
    comparar(2026, 1, oficial_2026(), mine)


if __name__ == "__main__":
    main()
