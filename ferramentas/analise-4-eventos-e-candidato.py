"""H4 (eventos e episodios dos dois lados) e H11 (por que Flavio e nao outro nome da direita).

H4, regra do pre-registro (secao 5): por instituto com 8 ou mais rodadas na serie Lula x Flavio (dez/2025 em diante), a mudanca da margem
entre a ultima pesquisa antes e a primeira depois do evento (ou do grupo de eventos a menos de 30 dias um do outro), se a distancia for de
ate 45 dias e o cenario tiver o mesmo numero de candidatos. Movimento normal = percentil 95 do valor absoluto das mudancas entre rodadas
seguidas do mesmo instituto FORA das janelas de evento (7 dias antes a 21 depois de qualquer evento confirmado). Coincide com movimento se
a mudanca passa do normal em 2 ou mais institutos, no mesmo sentido.
Eventos de 2025 (V01 a V04) nao entram: nao ha serie de avaliacao do governo com 8 rodadas (condicao da secao 10) e a serie de 2025 sem Flavio
nao foi verificada na fonte (emenda 1). Ficam como 'nao testavel'.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import DADOS, DER, RES, verificar_fontes  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402

spec = importlib.util.spec_from_file_location("a3", Path(__file__).resolve().parent / "analise-3-pesquisas.py")
a3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a3)

INICIO_SERIE = pd.Timestamp("2025-12-01")
MIN_RODADAS = 8
MAX_DIAS = 45


def eventos() -> pd.DataFrame:
    e = pd.read_csv(DADOS / "eventos_confirmados.csv", dtype=str)
    e = e[e.confirmado.astype(str).str.lower() == "true"].copy()
    e["data"] = pd.to_datetime(e.data_confirmada)
    return e.sort_values("data").reset_index(drop=True)


def grupos(e: pd.DataFrame) -> list[dict]:
    """Eventos a menos de 30 dias um do outro viram um grupo. Direcao so existe se todos os alvos do grupo forem iguais."""
    out, cur = [], []
    for r in e.itertuples():
        if cur and (r.data - cur[-1].data).days >= 30:
            out.append(cur)
            cur = []
        cur.append(r)
    if cur:
        out.append(cur)
    res = []
    for g in out:
        alvos = {r.alvo for r in g}
        direcao = None
        if alvos == {"lula_governo"}:
            direcao = +1  # esperado: margem Flavio menos Lula sobe
        elif alvos == {"flavio_oposicao"}:
            direcao = -1
        res.append({"ids": [r.id for r in g], "ini": g[0].data, "fim": g[-1].data, "alvos": sorted(alvos), "direcao": direcao,
                    "descricao": " + ".join(f"{r.id}" for r in g)})
    return res


def var_margem(r) -> float:
    """Variancia amostral da margem (Flavio menos Lula, em pontos^2) de uma pesquisa: (pF + pL - (pF - pL)^2) / n, com pF e pL em proporcao da amostra."""
    n = r.amostra if getattr(r, "amostra", None) and r.amostra == r.amostra else 2000
    pf, pl = r.pct_Flavio / 100, r.pct_Lula / 100
    return 1e4 * (pf + pl - (pf - pl) ** 2) / n


def main() -> None:
    verificar_fontes()
    p = a3.melhor_cenario()
    p = p[p.campo_fim >= INICIO_SERIE].copy()
    am = pd.read_parquet(DER / "pesquisas_2026.parquet")[["pesquisa", "amostra"]].drop_duplicates("pesquisa")
    p = p.merge(am, on="pesquisa", how="left")
    ev = eventos()
    ev26 = ev[(ev.data >= INICIO_SERIE) & (ev.tipo == "exposicao")]
    nao_test = ev[(ev.data < INICIO_SERIE) & (ev.tipo == "exposicao")]
    registrar("h4.exposicoes_de_2025_nao_testaveis", sorted(nao_test.id.tolist()))
    janelas = [(r.data - timedelta(days=7), r.data + timedelta(days=21)) for r in ev.itertuples()]
    por_inst = p.groupby("instituto").size()
    institutos = por_inst[por_inst >= MIN_RODADAS].index.tolist()
    registrar("h4.institutos_com_8_ou_mais_rodadas", {k: int(por_inst[k]) for k in institutos})
    normal, difs_fora = {}, {}
    for nome in institutos:
        g = p[p.instituto == nome].sort_values("campo_fim")
        d = []
        for a, b in zip(g.itertuples(), g.iloc[1:].itertuples()):
            if a.n != b.n:
                continue
            meio = a.campo_fim + (b.campo_fim - a.campo_fim) / 2
            if any(j0 <= meio <= j1 for j0, j1 in janelas):
                continue
            d.append(abs(b.margem - a.margem))
        difs_fora[nome] = d
        normal[nome] = float(np.percentile(d, 95)) if len(d) >= 2 else np.nan  # regra literal do pre-registro: p95 das variacoes disponiveis
    pool = [x for k in institutos for x in difs_fora[k]]
    p95_pool = float(np.percentile(pool, 95)) if len(pool) >= 4 else np.nan
    registrar("h4.sensibilidade.p95_agrupado_pontos", p95_pool)
    registrar("h4.sensibilidade.variacoes_fora_das_janelas", len(pool))
    tabela("h4_movimento_normal", pd.DataFrame([{"instituto": k, "rodadas": int(por_inst[k]), "mudancas_fora_das_janelas": len(difs_fora[k]), "p95_normal": normal[k]} for k in institutos]))
    linhas = []
    gr = grupos(ev26)
    for g in gr:
        for nome in institutos:
            q = p[p.instituto == nome].sort_values("campo_fim")
            antes = q[q.campo_fim < g["ini"]]
            depois = q[q.campo_fim > g["fim"]]
            if antes.empty or depois.empty:
                continue
            a, b = antes.iloc[-1], depois.iloc[0]
            dist = (b.campo_fim - a.campo_fim).days
            if dist > MAX_DIAS or a.n != b.n:
                continue
            delta = b.margem - a.margem
            linhas.append({"grupo": g["descricao"], "ids": ",".join(g["ids"]), "instituto": nome, "antes": a.campo_fim.date(), "depois": b.campo_fim.date(), "dias": dist, "n_cand": int(a.n),
                           "margem_antes": a.margem, "margem_depois": b.margem, "delta": delta, "normal": normal[nome], "passa_do_normal": bool(abs(delta) > normal[nome]) if not np.isnan(normal[nome]) else False,
                           "passa_p95_agrupado": bool(abs(delta) > p95_pool) if not np.isnan(p95_pool) else False,
                           "limiar_amostral": 1.96 * 1.5 ** 0.5 * float(np.sqrt(var_margem(a) + var_margem(b)))})
    t_ = None
    t = pd.DataFrame(linhas)
    tabela("h4_eventos_por_instituto", t)
    resumo = []
    for g in gr:
        x = t[t.grupo == g["descricao"]] if len(t) else t
        if x.empty:
            resumo.append({"grupo": g["descricao"], "ids": ",".join(g["ids"]), "alvos": "+".join(g["alvos"]), "institutos_testados": 0, "coincide_com_movimento": False, "sentido": "", "mediana_delta": np.nan, "tamanho_pontos": np.nan, "leitura": "nao testavel (menos de 2 institutos com par antes e depois em ate 45 dias)"})
            continue
        passam = x[x.passa_do_normal]
        passam_pool = x[x.passa_p95_agrupado]
        passam_amost = x[x.delta.abs() > x.limiar_amostral]
        sinais = np.sign(passam.delta)
        mesmo = len(passam) >= 2 and (sinais == sinais.iloc[0]).sum() >= 2
        sentido = "sobe (Flavio melhora)" if mesmo and sinais.iloc[0] > 0 else ("desce (Lula melhora)" if mesmo else "")
        coincide = bool(mesmo and (sinais == sinais.mode().iloc[0]).sum() >= 2)
        esperado = g["direcao"]
        compat = (esperado is None) or (coincide and np.sign(passam.delta.median()) == esperado)
        leitura = ("nao testavel" if len(x) < 2 else
                   ("a serie nao se moveu alem do normal" if not coincide else
                    ("coincide com movimento no sentido esperado pelo alvo" if (esperado is not None and compat) else
                     ("coincide com movimento no sentido contrario ao esperado pelo alvo" if esperado is not None else "coincide com movimento (alvo dos dois lados: sem sentido esperado)"))))
        resumo.append({"grupo": g["descricao"], "ids": ",".join(g["ids"]), "alvos": "+".join(g["alvos"]), "institutos_testados": int(len(x)), "institutos_acima_do_normal": int(len(passam)), "institutos_acima_p95_agrupado": int(len(passam_pool)), "institutos_acima_limiar_amostral": int(len(passam_amost)),
                       "coincide_com_movimento": coincide, "sentido": sentido, "mediana_delta": float(x.delta.median()), "tamanho_pontos": float(abs(passam.delta.median())) if coincide else 0.0, "leitura": leitura})
    r = pd.DataFrame(resumo)
    tabela("h4_resumo_por_grupo", r)
    registrar("h4.grupos", [{k: (None if (isinstance(v, float) and v != v) else v) for k, v in x.items()} for x in r.to_dict("records")])
    registrar("h4.grupos_que_coincidem_com_movimento", int(r.coincide_com_movimento.sum()))
    registrar("h4.grupos_testaveis", int((r.institutos_testados >= 2).sum()))
    registrar("h4.tamanho_soma_movimentos_acima_do_normal_pontos", float(r.tamanho_pontos.fillna(0).sum()))
    print(r.to_string())


if __name__ == "__main__":
    main()
