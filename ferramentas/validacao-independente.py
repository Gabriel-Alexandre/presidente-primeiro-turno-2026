"""Recontagem independente (docs/PRE_REGISTRO.md, secao 9): os numeros mais importantes refeitos com codigo novo e fontes diferentes.

Nao usa mun_presidente.parquet, nem presidente.pesquisas, nem os derivados da apuracao. Le:
  2022: votacao por candidato, municipio e zona do TSE (dados abertos), presidente, 1o turno;
  2026: JSON oficial por municipio capturado no oficial.sqlite do projeto da apuracao (nao os boletins);
  pesquisas: texto bruto (wikitext) da Wikipedia, com expressao regular, no lugar do HTML renderizado.
Compara com resultados/RESUMO.json e escreve resultados/validacao_independente.csv.
"""
from __future__ import annotations

import gzip
import json
import re
import sqlite3
import sys
import zipfile
import zlib
from collections import defaultdict
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import APURACAO, BRUTOS, RES  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402

REG = {}
for r, ufs in {"Norte": "AC AM AP PA RO RR TO", "Nordeste": "AL BA CE MA PB PE PI RN SE", "Centro-Oeste": "DF GO MS MT", "Sudeste": "ES MG RJ SP", "Sul": "PR RS SC"}.items():
    for u in ufs.split():
        REG[u] = r


def oficial_2022() -> dict:
    z = zipfile.ZipFile(BRUTOS / "tse" / "votacao_candidato_munzona_2022.zip")
    nome = "votacao_candidato_munzona_2022_BRASIL.csv"
    out = defaultdict(lambda: defaultdict(int))  # (uf, mun) -> cand -> votos
    for ch in pd.read_csv(z.open(nome), sep=";", encoding="latin-1", dtype=str, chunksize=400_000, usecols=["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "CD_CARGO", "NR_CANDIDATO", "QT_VOTOS_NOMINAIS"]):
        ch = ch[(ch.CD_CARGO == "1") & (ch.NR_TURNO == "1")]
        for r in ch.itertuples(index=False):
            out[(r.SG_UF, int(r.CD_MUNICIPIO))][int(r.NR_CANDIDATO)] += int(r.QT_VOTOS_NOMINAIS)
    return out


def oficial_2026() -> dict:
    c = sqlite3.connect(APURACAO / "dados" / "brutos" / "oficial.sqlite")
    out = defaultdict(lambda: defaultdict(int))
    nac = None
    for url, body in c.execute("select url, body from raw where url like '%-c0001-e006257-u.json' and status = 200"):
        pre = url.rsplit("/", 1)[1].split("-")[0]
        try:
            b = gzip.decompress(body)
        except Exception:
            try:
                b = zlib.decompress(body)
            except Exception:
                b = body
        j = json.loads(b)
        if pre == "br":
            nac = j
            continue
        if len(pre) < 7:
            continue
        for ag in j["carg"][0]["agr"]:
            for p in ag["par"]:
                for cd in p["cand"]:
                    out[(pre[:2].upper(), int(pre[2:]))][int(cd["n"])] += int(cd["vap"])
    return out, nac


def main() -> None:
    R = json.load(open(RES / "RESUMO.json", encoding="utf-8"))
    o22 = oficial_2022()
    o26, nac = oficial_2026()
    # 1 e 2: margens nacionais
    tot22 = sum(sum(v.values()) for v in o22.values())
    l22, j22 = sum(v.get(13, 0) for v in o22.values()), sum(v.get(22, 0) for v in o22.values())
    m22 = 100 * (j22 - l22) / tot22
    v26 = {int(cd["n"]): int(cd["vap"]) for ag in nac["carg"][0]["agr"] for p in ag["par"] for cd in p["cand"]}
    tot26_nac = sum(v26.values())
    m26 = 100 * (v26[22] - v26[13]) / tot26_nac
    # recontagem pelos municipios oficiais de 2026 (mesma fonte, outro caminho)
    tot26_mun = sum(sum(v.values()) for v in o26.values())
    f26 = sum(v.get(22, 0) for v in o26.values())
    lu26 = sum(v.get(13, 0) for v in o26.values())
    linhas = []

    def cmp(nome, indep, resumo, tol, un=""):
        d = indep - resumo
        linhas.append({"numero": nome, "recontagem_independente": indep, "resultados_resumo": resumo, "diferenca": d, "tolerancia": tol, "passa": bool(abs(d) <= tol), "unidade": un})

    cmp("margem de 2026 (Flavio menos Lula, pontos dos validos), arquivo oficial nacional", m26, R["a1"]["margem_2026"], 0.02, "pontos")
    cmp("margem de 2022 (Jair menos Lula), arquivo oficial por municipio", m22, R["a1"]["margem_2022"], 0.02, "pontos")
    cmp("virada 2022 para 2026", m26 - m22, R["a1"]["virada_2022_2026"], 0.03, "pontos")
    cmp("ganho do candidato do PL (pontos)", 100 * v26[22] / tot26_nac - 100 * j22 / tot22, R["a1"]["pl_ganho_pontos"], 0.02, "pontos")
    cmp("perda de Lula (pontos)", 100 * l22 / tot22 - 100 * v26[13] / tot26_nac, R["a1"]["pt_perda_pontos"], 0.02, "pontos")
    cmp("votos a mais do candidato do PL", v26[22] - j22, R["a1"]["pl_votos_variacao"], 5000, "votos")
    cmp("votos a menos de Lula", v26[13] - l22, R["a1"]["pt_votos_variacao"], 5000, "votos")
    cmp("outros candidatos na urna de 2026 (% dos validos)", 100 - 100 * (v26[22] + v26[13]) / tot26_nac, 100 - R["a1"]["pl_pct_2026"] - R["a1"]["pt_pct_2026"], 0.02, "pontos")
    # regiao: contribuicao do Sudeste a virada, por deslocamento e participacao, com loops simples
    def regiao(o, cp, ct):
        w, m = defaultdict(float), defaultdict(float)
        pl, pt, v = defaultdict(int), defaultdict(int), defaultdict(int)
        for (uf, mun), d in o.items():
            if uf == "ZZ":
                r = "Exterior"
            else:
                r = REG[uf]
            pl[r] += d.get(cp, 0)
            pt[r] += d.get(ct, 0)
            v[r] += sum(d.values())
        T = sum(v.values())
        for r in v:
            w[r] = v[r] / T
            m[r] = 100 * (pl[r] - pt[r]) / v[r]
        return w, m
    w0, m0 = regiao(o22, 22, 13)
    w1, m1 = regiao(o26, 22, 13)
    contrib = {r: ((w0[r] + w1[r]) / 2) * (m1[r] - m0[r]) + ((m0[r] + m1[r]) / 2) * (w1[r] - w0[r]) for r in set(w0) | set(w1)}
    totc = sum(contrib.values())
    cmp("contribuicao do Sudeste (% da virada)", 100 * contrib["Sudeste"] / totc, R["a2"]["regiao"]["pct_da_virada"]["Sudeste"], 0.5, "% da virada")
    cmp("contribuicao do Nordeste (% da virada)", 100 * contrib["Nordeste"] / totc, R["a2"]["regiao"]["pct_da_virada"]["Nordeste"], 0.5, "% da virada")
    # correlacao municipal Jair 2022 x Flavio 2026, ponderada por validos de 2026
    import numpy as np
    chaves = [k for k in o22 if k in o26 and k[0] != "ZZ"]
    a = np.array([100 * o22[k].get(22, 0) / sum(o22[k].values()) for k in chaves])
    b = np.array([100 * o26[k].get(22, 0) / sum(o26[k].values()) for k in chaves])
    w = np.array([sum(o26[k].values()) for k in chaves], float)
    ma, mb = np.average(a, weights=w), np.average(b, weights=w)
    corr = np.average((a - ma) * (b - mb), weights=w) / np.sqrt(np.average((a - ma) ** 2, weights=w) * np.average((b - mb) ** 2, weights=w))
    cmp("correlacao municipal Jair 2022 x Flavio 2026", float(corr), R["h1"]["correlacoes_municipais_ponderadas"]["jair22_flavio26"], 0.005, "correlacao")
    # pesquisa da vespera do Datafolha pelo wikitext (regex), contra o HTML
    wt = json.load(open(BRUTOS / "wikipedia" / "pesquisas-2026-en.json", encoding="utf-8"))["parse"]["wikitext"]
    i = wt.index("''Datafolha''\n|''3 Oct''")
    cel = [re.sub(r"\{\{.*?\}\}|<ref.*", "", x).strip().split("|")[-1].strip() for x in wt[i:i + 600].split("\n|")[2:6]]
    d = pd.read_parquet(Path(__file__).resolve().parent.parent / "dados" / "derivados" / "pesquisas_2026.parquet")
    x = d[(d.instituto == "Datafolha") & (d.campo_fim.astype(str) == "2026-10-03") & (d.cand.isin(["Lula", "Flavio"]))].drop_duplicates("cand").set_index("cand").pct
    cmp("Datafolha de 3/out, Lula (wikitext x HTML)", float(cel[0].replace("style=", "").split("|")[-1].split()[-1]) if cel and cel[0] else float("nan"), float(x["Lula"]), 0.0, "pontos")
    cmp("Datafolha de 3/out, Flavio (wikitext x HTML)", float(re.findall(r"[\d.]+", cel[1])[-1]) if len(cel) > 1 else float("nan"), float(x["Flavio"]), 0.0, "pontos")
    pub = {int(cd["n"]): float(cd["pvap"].replace(",", ".")) for ag in nac["carg"][0]["agr"] for p in ag["par"] for cd in p["cand"]}
    registrar("val.oficial_2026", {"pct_flavio": pub[22], "pct_lula": pub[13], "margem_dos_percentuais_publicados": round(pub[22] - pub[13], 2), "abstencao_publicada_pct": float(nac["e"]["pa"].replace(",", ".")), "validos": int(nac["v"]["vv"])})
    t = pd.DataFrame(linhas)
    tabela("validacao_independente", t)
    registrar("val.independente", {"numeros": int(len(t)), "passam": int(t.passa.sum()), "falham": t[~t.passa].numero.tolist()})
    pd.set_option("display.width", 250)
    print(t[["numero", "recontagem_independente", "resultados_resumo", "diferenca", "passa"]].round(4).to_string())


if __name__ == "__main__":
    main()
