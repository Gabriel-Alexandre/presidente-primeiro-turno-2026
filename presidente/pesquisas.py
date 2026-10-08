"""Leitura das tabelas de pesquisa da Wikipedia (HTML renderizado), com celulas mescladas expandidas.

Uma linha de tabela e um CENARIO de uma pesquisa. A mesma pesquisa (instituto + campo + amostra) pode ter varios cenarios.
A Wikipedia e um indice (cada pesquisa cita sua fonte); o valor so entra na serie depois do casamento com o registro do TSE
e da conferencia por amostra (docs/PRE_REGISTRO.md, bloco B).
"""
from __future__ import annotations

import json
import re
from datetime import date

import pandas as pd
from bs4 import BeautifulSoup

MESES = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}


def _num(txt: str):
    t = txt.replace("\xa0", " ").replace(",", "").strip()
    m = re.match(r"^[<>~≈]?\s*(\d+(?:\.\d+)?)\s*%?$", t)
    return float(m.group(1)) if m else None


def _grade(tabela) -> list[list]:
    """Expande rowspan e colspan. Cada celula vira (texto, tag, elemento)."""
    linhas = tabela.find_all("tr")
    grade: list[list] = []
    pend: dict[tuple[int, int], tuple] = {}
    for i, tr in enumerate(linhas):
        row: list = []
        col = 0
        cels = tr.find_all(["td", "th"], recursive=False)
        it = iter(cels)
        while True:
            while (i, col) in pend:
                row.append(pend.pop((i, col)))
                col += 1
            c = next(it, None)
            if c is None:
                break
            rs = int(c.get("rowspan", 1) or 1)
            cs = int(c.get("colspan", 1) or 1)
            for k in range(cs):
                cel = (c.get_text(" ", strip=True), c.name, c)
                row.append(cel)
                for r in range(1, rs):
                    pend[(i + r, col)] = cel
                col += 1
        while (i, col) in pend:
            row.append(pend.pop((i, col)))
            col += 1
        grade.append(row)
    return grade


def _datas(txt: str, ano: int):
    t = txt.replace("\xa0", " ").replace("–", "-").replace("—", "-")
    m = re.match(r"^(\d{1,2})\s*([A-Za-z]{3})?\s*-\s*(\d{1,2})\s*([A-Za-z]{3})", t)
    if m:
        d1, m1, d2, m2 = int(m.group(1)), m.group(2), int(m.group(3)), m.group(4)
        m1 = m1 or m2
        try:
            f = date(ano, MESES[m2], d2)
            ya = ano - 1 if MESES[m1] > MESES[m2] else ano
            i = date(ya, MESES[m1], d1)
            return i, f
        except (KeyError, ValueError):
            return None, None
    m = re.match(r"^(\d{1,2})\s*([A-Za-z]{3})", t)
    if m:
        try:
            d = date(ano, MESES[m.group(2)], int(m.group(1)))
            return d, d
        except (KeyError, ValueError):
            return None, None
    return None, None


def _titulo(c):
    a = c[2].find("a")
    t = a.get("title") if a else None
    return t if t and not t.startswith("File:") else None


def _referencias(soup) -> dict[str, str]:
    out = {}
    for li in soup.select("ol.references li[id]"):
        a = li.select_one("a.external, a[rel~=nofollow]")
        if a and a.get("href"):
            out[li["id"]] = a["href"]
    return out


def ler_tabelas(caminho_json, tabelas_ano: dict[int, int]) -> pd.DataFrame:
    """tabelas_ano: {indice da tabela wikitable (ordem no HTML): ano}. Devolve uma linha por cenario e candidato."""
    h = json.load(open(caminho_json, encoding="utf-8"))["parse"]["text"]
    soup = BeautifulSoup(h, "lxml")
    refs = _referencias(soup)
    tabs = soup.find_all("table", class_="wikitable")
    linhas = []
    for ti, ano in tabelas_ano.items():
        g = _grade(tabs[ti])
        cand_row, melhor = None, 1
        for r in g:
            if all(c[1] == "th" for c in r):
                k = sum(1 for c in r if _titulo(c))
                if k > melhor:
                    cand_row, melhor = r, k
        if cand_row is None:
            raise RuntimeError(f"sem cabecalho de candidatos na tabela {ti}")
        nomes = [_titulo(c) for c in cand_row if _titulo(c)]
        n = len(nomes)
        rotulos = [re.sub(r"\s*\[.*?\]\s*", "", c[0]).strip() for c in cand_row if _titulo(c)]
        dados = [r for r in g if any(c[1] == "td" for c in r)]
        for ordem, r in enumerate(dados):
            if len(r) < 2 + n + 4:
                continue
            instituto = r[0][0].strip()
            if instituto.lower().startswith("results") or not instituto:
                continue
            ini, fim = _datas(r[1][0], ano)
            if fim is None:
                continue
            vals = [_num(c[0]) for c in r[2 : 2 + n]]
            resto = [c[0] for c in r[2 + n :]]
            # ordem do resto: [others], blank, moe, amostra, lead, link  (others pode faltar)
            tem_others = len(r) >= 2 + n + 6
            k = 0
            outros = _num(resto[0]) if tem_others else None
            if tem_others:
                k = 1
            bni = _num(resto[k]) if k < len(resto) else None
            amostra = None
            for c in resto[k + 1 : k + 4]:
                t = c.replace(",", "").strip()
                if re.fullmatch(r"\d{3,6}", t):
                    amostra = int(t)
                    break
            url = None
            a_ref = r[-1][2].select_one("sup.reference a[href^='#cite_note']") if r[-1][1] == "td" else None
            if a_ref:
                url = refs.get(a_ref["href"].lstrip("#"))
            for nome, rot, v in zip(nomes, rotulos, vals):
                if v is not None:
                    linhas.append({"tabela": ti, "ordem": ordem, "instituto": instituto, "campo_ini": ini, "campo_fim": fim, "amostra": amostra,
                                   "candidato": nome, "rotulo": rot, "pct": v, "outros": outros, "bni": bni, "n_cand_na_tabela": n, "url": url})
    d = pd.DataFrame(linhas)
    # cenario = linhas consecutivas da mesma tabela com o mesmo indice de linha
    d["cenario"] = d["tabela"].astype(str) + "-" + d["ordem"].astype(str)
    d["pesquisa"] = d["instituto"] + "|" + d["campo_ini"].astype(str) + "|" + d["campo_fim"].astype(str) + "|" + d["amostra"].astype(str)
    return d
