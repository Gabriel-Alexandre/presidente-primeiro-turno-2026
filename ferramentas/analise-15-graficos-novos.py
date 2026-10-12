"""Graficos 15 a 20 (emendas 9 e 10): institutos em cinco rodadas, 1o contra 2o turno, precos, bolso e dividas, emprego, sensacao.
1920 x 1080, no mesmo estilo de analise-8-graficos.py, a partir do RESUMO.json e dos CSV (nenhum numero digitado).
"""
from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import matplotlib
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import FIG_VIDEO, RES  # noqa: E402

AZUL, LARANJA, CINZA, ESCURO, VERMELHO = "#1f5fa8", "#d9730d", "#8a8f98", "#1b1f24", "#b3261e"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#555", "axes.labelcolor": ESCURO,
                     "xtick.color": ESCURO, "ytick.color": ESCURO, "font.size": 17})
R = json.load(open(RES / "RESUMO.json", encoding="utf-8"))
vg = lambda x, n=1: f"{x:.{n}f}".replace(".", ",")  # noqa: E731


def fig(titulo, sub="", fonte="", ncols=1, esquerda=0.08):
    f, axs = plt.subplots(1, ncols, figsize=(19.2, 10.8), dpi=100)
    t = textwrap.fill(titulo, 62)
    sb = textwrap.fill(sub, 120) if sub else ""
    f.text(0.07, 0.96, t, fontsize=29, fontweight="bold", color=ESCURO, va="top", linespacing=1.15)
    y = 0.96 - 0.058 * len(t.splitlines()) - 0.01
    if sb:
        f.text(0.07, y, sb, fontsize=18, color="#444", va="top", linespacing=1.2)
        y -= 0.036 * len(sb.splitlines())
    f.subplots_adjust(left=esquerda, right=0.96, top=y - (0.13 if ncols > 1 else 0.04), bottom=0.12, wspace=0.35)
    if fonte:
        f.text(0.07, 0.035, textwrap.fill(fonte, 170), fontsize=13, color="#666")
    return f, axs


def salvar(f, nome):
    FIG_VIDEO.mkdir(parents=True, exist_ok=True)
    f.savefig(FIG_VIDEO / f"{nome}.png", dpi=100)
    plt.close(f)
    print("ok", nome, flush=True)


def g15_institutos():
    e = pd.read_csv(RES / "b6_erro_por_instituto_e_rodada.csv")
    c14 = R["b6"]["contexto_2014"]
    linhas = []
    for r in e.itertuples():
        linhas.append((r.instituto, r.rodada, r.erro))
    for rod, v in c14.items():
        for inst, err in v["por_instituto"].items():
            linhas.append(({"Ibope": "Ipec (antigo Ibope)"}.get(inst, inst), rod, err))
    d = pd.DataFrame(linhas, columns=["instituto", "rodada", "erro"])
    cont = d.groupby("instituto").size()
    d = d[d.instituto.isin(cont[cont >= 3].index)]
    m = d.pivot_table(index="instituto", columns="rodada", values="erro", aggfunc="first")
    cols = ["2014-1", "2014-2", "2018-1", "2018-2", "2022-1", "2022-2", "2026-1"]
    m = m.reindex(columns=cols)
    m = m.loc[m.mean(axis=1).sort_values().index]
    f, ax = fig("Datafolha e Ipec mostraram o candidato contra o PT mais fraco do que a urna em todas as rodadas desde 2014",
                "Erro na diferença entre os dois primeiros (pesquisa menos urna, pontos). Azul: mostrou o candidato contra o PT mais fraco; vermelho: mais forte. Última pesquisa de cada instituto, até 8 dias antes, sem boca de urna",
                "Fontes: Pindograma (pesquisas com registro no TSE) para 2014 a 2022; série de 2026 conferida no registro do TSE e na fonte original (dados/CAPTURAS_INSTITUTOS.csv). 2014: Aécio contra Dilma; 2018 e 2022: Jair Bolsonaro; 2026: Flávio. Só institutos em 3 rodadas ou mais", esquerda=0.17)
    v = np.clip(m.to_numpy(dtype=float), -12, 12)
    im = ax.imshow(v, cmap="RdBu_r", vmin=-12, vmax=12, aspect="auto")
    ax.set_xticks(range(len(cols)), ["2014\n1º turno", "2014\n2º turno", "2018\n1º turno", "2018\n2º turno", "2022\n1º turno", "2022\n2º turno", "2026\n1º turno"], fontsize=15)
    ax.set_yticks(range(len(m)), m.index, fontsize=16)
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            x = m.iat[i, j]
            if x == x:
                ax.text(j, i, f"{x:+.1f}".replace(".", ","), ha="center", va="center", fontsize=14, color="white" if abs(x) > 6 else ESCURO, fontweight="bold")
    for s in ax.spines.values():
        s.set_visible(False)
    salvar(f, "15_institutos_desde_2014")


def g16_turnos():
    pr = R["b6"]["por_rodada"]
    c14 = R["b6"]["contexto_2014"]
    # quanto a URNA deu a mais ao candidato contra o PT do que a pesquisa (mediana dos institutos); positivo = a pesquisa mostrou ele mais fraco
    rod = [("2014-1", -c14["2014-1"]["erro_oposicao_mediano"]), ("2018-1", -pr["2018-1"]["erro_pl_mediano"]), ("2022-1", -pr["2022-1"]["erro_pl_mediano"]),
           ("2026-1", -pr["2026-1"]["erro_pl_mediano"]), ("2014-2", -c14["2014-2"]["erro_oposicao_mediano"]), ("2018-2", -pr["2018-2"]["erro_pl_mediano"]),
           ("2022-2", -pr["2022-2"]["erro_pl_mediano"])]
    f, ax = fig("No 1º turno, a urna deu ao candidato contra o PT de 4 a 7 pontos a mais do que as pesquisas, em quatro eleições seguidas",
                "Quantos pontos a urna deu a mais ao principal candidato contra o PT do que a última pesquisa de cada instituto (mediana dos institutos, votos válidos). No 2º turno o erro quase some",
                "Fontes: Pindograma (2014 a 2022) e série de 2026 do projeto. 2014: Aécio; 2018 e 2022: Jair Bolsonaro; 2026: Flávio Bolsonaro. O voto do candidato do PT, no mesmo período, ficou perto do que as pesquisas mostravam em 2022 e 2026")
    x = np.arange(len(rod))
    vals = [v for _, v in rod]
    cores = [AZUL if v > 0 else VERMELHO for v in vals]
    ax.bar(x, vals, color=cores, width=0.62)
    for i, v in enumerate(vals):
        ax.text(i, v + (0.15 if v >= 0 else -0.15), ("+" if v > 0 else "") + vg(v), ha="center", va="bottom" if v >= 0 else "top", fontsize=22, fontweight="bold")
    ax.axhline(0, color="#555", lw=1.2)
    ax.axvline(3.5, color="#999", ls="--", lw=1.2)
    ax.set_xticks(x, ["2014", "2018", "2022", "2026", "2014", "2018", "2022"], fontsize=18)
    ax.text(1.5, 7.6, "1º TURNO", ha="center", fontsize=22, fontweight="bold", color=ESCURO)
    ax.text(5, 7.6, "2º TURNO", ha="center", fontsize=22, fontweight="bold", color=ESCURO)
    ax.set_ylim(-3.5, 8.5)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: vg(v, 0)))
    ax.set_ylabel("pontos a mais na urna")
    salvar(f, "16_primeiro_e_segundo_turno")


def g17_precos():
    p = R["e14"]["precos"]
    itens = [("Índice geral", "Tudo (IPCA)"), ("Alimentação no domicílio", "Comida em casa"), ("Café moído", "Café"), ("Tomate", "Tomate"), ("Carnes", "Carnes"),
             ("Arroz", "Arroz"), ("Gasolina", "Gasolina"), ("Energia elétrica residencial", "Conta de luz")]
    f, ax = fig("O preço não volta: a inflação desacelerou, mas o que subiu continua mais caro",
                "Quanto cada coisa subiu, somando mês a mês: de outubro de 2022 a setembro de 2026 (azul) e de janeiro de 2020 a setembro de 2026 (cinza)",
                "Fonte: IBGE, IPCA por item (tabela 7060 do SIDRA), acumulado mês a mês. Conferido contra a cesta básica do DIEESE em São Paulo: +20,1% de ago/2022 a ago/2026")
    y = np.arange(len(itens))[::-1]
    a = [p[k]["desde_out22"] for k, _ in itens]
    b = [p[k]["desde_jan20"] if p[k]["desde_jan20"] is not None else np.nan for k, _ in itens]
    ax.barh(y + 0.2, b, height=0.38, color="#c5cad3", label="desde jan/2020")
    ax.barh(y - 0.2, a, height=0.38, color=AZUL, label="desde out/2022")
    for yy, v in zip(y, a):
        ax.text(v + 2, yy - 0.2, f"+{vg(v, 0)}%", va="center", fontsize=17, fontweight="bold", color=AZUL)
    for yy, v in zip(y, b):
        if v == v:
            ax.text(v + 2, yy + 0.2, f"+{vg(v, 0)}%", va="center", fontsize=15, color="#555")
    ax.set_yticks(y, [n for _, n in itens], fontsize=19)
    ax.set_xlabel("alta acumulada (%)")
    ax.legend(loc="lower right", frameon=False, fontsize=17)
    salvar(f, "17_precos_desde_2022_e_2020")


def g18_bolso():
    d = R["e14"]
    f, axs = fig("O emprego melhorou, mas a dívida chegou ao maior nível desde 2005",
                 "Quatro números de quatro fontes diferentes, em 2022 e em 2026",
                 "Fontes: IBGE (PNAD, ocupados no 2º trimestre); Serasa (pessoas com nome sujo: mai/2022 e ago/2026; empresas em recuperação judicial: 2022 pela conta das altas publicadas e 2025 publicado); Banco Central (série 29034, parte da renda das famílias que vai para pagar dívida, set/2022 e jul/2026, a maior desde 2005)", ncols=4)
    blocos = [("Pessoas trabalhando\n(milhões)", d["emprego"]["ocupados_mil_2t22"] / 1000, d["emprego"]["ocupados_mil_2t26"] / 1000, "#2e7d32"),
              ("Pessoas com\nnome sujo (milhões)", d["dividas"]["nome_sujo_mi_mai22"], d["dividas"]["nome_sujo_mi_ago26"], VERMELHO),
              ("Empresas em\nrecuperação judicial", d["empresas"]["recuperacao_judicial_empresas"]["2022"], d["empresas"]["recuperacao_judicial_empresas"]["2025"], VERMELHO),
              ("Parte da renda que vai\npara pagar dívida (%)", d["dividas"]["comprometimento_set22"], d["dividas"]["comprometimento_ultimo"], VERMELHO)]
    for ax, (tit, a, b, cor) in zip(axs, blocos):
        ax.bar([0, 1], [a, b], color=["#c5cad3", cor], width=0.6)
        for i, v in enumerate((a, b)):
            ax.text(i, v * 1.02, vg(v, 1) if v < 200 else f"{v:,.0f}".replace(",", "."), ha="center", va="bottom", fontsize=20, fontweight="bold")
        ax.set_xticks([0, 1], ["2022", "2025/26"], fontsize=17)
        ax.set_title(tit, fontsize=19, fontweight="bold", pad=14)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.set_ylim(0, max(a, b) * 1.22)
    salvar(f, "18_emprego_e_dividas")


def g19_sensacao():
    s = R["e14"]["sensacao"]
    f, ax = fig("A maioria sentia o contrário do índice: o dobro dizia que a economia piorou",
                "Genial/Quaest, junho de 2026: a economia do Brasil nos últimos 12 meses, e o preço da comida",
                "Fonte: Genial/Quaest, 5 a 8 de junho de 2026, 2.004 entrevistas presenciais, registro BR-07661/2026 (InfoMoney, 10/06/2026). Em 2025 a mesma pergunta chegou a 56% de piorou")
    cats = ["piorou", "melhorou"]
    vals = [s["quaest_jun26_piorou"], s["quaest_jun26_melhorou"]]
    ax.barh([1.6, 0.8], vals, color=[VERMELHO, "#2e7d32"], height=0.6)
    ax.barh([-0.4], [s["quaest_jun26_comida_subiu"]], color=VERMELHO, height=0.6)
    for yy, v in zip([1.6, 0.8, -0.4], vals + [s["quaest_jun26_comida_subiu"]]):
        ax.text(v + 1, yy, f"{v}%", va="center", fontsize=24, fontweight="bold")
    ax.set_yticks([1.6, 0.8, -0.4], ["a economia piorou", "a economia melhorou", "o preço da comida subiu"], fontsize=21)
    ax.set_xlim(0, 100)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    salvar(f, "19_sensacao_economia")


if __name__ == "__main__":
    g15_institutos()
    g16_turnos()
    g17_precos()
    g18_bolso()
    g19_sensacao()
