"""H11: por que o Flavio e nao outro nome da direita.

Em cada pesquisa da serie, compara a margem 'candidato menos Lula' (em validos) de cada outro nome (Tarcisio, Ratinho, Zema, Caiado, Leite)
no cenario SEM Flavio com a margem 'Flavio menos Lula' no cenario COM Flavio da MESMA pesquisa. Diferenca = margem_X - margem_Flavio:
positiva = o outro nome rendia mais que Flavio. Cenarios com diferenca de mais de 1 candidato no tamanho ficam fora.
Interpretacao fixada no pre-registro: rende mais de forma estavel em 2 ou mais institutos = ha algo no candidato; ate 1,5 ponto de diferenca =
o fator e o campo; rende menos = o fator esta fora do candidato.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import DER, verificar_fontes  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402

OUTROS = ["Tarcisio", "Ratinho", "Zema", "Caiado", "Leite", "Ciro"]
TOL = 1.5


def main() -> None:
    verificar_fontes()
    d = pd.read_parquet(DER / "pesquisas_2026.parquet")
    d["campo_fim"] = pd.to_datetime(d.campo_fim)
    ok = d.groupby("pesquisa").entra.transform("any")
    d = d[ok]
    # candidatos por cenario
    cen = d.groupby("cenario").agg(pesquisa=("pesquisa", "first"), instituto=("instituto", "first"), campo_fim=("campo_fim", "first"), n=("cand", "nunique"), conj=("cand", lambda s: set(s)))
    linhas = []
    for pesq, g in cen.groupby("pesquisa"):
        com_f = g[g.conj.apply(lambda s: {"Lula", "Flavio"} <= s)]
        if com_f.empty:
            continue
        for x in OUTROS:
            sem_f = g[g.conj.apply(lambda s: {"Lula", x} <= s and "Flavio" not in s)]
            if sem_f.empty:
                continue
            # cenario com Flavio de tamanho mais proximo
            for cx in sem_f.itertuples():
                cf = com_f.iloc[(com_f.n - cx.n).abs().argsort()].iloc[0]
                if abs(cf.n - cx.n) > 1:
                    continue
                vf = d[(d.cenario == cf.name)].set_index("cand").valido
                vx = d[(d.cenario == cx.Index)].set_index("cand").valido
                m_f = vf["Flavio"] - vf["Lula"]
                m_x = vx[x] - vx["Lula"]
                linhas.append({"pesquisa": pesq, "instituto": cx.instituto, "campo_fim": cx.campo_fim, "outro": x, "n_cenario_outro": cx.n, "n_cenario_flavio": cf.n,
                               "margem_outro": m_x, "margem_flavio": m_f, "dif": m_x - m_f})
    t = pd.DataFrame(linhas)
    t["trimestre"] = t.campo_fim.dt.to_period("Q").astype(str)
    tabela("h11_pares", t)
    resumo = []
    for (x, tri), g in t.groupby(["outro", "trimestre"]):
        por_inst = g.groupby("instituto").dif.mean()
        resumo.append({"outro": x, "trimestre": tri, "pares": len(g), "institutos": int(g.instituto.nunique()), "dif_media": float(g.dif.mean()), "dif_mediana": float(g.dif.median()),
                       "institutos_com_dif_maior_que_tolerancia": int((por_inst > TOL).sum()), "institutos_com_dif_menor_que_menos_tolerancia": int((por_inst < -TOL).sum())})
    r = pd.DataFrame(resumo)
    def leitura(x):
        if x.institutos < 2:
            return "nao testavel (menos de 2 institutos)"
        if x.institutos_com_dif_maior_que_tolerancia >= 2:
            return "rende mais que Flavio"
        if x.institutos_com_dif_menor_que_menos_tolerancia >= 2:
            return "rende menos que Flavio"
        return "o mesmo (dentro de 1,5 ponto) ou sem consenso"
    r["leitura"] = r.apply(leitura, axis=1)
    tabela("h11_resumo", r)
    registrar("h11.pares", int(len(t)))
    registrar("h11.por_nome_e_trimestre", r.to_dict("records"))
    print(r.round(2).to_string())


if __name__ == "__main__":
    main()
