"""Confere os valores da serie contra a fonte citada na Wikipedia (docs/PRE_REGISTRO.md, bloco B e emenda 1).

Escopo: (a) todas as pesquisas da vespera (campo ate 28/set a 3/out de 2026); (b) todas as de 2025 (sem registro no TSE por lei);
(c) 20 pesquisas de 2026 sorteadas (semente 20261007). Para cada uma, captura a pagina citada (sha256 no manifesto) e procura os
valores de Lula e de Flavio, brutos ou validos, no texto. Resultado: confere, diverge ou nao_verificavel (pagina nao abriu).
"""
from __future__ import annotations

import hashlib
import html
import random
import re
import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import BRUTOS, DER, SEMENTE  # noqa: E402
from presidente.manifesto import baixar  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402


def texto(h: str) -> str:
    h = re.sub(r"(?s)<(script|style|noscript)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(h))


def numeros(t: str) -> list[tuple[int, float]]:
    """(posicao, valor) de todo numero seguido de % ou 'por cento'."""
    out = []
    for m in re.finditer(r"(?<![\d.,])(\d{1,3}(?:[.,]\d{1,2})?)\s?(?:%|por cento)", t):
        out.append((m.start(), float(m.group(1).replace(",", "."))))
    return out


def par(t: str, lula: list[float], flavio: list[float], tol: float = 0.5, janela: int = 400):
    """Menor desvio com que o par (Lula, Flavio) aparece proximo no texto; None se nao aparece."""
    nums = numeros(t)
    melhor = None
    for pa, a in nums:
        da = min(abs(a - v) for v in lula)
        if da > 1.0:
            continue
        for pb, b in nums:
            if pb == pa or abs(pb - pa) > janela:
                continue
            db = min(abs(b - v) for v in flavio)
            if db > 1.0:
                continue
            d = max(da, db)
            melhor = d if melhor is None else min(melhor, d)
    return melhor


SEGUNDAS = ["https://revistaforum.com.br/politica/ultimas-pesquisas-primeiro-turno-presidente/"]
_cache: dict[str, str] = {}


def segunda_fonte(r) -> str:
    """Procura o par de valores da pesquisa da vespera em uma fonte diferente da citada pela Wikipedia."""
    for u in SEGUNDAS:
        if u not in _cache:
            nome = hashlib.sha256(u.encode()).hexdigest()[:16] + ".html"
            baixar(u, BRUTOS / "capturas-pesquisas" / nome, pausa=1.0, minimo=3000)
            _cache[u] = texto((BRUTOS / "capturas-pesquisas" / nome).read_bytes().decode("utf-8", "ignore"))
        t = _cache[u]
        i = t.find(r.instituto.split()[0])
        if i >= 0:
            dv = par(t[max(0, i - 200): i + 1500], [r.pct_Lula, r.valido_Lula], [r.pct_Flavio, r.valido_Flavio])
            if dv is not None and dv <= 1.0:
                return u
    return ""


def main() -> None:
    d = pd.read_parquet(DER / "pesquisas_2026.parquet")
    d = d[d.entra & d.cand.isin(["Lula", "Flavio"])]
    p = d.pivot_table(index=["pesquisa", "instituto", "campo_fim", "url", "via"], columns="cand", values=["pct", "valido"], aggfunc="first").reset_index()
    p.columns = ["_".join(c).strip("_") if isinstance(c, tuple) else c for c in p.columns]
    p = p.dropna(subset=["pct_Lula", "pct_Flavio"])
    vesp = p[(p.campo_fim >= date(2026, 9, 28)) & (p.campo_fim <= date(2026, 10, 3))]
    a25 = p[p.via == "fonte_citada_2025"]
    resto = p[(p.via == "registro_tse") & ~p.pesquisa.isin(vesp.pesquisa)]
    amostra = resto.sample(n=min(20, len(resto)), random_state=SEMENTE)
    alvo = pd.concat([vesp.assign(grupo="vespera"), a25.assign(grupo="2025"), amostra.assign(grupo="amostra")]).drop_duplicates("pesquisa")
    linhas = []
    for r in alvo.itertuples():
        url = r.url
        res, motivo = "nao_verificavel", "sem url"
        if isinstance(url, str) and url.startswith("http"):
            nome = hashlib.sha256(url.encode()).hexdigest()[:16] + ".html"
            try:
                baixar(url, BRUTOS / "capturas-pesquisas" / nome, pausa=1.0, tentativas=2, minimo=3000)
                t = texto((BRUTOS / "capturas-pesquisas" / nome).read_bytes().decode("utf-8", "ignore"))
                if "Lula" not in t and "Flávio" not in t and "Flavio" not in t:
                    res, motivo = "nao_verificavel", "pagina sem os nomes"
                else:
                    dv = par(t, [r.pct_Lula, r.valido_Lula], [r.pct_Flavio, r.valido_Flavio])
                    if dv is None:
                        res, motivo = "diverge", "par nao encontrado"
                    elif dv <= 0.5:
                        res, motivo = "confere", f"desvio {dv:.2f}"
                    else:
                        res, motivo = "confere_com_ressalva", f"desvio {dv:.2f}"
            except RuntimeError as e:
                res, motivo = "nao_verificavel", str(e)[:60]
        seg = None
        if r.grupo == "vespera":
            seg = segunda_fonte(r)
        linhas.append({"segunda_fonte": seg, "grupo": r.grupo, "pesquisa": r.pesquisa, "instituto": r.instituto, "campo_fim": r.campo_fim, "lula": r.pct_Lula, "flavio": r.pct_Flavio, "url": url, "resultado": res, "motivo": motivo})
        print(r.grupo, r.instituto, r.campo_fim, res, motivo, flush=True)
    out = pd.DataFrame(linhas)
    tabela("pesq_verificacao", out)
    # aplica a regra: pesquisa de 2025 so fica se a fonte citada confere; vespera sem fonte que confere fica marcada
    ok = out.resultado.isin(["confere", "confere_com_ressalva"])
    sai = set(out[(out.grupo == "2025") & ~ok].pesquisa)
    vesp_ok = set(out[(out.grupo == "vespera") & ok].pesquisa)
    dd = pd.read_parquet(DER / "pesquisas_2026.parquet")
    dd["entra"] = dd.entra & ~dd.pesquisa.isin(sai)
    dd["vespera_verificada"] = dd.pesquisa.isin(vesp_ok)
    dd.to_parquet(DER / "pesquisas_2026.parquet", index=False)
    registrar("b0.pesquisas_na_serie", int(dd[dd.entra].pesquisa.nunique()))
    registrar("b0.cenarios_na_serie", int(dd[dd.entra].cenario.nunique()))
    registrar("b0.pesquisas_2025_removidas_por_nao_conferir", len(sai))
    registrar("b0.vespera_verificadas", len(vesp_ok))
    registrar("b0.vespera_total", int((out.grupo == "vespera").sum()))
    registrar("b0.amostra_divergentes", int(((out.grupo == "amostra") & (out.resultado == "diverge")).sum()))
    registrar("b0.amostra_total", int((out.grupo == "amostra").sum()))
    for g, x in out.groupby("grupo"):
        registrar(f"b0.verificacao.{g}", x.resultado.value_counts().to_dict())


if __name__ == "__main__":
    main()
