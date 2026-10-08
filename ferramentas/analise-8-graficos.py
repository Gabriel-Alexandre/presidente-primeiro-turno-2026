"""Graficos do relatorio e do video: 1920 x 1080, gerados dos CSV e do RESUMO.json (nenhum numero digitado).

Cores: azul = candidato do partido de Bolsonaro; laranja = candidato do PT; cinza = os demais. Escolha por contraste e daltonismo, nao por simbolo.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import CONGRESSO, DER, FIG_VIDEO, RES  # noqa: E402

AZUL, LARANJA, CINZA, ESCURO, CLARO = "#1f5fa8", "#d9730d", "#8a8f98", "#1b1f24", "#eef0f3"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#555", "axes.labelcolor": ESCURO,
                     "xtick.color": ESCURO, "ytick.color": ESCURO, "font.size": 17, "axes.titlesize": 26, "axes.titleweight": "bold"})
R = json.load(open(RES / "RESUMO.json", encoding="utf-8"))


def fig(titulo: str, sub: str = "", fonte: str = ""):
    import textwrap
    f, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    t = textwrap.fill(titulo, 62)
    sb = textwrap.fill(sub, 120) if sub else ""
    nt, ns = len(t.splitlines()), (len(sb.splitlines()) if sb else 0)
    topo = 0.96
    f.text(0.07, topo, t, fontsize=29, fontweight="bold", color=ESCURO, va="top", linespacing=1.15)
    y = topo - 0.058 * nt - 0.01
    if sb:
        f.text(0.07, y, sb, fontsize=18, color="#444", va="top", linespacing=1.2)
        y -= 0.036 * ns
    f.subplots_adjust(left=0.08, right=0.96, top=y - 0.03, bottom=0.12)
    if fonte:
        f.text(0.07, 0.035, textwrap.fill(fonte, 170), fontsize=13, color="#666")
    return f, ax


def salvar(f, nome: str) -> None:
    FIG_VIDEO.mkdir(parents=True, exist_ok=True)
    f.savefig(FIG_VIDEO / f"{nome}.png", dpi=100)
    plt.close(f)
    print("ok", nome, flush=True)


def g01():
    t = pd.read_csv(RES / "a1_nacional.csv")
    pl = {2018: "jair", 2022: "jair", 2026: "flavio"}
    pt = {2018: "haddad", 2022: "lula", 2026: "lula"}
    nomes = {2018: ("Jair Bolsonaro", "Haddad"), 2022: ("Jair Bolsonaro", "Lula"), 2026: ("Flávio Bolsonaro", "Lula")}
    f, ax = fig("O candidato do PL passou de 43,2% para 47,0% e Lula caiu de 48,4% para 45,2%", "1º turno de presidente, percentual dos votos válidos", "Fonte: boletins de urna (projeto da apuração), conferidos contra o resultado oficial do TSE")
    x = np.arange(3)
    for i, a in enumerate((2018, 2022, 2026)):
        p = t[(t.ano == a) & (t.candidato == pl[a])].pct_validos.iloc[0]
        l = t[(t.ano == a) & (t.candidato == pt[a])].pct_validos.iloc[0]
        o = 100 - p - l
        for k, (v, c) in enumerate(((p, AZUL), (l, LARANJA), (o, CINZA))):
            ax.bar(i + (k - 1) * 0.27, v, 0.25, color=c)
            ax.text(i + (k - 1) * 0.27, v + 0.8, f"{v:.1f}%".replace(".", ","), ha="center", fontsize=19, fontweight="bold")
        ax.text(i - 0.27, -4.2, nomes[a][0], ha="center", fontsize=14)
        ax.text(i, -4.2, nomes[a][1], ha="center", fontsize=14)
        ax.text(i + 0.27, -4.2, "outros", ha="center", fontsize=14)
    ax.set_xticks(x, ["2018", "2022", "2026"], fontsize=22)
    ax.set_ylim(0, 58)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    salvar(f, "01_resultado_nacional")


def g02():
    t = pd.read_csv(RES / "a2_regiao.csv").sort_values("contribuicao")
    f, ax = fig(f"A virada de {R['a1']['virada_2022_2026']:.1f} pontos veio de todas as regiões".replace(".", ","), "Contribuição de cada região para a mudança da margem entre os dois primeiros (pontos percentuais) e % da virada", "Decomposição exata por deslocamento e participação (docs/PRE_REGISTRO.md, A2)")
    cores = [AZUL] * len(t)
    ax.barh(t.regiao, t.contribuicao, color=cores)
    for i, r in enumerate(t.itertuples()):
        ax.text(r.contribuicao + 0.04, i, f"{r.contribuicao:.2f}".replace(".", ",") + f"  ({r.pct_da_virada:.0f}%)", va="center", fontsize=20, fontweight="bold")
    ax.set_xlim(0, t.contribuicao.max() * 1.35)
    ax.tick_params(axis="y", labelsize=22)
    ax.set_xlabel("pontos de margem")
    salvar(f, "02_virada_por_regiao")


def g03():
    t = pd.read_csv(RES / "a1_uf.csv").sort_values("virada_2022_2026")
    f, ax = fig("A margem andou a favor do candidato do PL em quase todos os estados", "Virada de 2022 para 2026 por UF (pontos de margem; positivo = mais favorável ao candidato do PL)", "Margem = candidato do PL menos Lula, em pontos dos votos válidos")
    cores = [AZUL if v > 0 else LARANJA for v in t.virada_2022_2026]
    ax.barh(t.uf, t.virada_2022_2026, color=cores)
    ax.tick_params(axis="y", labelsize=14)
    ax.axvline(0, color="#333", lw=1)
    ax.set_xlabel("pontos de margem")
    salvar(f, "03_virada_por_uf")


def g04():
    t = pd.read_csv(RES / "a3_decomposicao.csv")
    f, axs = plt.subplots(1, 2, figsize=(19.2, 10.8), dpi=100)
    f.subplots_adjust(left=0.07, right=0.97, top=0.78, bottom=0.14, wspace=0.18)
    f.text(0.07, 0.95, "Quase todo o ganho foi troca de voto, não comparecimento", fontsize=29, fontweight="bold", va="top")
    f.text(0.07, 0.885, "Variação de votos de 2022 para 2026 decomposta em quatro termos (milhares de votos, soma exata por município)", fontsize=19, color="#444", va="top")
    f.text(0.07, 0.04, "Ordem: eleitorado apto, comparecimento, fração de válidos, parcela do candidato (a outra ordem está em resultados/a3_decomposicao.csv)", fontsize=14, color="#666")
    rot = {"apto": "Eleitorado\napto", "comparecimento": "Compare-\ncimento", "validos": "Fração de\nválidos", "parcela": "Troca de\nvoto"}
    for ax, c, cor, nome in ((axs[0], "pl", AZUL, "Candidato do PL"), (axs[1], "pt", LARANJA, "Candidato do PT")):
        x = t[t.candidato == c].set_index("termo")
        ordem = ["apto", "comparecimento", "validos", "parcela"]
        v = [x.loc[k, "votos_ordem_a"] / 1000 for k in ordem]
        ax.bar([rot[k] for k in ordem], v, color=cor)
        for i, val in enumerate(v):
            ax.text(i, val + (60 if val >= 0 else -190), f"{val:,.0f}".replace(",", "."), ha="center", fontsize=18, fontweight="bold")
        ax.axhline(0, color="#333", lw=1)
        ax.set_title(f"{nome}: {x.loc['total', 'votos_ordem_a'] / 1000:,.0f} mil votos".replace(",", "."), fontsize=22)
        ax.set_ylim(-5000, 5400)
        ax.spines["left"].set_visible(False)
        ax.set_yticks([])
    salvar(f, "04_decomposicao_dos_votos")


def g05():
    t = pd.read_csv(RES / "a4_matriz_transicao.csv")
    t = t[(t.spec == "enxuto") & (t.ajuste == "nacional")]
    est = pd.read_csv(RES / "a4_estabilidade.csv")
    robustos = {(r.origem, r.destino) for r in est.itertuples() if r.robusto}
    om = ["lula22", "jair22", "terceiros22", "bn22", "abst22"]
    dm = ["flavio26", "lula26", "caiado26", "cury26", "renan26", "zema26", "outros26", "bn26", "abst26"]
    on = ["Lula", "Jair", "Ciro, Tebet e outros", "Branco/nulo", "Abstenção"]
    dn = ["Flávio", "Lula", "Caiado", "Cury", "Renan", "Zema", "Outros", "Branco/nulo", "Abstenção"]
    M = t.pivot(index="origem", columns="destino", values="B").loc[om, dm].to_numpy()
    f, ax = fig("Para onde foi o voto de 2022 (estimativa ecológica)", "De cada 100 eleitores de 2022 (linhas), quantos aparecem em cada destino de 2026 (colunas). Inferência entre lugares, não o voto de ninguém. Em preto, fluxos estáveis entre regiões e especificações; em cinza, fluxos que variam demais e não entram nas conclusões", "Regressão ecológica com restrições, 5.570 municípios, 300 reamostragens. Estável = as duas especificações diferem em até 3 pontos e a amplitude entre as cinco regiões é de até 15 (resultados/a4_estabilidade.csv)")
    ax.imshow(M, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(9), dn, rotation=25, ha="right", fontsize=16)
    ax.set_yticks(range(5), on, fontsize=18)
    for i in range(5):
        for j in range(9):
            if M[i, j] >= 0.005:
                ok = (om[i], dm[j]) in robustos
                ax.text(j, i, f"{100 * M[i, j]:.0f}", ha="center", va="center", fontsize=18 if ok else 15, color=("white" if M[i, j] > 0.5 else ESCURO) if ok else ("#c9ced6" if M[i, j] > 0.5 else "#7a7f87"), fontweight="bold" if ok else "normal")
    ax.spines[:].set_visible(False)
    f.subplots_adjust(bottom=0.2)
    salvar(f, "05_transicao_2022_2026")


def g06(p: pd.DataFrame):
    w = pd.read_csv(RES / "b1_semanal_2026.csv", parse_dates=["semana"])
    f, ax = fig("As pesquisas mostraram Lula à frente até a última semana; a urna deu o contrário", "Média semanal das pesquisas, margem do candidato do PL menos Lula nos votos válidos (cada instituto corrigido pelo próprio desvio médio)", "Fontes: pesquisas registradas no TSE, conferidas na fonte citada (docs/PRE_REGISTRO.md, B1). Linha tracejada: resultado da urna")
    ax.plot(w.semana, w.margem_flavio_menos_lula, color=AZUL, lw=4)
    ax.scatter(w.semana, w.margem_flavio_menos_lula, s=w.pesquisas * 8, color=AZUL, alpha=0.5)
    ax.axhline(R["a1"]["margem_2026"], color=ESCURO, ls="--", lw=2)
    ax.text(w.semana.iloc[0], R["a1"]["margem_2026"] + 1, f"urna: {R['a1']['margem_2026']:+.1f} pontos".replace(".", ","), fontsize=18)
    ax.axhline(0, color="#999", lw=1)
    for d, rot, y in (("2026-05-13", "13/05: mensagens\nFlávio-Vorcaro", -24), ("2026-07-30", "30/07: STF autoriza\ninvestigar Lulinha", -18), ("2026-09-01", "set: crise do STF,\ndebates cancelados", -24)):
        ax.axvline(pd.Timestamp(d), color="#aaa", lw=1.5, ls=":")
        ax.text(pd.Timestamp(d), y, rot, fontsize=14, ha="center", color="#444")
    ax.set_ylabel("margem em pontos (positivo = candidato do PL à frente)")
    ax.set_ylim(-28, 6)
    salvar(f, "06_trajetoria_pesquisas_2026")


def g07():
    from importlib import util
    spec = util.spec_from_file_location("a3", Path(__file__).resolve().parent / "analise-3-pesquisas.py")
    a3 = util.module_from_spec(spec)
    spec.loader.exec_module(a3)
    p26 = a3.melhor_cenario()
    p26["dias"] = (pd.Timestamp("2026-10-04") - p26.campo_fim).dt.days
    p22 = a3.pindograma_2022()
    p22["dias"] = (pd.Timestamp("2022-10-02") - p22.fim).dt.days
    f, ax = fig("Nos dois anos a média das pesquisas terminou abaixo do resultado do candidato do PL", "Margem média semanal das pesquisas (candidato do PL menos Lula, votos válidos) por dias até a eleição, e resultado da urna", "Fontes: pesquisas de 2026 (Wikipédia casada com o registro do TSE) e de 2022 (Pindograma). Médias simples, sem correção de instituto")
    for p, c, nome, urna in ((p22, CINZA, "2022 (Jair)", R["a1"]["margem_2022"]), (p26, AZUL, "2026 (Flávio)", R["a1"]["margem_2026"])):
        q = p[(p.dias <= 240) & (p.dias >= 0)].copy()
        q["sem"] = (q.dias // 7)
        g = q.groupby("sem").margem.mean()
        ax.plot(-(g.index * 7), g.values, color=c, lw=4, label=nome)
        ax.scatter([0], [urna], color=c, s=260, marker="D", zorder=5)
        ax.text(-3, urna + (1.2 if c == AZUL else -2.8), f"urna {nome.split()[0]}: {urna:+.1f}".replace(".", ","), fontsize=16, ha="right", color=c, fontweight="bold", bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))
    ax.axhline(0, color="#999", lw=1)
    ax.set_xlabel("dias até o 1º turno")
    ax.set_ylabel("margem (pontos)")
    ax.legend(fontsize=20, loc="lower left", frameon=False)
    salvar(f, "07_trajetoria_2022_2026")


def g08():
    e = pd.read_csv(RES / "b2_erro_por_instituto.csv")
    e = e[e.verificada]
    f, ax = fig("As pesquisas subestimaram o candidato do PL em 2022 e em 2026, e o erro típico foi parecido", "Erro da margem na última pesquisa de cada instituto (pesquisa menos urna, pontos; negativo = mostrou o candidato do PL pior do que foi). Barra preta: mediana; losango: média", "Cada ponto é um instituto. 2018: Datafolha e outros; 2022 e 2026: institutos com pesquisa na véspera (2026: só as verificadas na fonte). Em 2022 dois institutos muito fora da curva puxam a média para cima")
    rng = np.random.default_rng(1)
    for i, a in enumerate((2018, 2022, 2026)):
        x = e[e.ano == a]
        ax.scatter(i + rng.uniform(-0.12, 0.12, len(x)), x.erro_margem, s=190, color=[CINZA, CINZA, AZUL][i], alpha=0.8, edgecolor="white")
        ax.hlines(x.erro_margem.median(), i - 0.25, i + 0.25, color=ESCURO, lw=4)
        ax.scatter([i], [x.erro_margem.mean()], marker="D", s=170, color="white", edgecolor=ESCURO, linewidth=2.5, zorder=4)
        ax.text(i + 0.3, x.erro_margem.median(), f"mediana {x.erro_margem.median():+.1f}\nmédia {x.erro_margem.mean():+.1f}".replace(".", ","), va="center", fontsize=19, fontweight="bold")
    ax.axhline(0, color="#666", lw=1.5)
    ax.set_xlim(-0.5, 2.9)
    ax.set_xticks(range(3), ["2018", "2022", "2026"], fontsize=22)
    ax.set_ylabel("erro da margem (pontos)")
    salvar(f, "08_erro_dos_institutos")


def g09():
    t = pd.read_csv(RES / "b3_ultimos_21_dias.csv", parse_dates=["campo_fim"])
    f, ax = fig("Nas três últimas semanas os outros candidatos encolheram em todos os institutos", "Parcela dos votos válidos que não é de Lula nem de Flávio, por pesquisa (pontos percentuais)", "Fonte: pesquisas verificadas; valores válidos calculados dos brutos. Urna: 7,8%")
    cores = {"AtlasIntel": "#1f5fa8", "Datafolha": "#d9730d", "Futura": "#2a9d8f", "Palver": "#9b5de5", "Quaest": "#e63946"}
    for nome, g in t.groupby("instituto"):
        ax.plot(g.campo_fim, g.outros_valido, marker="o", lw=3, ms=9, color=cores.get(nome, CINZA), label=nome)
    ax.axhline(100 - R["a1"]["pl_pct_2026"] - R["a1"]["pt_pct_2026"], color=ESCURO, ls="--", lw=2)
    ax.text(t.campo_fim.min(), 100 - R["a1"]["pl_pct_2026"] - R["a1"]["pt_pct_2026"] + 0.4, "urna", fontsize=18)
    ax.legend(fontsize=18, frameon=False, ncol=3, loc="upper right")
    ax.set_ylabel("outros candidatos (%)")
    salvar(f, "09_outros_nas_ultimas_semanas")


def g10():
    t = pd.read_csv(RES / "h4_eventos_por_instituto.csv")
    f, ax = fig("Episódios dos dois lados: o que moveu a série e o que não moveu", "Mudança da margem (candidato do PL menos Lula) entre a última pesquisa antes e a primeira depois, por instituto (pontos)", "Cada ponto é um instituto; a barra preta é a mediana. Movimento acima do normal exige 2 ou mais institutos no mesmo sentido (docs/PRE_REGISTRO.md, §5)")
    grupos = [("V17", "13/05\nMensagens\nFlávio-Vorcaro"), ("V19", "30/07\nSTF autoriza investigar\nLulinha"), ("V09,V21,V23,V26,V27", "Setembro\n(crise do STF,\ndebates, N. Sra.\nAparecida)")]
    rng = np.random.default_rng(2)
    for i, (ids, rot) in enumerate(grupos):
        x = t[t.ids == ids]
        ax.scatter(i + rng.uniform(-0.1, 0.1, len(x)), x.delta, s=220, color=np.where(x.passa_do_normal, AZUL, CINZA), edgecolor="white", zorder=3)
        ax.hlines(x.delta.median(), i - 0.25, i + 0.25, color=ESCURO, lw=4)
        ax.text(i + 0.28, x.delta.median(), f"mediana {x.delta.median():+.1f}".replace(".", ","), va="center", fontsize=18, fontweight="bold")
    ax.axhline(0, color="#666", lw=1.5)
    f.subplots_adjust(bottom=0.2)
    ax.set_xlim(-0.5, 2.75)
    ax.set_xticks(range(3), [g[1] for g in grupos], fontsize=17)
    ax.set_ylabel("mudança da margem (pontos)\nnegativo = Lula melhora")
    ax.text(2.4, ax.get_ylim()[1] * 0.95, "azul: acima do\nmovimento normal\ndo instituto", fontsize=15, ha="right", va="top", color=AZUL)
    salvar(f, "10_episodios_e_series")


def g11():
    h8 = R["h8"]["evangelicos_por_dp"]
    h13 = R["h13"]
    f, ax = fig("Por lugar: o que se associa à virada municipal, e o que o placebo de 2018 a 2022 mostra", "Coeficiente por desvio-padrão do preditor, em pontos de margem, com intervalo de 95% (erro agrupado por UF, efeito fixo de UF)", "Placebo: a mesma regressão sobre a virada de 2018 para 2022. Associação entre municípios, não entre pessoas")
    linhas = [("Evangélicos (% do município)", h8), ("Mais eleitores com 60+ (variação)", h13["60_mais_por_dp"]), ("Mais jovens de 16 a 24 (variação)", h13["jovens_16_a_24_por_dp"]), ("Mais ensino superior (variação)", h13["superior_por_dp"])]
    for i, (nome, r) in enumerate(linhas[::-1]):
        for k, (chave, cor, off) in enumerate((("principal", AZUL, 0.12), ("placebo_2018_2022", CINZA, -0.12))):
            c, se = r[chave]["coef"], r[chave]["se"]
            ax.errorbar(c, i + off, xerr=1.96 * se, fmt="o", color=cor, ms=14, lw=3, capsize=6)
    f.subplots_adjust(left=0.30)
    ax.set_yticks(range(len(linhas)), [l[0] for l in linhas[::-1]], fontsize=19)
    ax.axvline(0, color="#444", lw=1.5)
    ax.set_xlabel("pontos de margem por desvio-padrão")
    ax.plot([], [], "o", color=AZUL, ms=14, label="virada 2022 para 2026")
    ax.plot([], [], "o", color=CINZA, ms=14, label="placebo: virada 2018 para 2022")
    ax.legend(fontsize=18, frameon=False, loc="lower right")
    salvar(f, "11_associacoes_por_lugar_e_placebo")


def g12():
    spec = importlib.util.spec_from_file_location("a6", Path(__file__).resolve().parent / "analise-6-municipal.py")
    a6 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(a6)
    m = a6.base()
    pr = pd.read_parquet(DER / "prefeitos_2024.parquet")
    d = m.merge(pr[["uf", "mun", "elegivel", "corrida"]], on=["uf", "mun"])
    d = d[d.elegivel & (d.corrida.abs() <= 15)]
    f, ax = fig("Prefeituras disputadas em 2024: quem ganhou por pouco não explica a virada de 2026", "Virada municipal (2022 para 2026) pela margem do candidato de direita na disputa pela prefeitura em 2024 (positivo = direita ganhou)", "Descontinuidade em eleições apertadas, janela de 5 pontos, núcleo triangular. Cada ponto é a média de uma faixa de 1 ponto")
    d["faixa"] = np.floor(d.corrida)
    g = d.groupby("faixa").apply(lambda x: pd.Series({"c": x.corrida.mean(), "V": x.V.mean(), "n": len(x)}), include_groups=False)
    ax.scatter(g.c, g.V, s=g.n * 2.2, color=AZUL, alpha=0.7)
    for lado in (d[d.corrida < 0], d[d.corrida >= 0]):
        s = lado[lado.corrida.abs() <= 5]
        b = np.polyfit(s.corrida, s.V, 1, w=np.sqrt(1 - s.corrida.abs() / 5))  # mesmo nucleo triangular do estimador
        xs = np.linspace(s.corrida.min(), s.corrida.max(), 20)
        ax.plot(xs, np.polyval(b, xs), color=ESCURO, lw=3)
    ax.axvline(0, color="#666", ls="--", lw=2)
    r = R["h7"]["resultados"]["direita_vs_nao_direita_h5"]["V"]
    ax.text(0.04, 0.06, f"efeito no corte: {r['efeito']:+.2f} ponto (erro padrão {r['se']:.2f}; p = {r['p']:.2f}); n = {r['n']}".replace(".", ","), transform=ax.transAxes, fontsize=19, va="bottom", bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))
    ax.set_xlabel("margem do candidato de direita em 2024 (pontos)")
    ax.set_ylabel("virada municipal (pontos)")
    salvar(f, "12_prefeitos_2024_descontinuidade")


def g13():
    spec = importlib.util.spec_from_file_location("a6", Path(__file__).resolve().parent / "analise-6-municipal.py")
    a6 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(a6)
    m = a6.base()
    f, ax = fig("O voto em Flávio repete o voto em Jair, município a município", f"Cada ponto é um município (5.570); correlação ponderada de {R['h1']['correlacoes_municipais_ponderadas']['jair22_flavio26']:.2f}".replace(".", ","), "Percentual dos votos válidos. Linha cinza: igual. Lugar não é pessoa: isto é entre municípios")
    hb = ax.hexbin(m.jair22, m.flavio26, gridsize=60, cmap="Blues", mincnt=1, bins="log")
    ax.plot([0, 100], [0, 100], color=CINZA, lw=2)
    ax.set_xlabel("Jair Bolsonaro em 2022 (% dos válidos)")
    ax.set_ylabel("Flávio Bolsonaro em 2026 (% dos válidos)")
    ax.set_xlim(5, 90)
    ax.set_ylim(5, 90)
    salvar(f, "13_heranca_jair_flavio")


def g14():
    t = pd.read_csv(RES / "h11_resumo.csv")
    t = t[t.outro.isin(["Tarcisio", "Caiado", "Zema", "Ratinho"]) & (t.institutos >= 2)]
    f, ax = fig("Outros nomes da direita nos cenários: só Tarcísio chegou perto de Flávio", "Diferença de margem contra Lula, nome menos Flávio, mesma pesquisa (pontos; negativo = o nome rendia menos que Flávio)", "Média por trimestre, só trimestres com 2 ou mais institutos. Michelle Bolsonaro não aparece nos dados coletados")
    nomes = {"Tarcisio": "Tarcísio", "Caiado": "Caiado", "Zema": "Zema", "Ratinho": "Ratinho Júnior"}
    cores = {"Tarcisio": AZUL, "Caiado": CINZA, "Zema": "#2a9d8f", "Ratinho": "#9b5de5"}
    for o, g in t.groupby("outro"):
        ax.plot(g.trimestre, g.dif_media, marker="o", lw=3.5, ms=11, color=cores[o], label=nomes[o])
    ax.axhline(0, color="#444", lw=1.5)
    ax.legend(fontsize=19, frameon=False)
    ax.set_ylabel("pontos de margem")
    salvar(f, "14_outros_nomes_da_direita")


def main() -> None:
    g01(); g02(); g03(); g04(); g05(); g06(None); g07(); g08(); g09(); g10(); g11(); g12(); g13(); g14()


if __name__ == "__main__":
    main()
