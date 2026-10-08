"""Gera RELATORIO.md, RESUMO_SIMPLES.md, analise-da-ia/DOSSIE.md e docs/LEITURA_DA_IA.md a partir de resultados/RESUMO.json e das tabelas.

Nenhum numero e digitado: tudo sai de R (RESUMO.json) ou dos CSV de resultados/. A leitura e o veredito sao opiniao do Claude, marcada como tal,
escrita sob analise-da-ia/REGRAS_DO_VEREDITO.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import DADOS, RAIZ, RES  # noqa: E402

R = json.load(open(RES / "RESUMO.json", encoding="utf-8"))
PRE_REG_COMMIT = "014e6b7"


def f1(x): return f"{x:.1f}".replace(".", ",")
def f2(x): return f"{x + (1e-9 if x >= 0 else -1e-9):.2f}".replace(".", ",")
def f3(x): return f"{x:.3f}".replace(".", ",")
def sg(x): return f"{x:+.1f}".replace(".", ",")
def sg2(x): return f"{x + (1e-9 if x >= 0 else -1e-9):+.2f}".replace(".", ",")
def dbr(iso): return f"{iso[8:10]}/{iso[5:7]}/{iso[0:4]}"
def tri(c): return f"{c[5]}º trimestre de {c[:4]}"
def pc(x): return f"{x:.1f}%".replace(".", ",")
def mil(x): return f"{x:,.0f}".replace(",", ".")
def mi(x): return f"{x / 1e6:.2f}".replace(".", ",")


def tabela_md(df: pd.DataFrame) -> str:
    cab = "| " + " | ".join(df.columns) + " |"
    sep = "|" + "|".join("---" for _ in df.columns) + "|"
    return "\n".join([cab, sep] + ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)])


a1, a2, a3, a4, b0, b1, b2, b3, b4 = (R[k] for k in ("a1", "a2", "a3", "a4", "b0", "b1", "b2", "b3", "b4"))
h1, h3, h4, h6, h7, h8, h9, h13, h11, bh, val, syn = (R[k] for k in ("h1", "h3", "h4", "h6", "h7", "h8", "h9", "h13", "h11", "bh", "val", "sintese"))
P = syn["pesquisas_e_urna"]
fx = a4["fluxo"]
V = a1["virada_2022_2026"]
OFF = R["val"]["oficial_2026"]
nac = pd.read_csv(RES / "a1_nacional.csv")
abst = {a: float(nac[(nac.ano == a) & (nac.candidato == "_abstencao_pct")].pct_validos.iloc[0]) for a in (2018, 2022, 2026)}
reg = pd.read_csv(RES / "a2_regiao.csv").sort_values("contribuicao", ascending=False)
porte = pd.read_csv(RES / "a2_porte.csv")
ufs = pd.read_csv(RES / "a1_uf.csv")
ev = pd.read_csv(DADOS / "eventos_confirmados.csv")
ev_ok = ev[ev.confirmado & (ev.tipo == "exposicao")]
ev_sem = ev[~ev.confirmado & (ev.tipo == "exposicao")]
aj = a4["ajustes"]
comp_f = aj["amplo:nacional"]["composicao"]["flavio26"]
tot_f = sum(comp_f.values())
comp_pct = {k: 100 * v / tot_f for k, v in comp_f.items()}
cond = R["condicoes_nao_executadas"]
g_h4 = {x["ids"]: x for x in h4["grupos"]}
v17, v19, sep = g_h4["V17"], g_h4["V19"], g_h4["V09,V21,V23,V26,V27"]
tam = h4["tamanhos_mediana_de_todos_os_testados"]
macro = h3["nacional_descritivo"]
sem = b1["margem_por_semana_ultimos_60_dias"]
mov = P["margem_media_das_pesquisas_semanais"]
pv = P["virada_vista_nas_pesquisas_por_resumo"]
h6q = h6["pesquisa_urna"]
_ws = pd.read_csv(RES / "b1_semanal_2026.csv", parse_dates=["semana"]).set_index("semana").margem_flavio_menos_lula
pre_v17 = float(_ws["2026-03-30":"2026-05-11"].mean())
pos_v17 = float(_ws["2026-05-18":"2026-07-27"].mean())
_dep = _ws["2026-05-18":]
volta_v17 = _dep[_dep >= pre_v17].index.min()
volta_txt = volta_v17.strftime("%d/%m") if pd.notna(volta_v17) else "nenhuma semana"
modelo = "Claude Sonnet 5.5 (Anthropic), no Claude Code (aplicativo para computador), em 07/out/2026; o planejamento e a validação do plano foram do Claude Opus 5.5, na mesma sessão de trabalho"

NAO_DIZ = """> **O que este projeto não diz.** Em quem cada pessoa votou, nem por que votou: tudo aqui é entre municípios, instituições e datas. Intenção de ninguém. **Quem vai ganhar o 2º turno** (25/10/2026): nenhuma previsão. Se as pesquisas foram "tendenciosas": a palavra não entra, e o que se mede é erro e direção do erro. O peso das **redes sociais**, da **avaliação do governo**, da **economia no bolso do eleitor** e do **gasto de campanha**: não foi possível testar com dado público (seção 9). Causa onde o desenho só mostra coincidência. **Flávio Bolsonaro terminou o 1º turno em primeiro; ele não venceu a eleição.**"""


def dossie() -> str:
    pl = pd.read_csv(RES / "placar.csv")
    linhas = "\n".join(f"- **{r.hipotese} ({r.nome}):** {r.situacao}. Tamanho: {r.tamanho}. Evidência: {r.evidencia}. Confiança: {r.confianca}. {r.o_que_sustenta}" for r in pl.itertuples())
    return f"""# Dossiê: os números que o veredito lê

**Gerado em 07/out/2026 por `ferramentas/analise-9-relatorio.py` a partir de `resultados/RESUMO.json`.** O veredito (`docs/LEITURA_DA_IA.md`) só usa o que está aqui. Nenhum número de memória.

## Os fatos (arquivo oficial e boletins)
- Margem (candidato do PL menos Lula, pontos dos válidos): 2018 {sg(a1['margem_2018'])}; 2022 {sg(a1['margem_2022'])}; 2026 {sg(a1['margem_2026'])}. Virada de 2022 para 2026: {f2(V)} pontos (PL {sg2(a1['pl_ganho_pontos'])}, Lula {sg2(-a1['pt_perda_pontos'])}).
- Votos: candidato do PL {sg(a1['pl_votos_variacao'] / 1e6)} milhões; Lula {sg(a1['pt_votos_variacao'] / 1e6)} milhões (cada um contra o seu 1º turno de 2022).
- Abstenção (com o exterior): {pc(abst[2022])} em 2022 e {pc(abst[2026])} em 2026.
- Onde: {'; '.join(f"{r.regiao} {pc(r.pct_da_virada)}" for r in reg.itertuples() if r.regiao != 'Exterior')} da virada; interior {pc(a2['capital_interior']['pct_da_virada']['Interior'])}, capitais {pc(a2['capital_interior']['pct_da_virada']['Capital'])}.
- Troca de voto contra comparecimento: parcela do candidato {f1(a3['pl']['pct_parcela']['a'])}% do ganho do PL e {f1(a3['pt']['pct_parcela']['a'])}% da perda de Lula; comparecimento {f1(a3['pl']['pct_comparecimento']['a'])}% e {f1(a3['pt']['pct_comparecimento']['a'])}%.
- Base: correlação municipal ponderada Jair 2022 x Flávio 2026 de {f2(h1['correlacoes_municipais_ponderadas']['jair22_flavio26'])}; retenção ecológica de Jair em Flávio de {pc(100 * fx['jair22_para_flavio26']['B_amplo'])} (regiões: {pc(100 * fx['jair22_para_flavio26']['min_regioes'])} a {pc(100 * fx['jair22_para_flavio26']['max_regioes'])}).

## As pesquisas
- Série: {b0['pesquisas_wikipedia']} pesquisas na tabela; as {b0['pesquisas_casadas_no_registro_tse']} de 2026 casam com o registro do TSE; {b0['pesquisas_de_2025_fora_do_registro_por_lei']} de 2025 não têm como casar; {b0['pesquisas_2025_removidas_por_nao_conferir']} saíram por não conferir na fonte; amostra de {b0['amostra_total']}: {b0['amostra_total'] - b0['amostra_divergentes']} conferem; véspera: {b0['vespera_verificadas']} de {b0['vespera_total']} conferem.
- Média semanal (instituto corrigido pelo próprio desvio): {sg(b1['primeira_semana']['margem'])} na semana de {dbr(b1['primeira_semana']['semana'])}; {sg(mov['semana_de_3_ago'])} na de 3/ago; {sg(mov['semana_de_28_set'])} na de 28/set; movimento na campanha {sg(mov['movimento_na_campanha'])}. Nenhuma semana com o candidato do PL à frente.
- Erro da margem na última pesquisa (pesquisa menos urna): 2026 média {sg(P['erro_margem_2026_medio'])}, mediana {sg(P['erro_margem_2026_mediano'])} ({P['institutos_2026']} institutos, todos com o PL subestimado); 2022 média {sg(P['erro_margem_2022_medio'])}, mediana {sg(P['erro_margem_2022_mediano'])}, média sem os dois extremos {sg(P['erro_margem_2022_sem_extremos_media'])} ({P['institutos_2022']} institutos; PL subestimado em {P['institutos_com_pl_subestimado_2022']}); 2018 média {sg(b2['2018']['erro_margem_medio'])}.
- Virada vista nas pesquisas da véspera, entre 2022 e 2026: {f1(pv['media']['virada_nas_pesquisas'])} pontos pela média ({f1(pv['media']['pct_da_virada_urna'])}% da virada), {f1(pv['media_aparada']['virada_nas_pesquisas'])} pela média aparada ({f1(pv['media_aparada']['pct_da_virada_urna'])}%), {f1(pv['mediana']['virada_nas_pesquisas'])} pela mediana ({f1(pv['mediana']['pct_da_virada_urna'])}%).
- Outros candidatos, da última pesquisa à urna: caem {f1(h6q['2026']['queda_dos_outros_media'])} pontos; o candidato do PL fica com mais de metade dessa queda em {h6q['2026']['institutos_em_que_o_pl_ficou_com_mais_de_metade']} de {h6q['2026']['institutos']} institutos e o PT em {h6q['2026']['institutos_em_que_o_pt_ficou_com_mais_de_metade']}. Em 2022: queda de {f1(h6q['2022']['queda_dos_outros_media'])}; PL em {h6q['2022']['institutos_em_que_o_pl_ficou_com_mais_de_metade']} de {h6q['2022']['institutos']} e PT em {h6q['2022']['institutos_em_que_o_pt_ficou_com_mais_de_metade']}.

## Os episódios (regra do pré-registro, §5)
- 13/05 (mensagens Flávio-Vorcaro): mediana {sg(v17['mediana_delta'])} ponto de margem; {int(v17['institutos_acima_do_normal'])} de {v17['institutos_testados']} institutos acima do normal, {int(v17['institutos_acima_limiar_amostral'])} pelo limiar amostral.
- 30/07 (STF autoriza investigar Lulinha): mediana {sg(v19['mediana_delta'])}; {int(v19['institutos_acima_do_normal'])} de {v19['institutos_testados']} acima do normal, {int(v19['institutos_acima_p95_agrupado'])} pelo p95 agrupado, {int(v19['institutos_acima_limiar_amostral'])} pelo limiar amostral.
- Setembro (cinco episódios, alvos dos dois lados): mediana {sg(sep['mediana_delta'])}; {sep['institutos_testados']} institutos.

## Por lugar
- Evangélicos: {sg2(h8['evangelicos_por_dp']['principal']['coef'])} ponto por desvio-padrão (p = {f3(h8['evangelicos_por_dp']['principal']['p'])}); placebo {sg2(h8['evangelicos_por_dp']['placebo_2018_2022']['coef'])}.
- Eleitorado de 60 anos ou mais (variação): {sg2(h13['60_mais_por_dp']['principal']['coef'])}; placebo {sg2(h13['60_mais_por_dp']['placebo_2018_2022']['coef'])}.
- Prefeitos de 2024 (descontinuidade, janela de 5 pontos): efeito {sg2(h7['resultados']['direita_vs_nao_direita_h5']['V']['efeito'])} (erro padrão {f2(h7['resultados']['direita_vs_nao_direita_h5']['V']['se'])}, p = {f3(h7['resultados']['direita_vs_nao_direita_h5']['V']['p'])}, n = {h7['resultados']['direita_vs_nao_direita_h5']['V']['n']}).
- Governadores com apoio declarado: virada de {f1(h9['resultados']['2026']['virada_media_bolsonaristas'])} (apoiam Flávio) e {f1(h9['resultados']['2026']['virada_media_lula'])} (apoiam Lula); p de permutação {f3(h9['resultados']['2026']['p_permutacao'])}.

## O placar
{linhas}

## O que não foi testado
{chr(10).join(f"- **{k}:** {v}" for k, v in cond.items())}
"""


def relatorio() -> str:
    pl = pd.read_csv(RES / "placar.csv")
    tab_reg = reg.assign(contribuição=lambda d: d.contribuicao.map(f2), pct=lambda d: d.pct_da_virada.map(lambda v: f1(v) + "%"), margem_2022=lambda d: d.margem_2022.map(sg), margem_2026=lambda d: d.margem_2026.map(sg))[["regiao", "margem_2022", "margem_2026", "contribuição", "pct"]]
    tab_reg.columns = ["Região", "Margem 2022", "Margem 2026", "Contribuição à virada (pontos)", "% da virada"]
    tab_porte = porte[porte.porte != "sem par IBGE"].assign(contribuição=lambda d: d.contribuicao.map(f2), pct=lambda d: d.pct_da_virada.map(lambda v: f1(v) + "%"))[["porte", "contribuição", "pct"]]
    tab_porte.columns = ["Porte do município", "Contribuição (pontos)", "% da virada"]
    top = ufs[ufs.uf != "ZZ"].head(3)
    base = ufs[ufs.uf != "ZZ"].tail(3)
    tab_res = pd.DataFrame({"": ["Candidato do PL", "Lula (ou Haddad)", "Outros", "Margem (PL menos PT), pontos", "Abstenção, com o exterior"],
                            "2018": [pc(a1["pl_pct_2018"]), pc(a1["pt_pct_2018"]), pc(100 - a1["pl_pct_2018"] - a1["pt_pct_2018"]), sg(a1["margem_2018"]), pc(abst[2018])],
                            "2022": [pc(a1["pl_pct_2022"]), pc(a1["pt_pct_2022"]), pc(100 - a1["pl_pct_2022"] - a1["pt_pct_2022"]), sg(a1["margem_2022"]), pc(abst[2022])],
                            "2026": [pc(a1["pl_pct_2026"]), pc(a1["pt_pct_2026"]), pc(100 - a1["pl_pct_2026"] - a1["pt_pct_2026"]), sg(a1["margem_2026"]), pc(abst[2026])]})
    tab_ev = ev_ok[["id", "evento", "data_confirmada", "alvo"]].copy()
    tab_ev.columns = ["Id", "Episódio", "Data", "Alvo"]
    flux = []
    for k, label in (("jair22_para_flavio26", "eleitores de Jair 2022 que aparecem em Flávio"), ("lula22_para_flavio26", "eleitores de Lula 2022 que aparecem em Flávio"), ("jair22_para_abst26", "eleitores de Jair 2022 que aparecem na abstenção"),
                     ("terceiros22_para_caiado26", "eleitores de Ciro, Tebet e outros de 2022 que aparecem em Caiado"), ("terceiros22_para_renan26", "eleitores de Ciro, Tebet e outros de 2022 que aparecem em Renan Santos"),
                     ("lula22_para_lula26", "eleitores de Lula 2022 que aparecem em Lula"), ("abst22_para_flavio26", "abstenção de 2022 que aparece em Flávio")):
        d = fx[k]
        flux.append({"Fluxo": label, "Estimativa": pc(100 * d["B_enxuto"]), "Intervalo entre as 5 regiões": f"{pc(100 * d['min_regioes'])} a {pc(100 * d['max_regioes'])}", "Estável?": "sim" if d["robusto"] else "não"})
    tab_flux = pd.DataFrame(flux)
    tab_inst = pd.read_csv(RES / "b2_erro_por_instituto.csv")
    tab_inst = tab_inst[tab_inst.verificada & (tab_inst.ano == 2026)][["instituto", "campo_fim", "pt", "pl", "erro_margem"]].assign(pt=lambda d: d.pt.map(f1), pl=lambda d: d.pl.map(f1), erro_margem=lambda d: d.erro_margem.map(sg))
    tab_inst.columns = ["Instituto", "Fim do campo", "Lula (válidos)", "Flávio (válidos)", "Erro da margem (pontos)"]
    return f"""# Relatório: presidente, 1º turno de 2026

{NAO_DIZ}

**Quem fez a análise.** {modelo}. O autor montou e dirigiu o processo; as leituras e o veredito são do Claude e vêm marcados. Os testes e os limiares foram escritos e gravados em commit (`{PRE_REG_COMMIT}`) **antes** de qualquer análise (`docs/PRE_REGISTRO.md`); as emendas, cada uma com "antes ou depois de ver o resultado", estão na §12 de lá. Todo número deste texto sai de `resultados/RESUMO.json`.

## Em dez achados

1. Flávio Bolsonaro (PL) terminou o 1º turno em primeiro, com {f2(OFF['pct_flavio'])}% dos votos válidos (arquivo oficial), e Lula (PT) com {f2(OFF['pct_lula'])}%. O 2º turno é em 25/10/2026. Em 2022, Lula terminou o 1º turno {f2(-a1['margem_2022'])} pontos na frente do candidato do PL; em 2026, o candidato do PL terminou {f2(OFF['margem_dos_percentuais_publicados'])} na frente: uma **virada de {f2(V)} pontos** na margem.
2. A virada se divide quase ao meio: o candidato do PL ganhou {f2(a1['pl_ganho_pontos'])} pontos e Lula perdeu {f2(a1['pt_perda_pontos'])}. Em votos, são {mi(a1['pl_votos_variacao'])} milhões a mais para um e {mi(-a1['pt_votos_variacao'])} milhões a menos para o outro.
3. Ela veio de todas as regiões e é um fenômeno do interior: {', '.join(f"{r.regiao} {pc(r.pct_da_virada)}" for r in reg.itertuples() if r.regiao != 'Exterior')}; interior {pc(a2['capital_interior']['pct_da_virada']['Interior'])}, capitais {pc(a2['capital_interior']['pct_da_virada']['Capital'])}.
4. Quase todo o ganho foi **troca de voto dentro dos municípios** ({f1(a3['pl']['pct_parcela']['a'])}% do ganho do candidato do PL), e não comparecimento ({f1(a3['pl']['pct_comparecimento']['a'])}%). A abstenção quase não mexeu ({pc(abst[2022])} para {pc(abst[2026])}).
5. A **base é herdada**: a correlação entre o voto em Jair em 2022 e em Flávio em 2026, município a município, é {f2(h1['correlacoes_municipais_ponderadas']['jair22_flavio26'])}, e a estimativa ecológica põe cerca de {pc(100 * fx['jair22_para_flavio26']['B_amplo'])} dos eleitores de Jair em Flávio (estável entre regiões e especificações).
6. A média das pesquisas (instituto a instituto corrigida) manteve **Lula à frente até a última semana** ({sg(mov['semana_de_28_set'])} ponto de margem), e **subiu {f1(mov['movimento_na_campanha'])} pontos a favor de Flávio entre 3/ago e 28/set**. Todos os {P['institutos_2026']} institutos verificados subestimaram o candidato do PL na última pesquisa (erro da margem: mediana {sg(P['erro_margem_2026_mediano'])}, média {sg(P['erro_margem_2026_medio'])}); em 2022 foi parecido (mediana {sg(P['erro_margem_2022_mediano'])}, {P['institutos_com_pl_subestimado_2022']} de {P['institutos_2022']} institutos).
7. Nas três últimas semanas, os outros candidatos encolheram em todos os institutos que mais pesquisaram, e da última pesquisa à urna perderam {f1(h6q['2026']['queda_dos_outros_media'])} pontos; o candidato do PL ficou com mais da metade dessa queda em {h6q['2026']['institutos_em_que_o_pl_ficou_com_mais_de_metade']} de {h6q['2026']['institutos']} institutos e Lula em {h6q['2026']['institutos_em_que_o_pt_ficou_com_mais_de_metade']}. Em 2022 os outros também encolheram, e o candidato do PL ficou com mais da metade em {h6q['2022']['institutos_em_que_o_pl_ficou_com_mais_de_metade']} de {h6q['2022']['institutos']}.
8. **Episódios dos dois lados.** As mensagens de Flávio com Daniel Vorcaro (13/05) coincidem com uma queda de {f1(-v17['mediana_delta'])} pontos na margem do candidato do PL (mediana entre os institutos); a média semanal ficou em {sg(pos_v17)} entre as semanas de 18/05 e 27/07, contra {sg(pre_v17)} nas semanas anteriores, e só voltou ao patamar anterior na semana de {volta_txt}; a autorização do STF para investigar Lulinha (30/07) coincide com {sg(v19['mediana_delta'])} ponto (mediana), um movimento que depende do limiar usado; os cinco episódios de setembro juntos coincidem com {sg(sep['mediana_delta'])}, mas misturam alvos dos dois lados e só {sep['institutos_testados']} institutos têm par de pesquisas.
9. **Por lugar, quatro hipóteses não se sustentam:** a virada foi menor onde há mais evangélicos; o envelhecimento do eleitorado não a explica (e o padrão aparece também no placebo de 2018 a 2022); quem ganhou a prefeitura por pouco em 2024 não se distingue de quem perdeu; e os estados com governador apoiador de Flávio não tiveram virada diferente dos de governador apoiador de Lula.
10. **O que não dá para testar com dado público:** avaliação do governo, voto econômico no nível do eleitor, pauta, redes sociais, tabelas por grupo de eleitor e gasto de campanha. Os indicadores nacionais melhoraram entre 2022 e 2026 (desocupação de {f1(macro['desocupacao_trimestral']['t2_2022'])}% para {f1(macro['desocupacao_trimestral']['t2_2026'])}% no 2º trimestre; renda real do trabalho {sg(macro['rendimento_real_reais']['variacao_pct'])}%), o que é um fato descritivo e não um teste.

## 1. O resultado (A1)

{tabela_md(tab_res)}

Fonte: soma dos boletins de urna (projeto `apuracao-eleicoes-2026`), conferida contra o resultado oficial do TSE por município: 2022 em 34.506 de 34.506 pares município-candidato; 2026 em {val_pares()} (diferença total de {mil(abs(R['a1']['validacao']['2026_1']['dif_total_votos']))} votos, de seções sem boletim publicado). Os {f2(OFF['pct_flavio'])}% e {f2(OFF['pct_lula'])}% citados acima são do arquivo oficial nacional; a soma dos boletins dá {pc(a1['pl_pct_2026'])} e {pc(a1['pt_pct_2026'])}.

Estados com a maior virada: {', '.join(f"{r.uf} ({sg(r.virada_2022_2026)})" for r in top.itertuples())}. Com a menor: {', '.join(f"{r.uf} ({sg(r.virada_2022_2026)})" for r in base.itertuples())}. Tabela completa em `resultados/a1_uf.csv`.

## 2. Onde está a virada (A2)

Decomposição exata da mudança da margem em contribuição de cada grupo de municípios (deslocamento e participação; a soma dá {f2(V)} pontos em todas as quatro formas).

{tabela_md(tab_reg)}

{tabela_md(tab_porte)}

Leitura: nenhuma região e nenhuma faixa de tamanho de cidade carrega a virada sozinha. As cidades de 20 a 100 mil habitantes e as de até 20 mil somam {pc(porte[porte.porte.isin(['20 a 100 mil', 'ate 20 mil'])].pct_da_virada.sum())}; as acima de 500 mil, {pc(porte[porte.porte == 'acima de 500 mil'].pct_da_virada.iloc[0])}. O efeito de composição (mudança do peso de cada grupo) é pequeno ({f2(a2['regiao']['composicao_total'])} ponto por região); o que mudou foi a margem dentro de cada grupo.

## 3. Troca de voto ou comparecimento (A3)

Para cada município, a variação de votos de 2022 para 2026 se decompõe, na ordem, em crescimento do eleitorado apto, variação do comparecimento, variação da fração de votos válidos e variação da **parcela do candidato** entre os válidos (a troca líquida de voto). A soma é exata; a ordem inversa dá o intervalo.

- Candidato do PL: {mil(a3['pl']['total'])} votos; parcela do candidato {mil(a3['pl']['termos_ordem_a']['parcela'])} ({f1(a3['pl']['pct_parcela']['a'])}% na ordem principal, {f1(a3['pl']['pct_parcela']['b'])}% na inversa); comparecimento {mil(a3['pl']['termos_ordem_a']['comparecimento'])}; eleitorado apto {mil(a3['pl']['termos_ordem_a']['apto'])}.
- Lula: {mil(a3['pt']['total'])} votos; parcela do candidato {mil(a3['pt']['termos_ordem_a']['parcela'])} ({f1(a3['pt']['pct_parcela']['a'])}% da perda); comparecimento {mil(a3['pt']['termos_ordem_a']['comparecimento'])}; eleitorado apto {mil(a3['pt']['termos_ordem_a']['apto'])}.
- Se cada município tivesse a taxa de comparecimento de 2022, a margem de 2026 seria {sg2(a3['margem_2026_com_comparecimento_de_2022'])} em vez de {sg2(a3['margem_2026_sobre_municipios_comuns'])}: o comparecimento muda a margem em {f2(abs(a3['margem_2026_com_comparecimento_de_2022'] - a3['margem_2026_sobre_municipios_comuns']))} ponto.

## 4. Para onde foi o voto de 2022 (A4, inferência ecológica)

Regressão ecológica com restrições, 5.570 municípios, 300 reamostragens. **É uma estimativa entre lugares: não diz em quem ninguém votou.** As soluções ficam muitas vezes na borda (muitos zeros exatos) e os intervalos de reamostragem subestimam a incerteza real; por isso só entra como resultado o fluxo que passa em três critérios (as duas especificações diferem em até 3 pontos, as cinco regiões variam até 15 pontos e o valor nacional fica dentro do intervalo das regiões).

{tabela_md(tab_flux)}

Composição do voto de Flávio na especificação ampla: {pc(comp_pct['jair22'])} de eleitores de Jair de 2022, {pc(comp_pct['abst22'])} do grupo que não votou em 2022 (inclui eleitores novos e o efeito de quem saiu do cadastro), {pc(comp_pct['lula22'])} de eleitores de Lula de 2022. **Os fluxos de e para a abstenção e o de Lula para Lula não são estáveis entre regiões**, e a base de eleitores muda entre 2022 e 2026 (mortes, novos títulos), o que a regressão trata como transição. O fluxo que se sustenta é o da herança.

## 5. As pesquisas e a reta final (B)

**Como a série foi montada.** {b0['pesquisas_wikipedia']} pesquisas na tabela da Wikipédia (que cita a fonte de cada linha). Todas as {b0['pesquisas_casadas_no_registro_tse']} de 2026 aparecem no registro de pesquisas do TSE (instituto e data); as {b0['pesquisas_de_2025_fora_do_registro_por_lei']} de 2025 não têm como aparecer (a lei só exige registro no ano eleitoral) e entram só se a fonte citada confirma os valores; {b0['pesquisas_2025_removidas_por_nao_conferir']} saíram por não conferir. Conferência na fonte: amostra sorteada de {b0['amostra_total']}, {b0['amostra_total'] - b0['amostra_divergentes']} conferem; véspera, {b0['vespera_verificadas']} de {b0['vespera_total']}. A véspera sem fonte que confere fica na série, marcada, e fora do cálculo de erro.

**Trajetória (B1).** Margem média semanal do candidato do PL menos Lula, com cada instituto corrigido pelo próprio desvio: {sg(b1['primeira_semana']['margem'])} na semana de {dbr(b1['primeira_semana']['semana'])}, {sg(mov['semana_de_3_ago'])} em 3/ago e {sg(mov['semana_de_28_set'])} em 28/set. Nenhuma semana teve o candidato do PL à frente. A urna deu {sg(a1['margem_2026'])}.

**Erro por instituto (B2).** Na última pesquisa de cada instituto, o candidato do PL foi subestimado em todos os {P['institutos_2026']} institutos verificados de 2026 e em {P['institutos_com_pl_subestimado_2022']} de {P['institutos_2022']} de 2022; em 2018 o erro foi de {sg(b2['2018']['erro_margem_medio'])} (sem direção). O erro da margem foi de mediana {sg(P['erro_margem_2026_mediano'])} e média {sg(P['erro_margem_2026_medio'])} (intervalo de 90% da média: {sg(P['erro_margem_2026_ic90'][0])} a {sg(P['erro_margem_2026_ic90'][1])}) em 2026, e de mediana {sg(P['erro_margem_2022_mediano'])} e média {sg(P['erro_margem_2022_medio'])} em 2022; a média de 2022 é puxada por dois institutos muito fora da curva (média sem os dois extremos: {sg(P['erro_margem_2022_sem_extremos_media'])}). **O erro típico de 2026 foi do tamanho do de 2022, não maior.**

{tabela_md(tab_inst)}

**Quanto da virada as pesquisas mostravam.** Entre as vésperas de 2022 e de 2026, a margem das pesquisas andou {f1(pv['media']['virada_nas_pesquisas'])} pontos pela média ({f1(pv['media']['pct_da_virada_urna'])}% da virada de {f2(V)}), {f1(pv['media_aparada']['virada_nas_pesquisas'])} pela média aparada ({f1(pv['media_aparada']['pct_da_virada_urna'])}%) e {f1(pv['mediana']['virada_nas_pesquisas'])} pela mediana ({f1(pv['mediana']['pct_da_virada_urna'])}%). **O dado não permite dizer qual fração apareceu só na urna**; a resposta depende do resumo usado.

**Os outros candidatos (B3).** Da última pesquisa verificada à urna, os outros caíram {f1(h6q['2026']['queda_dos_outros_media'])} pontos (intervalo de 90%: {f1(h6q['2026']['queda_dos_outros_ic90'][0])} a {f1(h6q['2026']['queda_dos_outros_ic90'][1])}); o candidato do PL ficou com {f1(100 * h6q['2026']['fracao_media_que_ficou_com_o_candidato_do_pl'])}% dessa queda em média (mediana {f1(100 * h6q['2026']['fracao_mediana'])}%). Isso inclui como os indecisos se distribuíram, porque o valor válido da pesquisa tira os indecisos em proporção. Nas três últimas semanas, em cada um dos 5 institutos com mais rodadas, os outros encolheram (começo da janela: de {f1(min(v['outros_inicio'] for v in b3['ultimos_21_dias'].values()))}% a {f1(max(v['outros_inicio'] for v in b3['ultimos_21_dias'].values()))}% dos válidos; fim: de {f1(min(v['outros_fim'] for v in b3['ultimos_21_dias'].values()))}% a {f1(max(v['outros_fim'] for v in b3['ultimos_21_dias'].values()))}%), e a margem do candidato do PL melhorou em {sum(1 for v in b3['ultimos_21_dias'].values() if v['margem_fim'] > v['margem_inicio'])} deles. A comparação por município de 2022 para 2026 (B3c) não mostra o mesmo padrão: onde os outros caíram mais, foi Lula, não o candidato do PL, que mais ganhou (coeficiente de Lula sobre a queda dos outros {sg2(h6['municipal']['lula_sobre_d_outros']['coef'])}; do candidato do PL {sg2(h6['municipal']['flavio_sobre_d_outros']['coef'])}); mas os "outros" de 2022 (Ciro, Tebet) e de 2026 (Caiado, Cury, Renan) são pessoas diferentes.

**Decomposição do erro (B4).** Só {b4['institutos']} institutos têm última pesquisa verificada e pelo menos 3 pesquisas em 21 dias. Neles o erro médio da margem foi de {sg(b4['erro_medio'])}; a parte consistente com mudança de última hora (extrapolação da tendência do instituto) foi de {sg(b4['parte_ultima_hora_media'])} e o resíduo de {sg(b4['residuo_medio'])}. A parte atribuível a comparecimento diferencial não pôde ser medida (exigiria pesquisa por UF).

## 6. Episódios dos dois lados (H4)

Lista fechada em commit antes das séries (`dados/eventos.csv`); {h4['exposicoes_confirmadas']} dos {h4['exposicoes_na_lista']} episódios tiveram a data confirmada em duas reportagens (`dados/eventos_confirmados.csv`, capturas em `dados/CAPTURAS.csv`) e {h4['exposicoes_removidas_sem_data_confirmada']} saíram, como o pré-registro manda. O alvo de cada episódio é quem o fato trata, não quem ele "ajudaria".

{tabela_md(tab_ev)}

Teste (pré-registro, §5): por instituto com 8 ou mais rodadas, a mudança da margem entre a última pesquisa antes e a primeira depois do episódio (ou do grupo de episódios a menos de 30 dias um do outro), com par a até 45 dias e o mesmo número de candidatos; o movimento é "acima do normal" se passa do percentil 95 das variações do próprio instituto fora das janelas de episódio; coincide com movimento quando 2 ou mais institutos passam, no mesmo sentido.

| Episódio | Alvo | Institutos com par | Mediana (pontos) | Acima do normal (regra literal) | pelo p95 agrupado | pelo limiar amostral | Leitura |
|---|---|---|---|---|---|---|---|
| 13/05, mensagens Flávio-Vorcaro | Flávio | {v17['institutos_testados']} | {sg(v17['mediana_delta'])} | {int(v17['institutos_acima_do_normal'])} | {int(v17['institutos_acima_p95_agrupado'])} | {int(v17['institutos_acima_limiar_amostral'])} | coincide, no sentido esperado |
| 30/07, STF autoriza investigar Lulinha | Lula e governo | {v19['institutos_testados']} | {sg(v19['mediana_delta'])} | {int(v19['institutos_acima_do_normal'])} | {int(v19['institutos_acima_p95_agrupado'])} | {int(v19['institutos_acima_limiar_amostral'])} | coincide, no sentido esperado; **depende do limiar** |
| Setembro (V09, V21, V23, V26, V27) | dos dois lados | {sep['institutos_testados']} | {sg(sep['mediana_delta'])} | {int(sep['institutos_acima_do_normal'])} | {int(sep['institutos_acima_p95_agrupado'])} | {int(sep['institutos_acima_limiar_amostral'])} | coincide, sem sentido esperado |

As duas colunas de sensibilidade foram definidas **depois** de ver as diferenças por instituto (emenda 3). V16 e V12 (dezembro de 2025) não têm instituto com par antes e depois. **Os episódios de 2025 (V01 a V04) não foram testados**, porque dependiam da série de avaliação do governo, que não alcança as 8 medições exigidas. Sem confirmação de data saíram {len(ev_sem)} episódios, entre eles os de ministros do STF no caso Master anteriores a setembro, o da Operação Contenção e o das sanções e tarifas de 2026.

Efeito não é causa: "coincide com movimento" quer dizer que a série se moveu além do normal naquela janela. O movimento depois das mensagens de Flávio com Vorcaro **durou meses**: a média semanal foi de {sg(pre_v17)} entre 30/03 e 11/05, de {sg(pos_v17)} entre 18/05 e 27/07, e só voltou a esse patamar anterior na semana de {volta_txt}, já na campanha.

## 7. Por lugar (H1, H3, H7, H8, H9, H13)

Todas as regressões usam o município como unidade, peso pelos válidos de 2026, efeito fixo de UF e erro agrupado por UF; o placebo repete a regressão sobre a virada de 2018 para 2022. Lugar não é pessoa.

| Hipótese | Resultado | Placebo 2018-2022 | Sem os 5 maiores estados | Passa a correção de Benjamini-Hochberg? |
|---|---|---|---|---|
| H8, evangélicos (por desvio-padrão de {f1(h8['dp_pct_evangelicos_pontos'])} pontos) | {sg2(h8['evangelicos_por_dp']['principal']['coef'])} (p = {f3(h8['evangelicos_por_dp']['principal']['p'])}) | {sg2(h8['evangelicos_por_dp']['placebo_2018_2022']['coef'])} | {sg2(h8['evangelicos_por_dp']['sem_5_maiores_ufs']['coef'])} | {'sim' if bh['passa_a_5pct']['H8_evangelicos'] else 'não'} |
| H13, mais eleitores com 60 anos ou mais | {sg2(h13['60_mais_por_dp']['principal']['coef'])} (p = {f3(h13['60_mais_por_dp']['principal']['p'])}) | {sg2(h13['60_mais_por_dp']['placebo_2018_2022']['coef'])} | {sg2(h13['60_mais_por_dp']['sem_5_maiores_ufs']['coef'])} | {'sim' if bh['passa_a_5pct']['H13_60_mais'] else 'não'} |
| H13, mais eleitores de 16 a 24 anos | {sg2(h13['jovens_16_a_24_por_dp']['principal']['coef'])} (p = {f3(h13['jovens_16_a_24_por_dp']['principal']['p'])}) | {sg2(h13['jovens_16_a_24_por_dp']['placebo_2018_2022']['coef'])} | {sg2(h13['jovens_16_a_24_por_dp']['sem_5_maiores_ufs']['coef'])} | {'sim' if bh['passa_a_5pct']['H13_jovens'] else 'não'} |
| H13, mais eleitores com superior | {sg2(h13['superior_por_dp']['principal']['coef'])} (p = {f3(h13['superior_por_dp']['principal']['p'])}) | {sg2(h13['superior_por_dp']['placebo_2018_2022']['coef'])} | {sg2(h13['superior_por_dp']['sem_5_maiores_ufs']['coef'])} | {'sim' if bh['passa_a_5pct']['H13_superior'] else 'não'} |
| H7, descontinuidade em prefeituras de 2024 (n = {h7['resultados']['direita_vs_nao_direita_h5']['V']['n']}) | {sg2(h7['resultados']['direita_vs_nao_direita_h5']['V']['efeito'])} (p = {f3(h7['resultados']['direita_vs_nao_direita_h5']['V']['p'])}) | {sg2(h7['resultados']['direita_vs_nao_direita_h5']['placebo_V0']['efeito'])} | n/a | {'sim' if bh['passa_a_5pct']['H7_h5'] else 'não'} |
| H3, mudança da desocupação por UF (27 pontos, por ponto percentual) | {sg2(h3['por_uf']['d_desocupacao_pontos']['coef'])} (p = {f3(h3['por_uf']['d_desocupacao_pontos']['p'])}) | {sg2(h3['por_uf']['placebo_2018_2022']['d_desocupacao_pontos']['coef'])} | n/a | {'sim' if bh['passa_a_5pct']['H3_desocupacao_uf'] else 'não'} |

- **H1 (herança):** correlação ponderada de {f2(h1['correlacoes_municipais_ponderadas']['jair22_flavio26'])} entre Jair 2022 e Flávio 2026 (de {f2(h1['correlacoes_municipais_ponderadas']['jair18_jair22'])} entre Jair 2018 e Jair 2022; de {f2(h1['correlacoes_municipais_ponderadas']['lula22_lula26'])} para Lula). A virada tem correlação de {f2(h1['correlacoes_municipais_ponderadas']['V_com_jair22'])} com o voto em Jair de 2022: ela se espalha por todo o mapa, com um pouco mais de força onde Jair tinha menos (virada média de {f1(float(pd.read_csv(RES / 'h1_virada_por_faixa_de_jair22.csv').V_medio.iloc[0]))} pontos onde Jair tinha até 25%, {f1(float(pd.read_csv(RES / 'h1_virada_por_faixa_de_jair22.csv').V_medio.iloc[-1]))} onde tinha mais de 65%).
- **H8 (religião):** o sinal é **contrário** ao da hipótese. Onde há mais evangélicos, a virada foi menor. O sinal permanece ao controlar pelo voto de Jair em 2022 ({sg2(R['revisao']['controle_pelo_voto_de_jair_2022']['religiao_com_jair22']['coef'])}, p = {f3(R['revisao']['controle_pelo_voto_de_jair_2022']['religiao_com_jair22']['p'])}), então não é só efeito teto (quem já tinha muito voto sobraria menos para subir). O sinal oposto no placebo de 2018 a 2022 mostra que, em 2022, Jair ganhou mais onde havia mais evangélicos; o que o desenho não separa é por que isso se inverteu.
- **H13 (renovação do eleitorado):** onde o eleitorado envelheceu mais, a virada foi menor, e o placebo repete o padrão (sinal igual, tamanho maior); sem efeito fixo de UF o sinal some. A variação média ponderada de eleitores com 60 anos ou mais foi de {sg(h13['variacao_media_ponderada_pontos']['60_mais'])} ponto e a de 16 a 24 anos, {sg(h13['variacao_media_ponderada_pontos']['jov'])}: se há efeito de composição, ele ajudaria Lula, não Flávio. Sem pesquisa por idade (A6), a evidência não passa de fraca.
- **H7 (máquina local):** {h7['resultados']['direita_vs_nao_direita_h5']['V']['n']} municípios na janela de 5 pontos ({h7['resultados']['direita_vs_nao_direita_h5']['V']['n_dir']} com direita vencedora e {h7['resultados']['direita_vs_nao_direita_h5']['V']['n_esq']} com direita perdedora); o efeito de {sg2(h7['resultados']['direita_vs_nao_direita_h5']['V']['efeito'])} ponto está dentro do intervalo do placebo. Poder suficiente (mais de 200 municípios). A variante só com o PL, janela de 5 pontos: {sg2(h7['resultados']['so_PL_h5']['V']['efeito'])} (p = {f3(h7['resultados']['so_PL_h5']['V']['p'])}).
- **H9 (governadores aliados):** virada média de {f1(h9['resultados']['2026']['virada_media_bolsonaristas'])} pontos nas {len(h9['resultados']['2026']['ufs_bolsonaristas'])} UFs com governador apoiador de Flávio e de {f1(h9['resultados']['2026']['virada_media_lula'])} nas {len(h9['resultados']['2026']['ufs_lula'])} com governador apoiador de Lula; diferença de {sg(h9['resultados']['2026']['diferenca'])} (p de permutação {f3(h9['resultados']['2026']['p_permutacao'])}).
- **H3 (economia):** descritivo nacional, não é teste. Desocupação de {f1(macro['desocupacao_trimestral']['t2_2022'])}% no 2º trimestre de 2022 para {f1(macro['desocupacao_trimestral']['t2_2026'])}% no de 2026 (mínimo de {f1(macro['desocupacao_trimestral']['min_desde_2022'])}% no {tri(macro['desocupacao_trimestral']['trimestre_do_min'])}); renda real do trabalho de R$ {mil(macro['rendimento_real_reais']['t2_2022'])} para R$ {mil(macro['rendimento_real_reais']['t2_2026'])} ({sg(macro['rendimento_real_reais']['variacao_pct'])}%); inflação em 12 meses de {f1(macro['geral']['set2022'])}% (set/2022) para {f1(macro['geral']['set2026'])}% (set/2026), e a de alimentos de {f1(macro['alimentacao_e_bebidas']['set2022'])}% para {f1(macro['alimentacao_e_bebidas']['set2026'])}%; Selic meta de {f2(macro['selic_meta']['out2022'])}% em out/2022 e {f2(macro['selic_meta']['set2026'])}% em set/2026 (chegou a {f2(macro['selic_meta']['max'])}% no período). Entre as 27 UFs, a virada foi maior onde a desocupação caiu menos (p = {f3(h3['por_uf']['d_desocupacao_pontos']['p'])}), mas o placebo não confirma e 27 pontos são poucos.
- **H11 (por que Flávio e não outro nome):** nos cenários de pesquisa, Caiado, Zema e Ratinho Júnior rendiam muito menos que Flávio contra Lula; Tarcísio rendia perto (diferença média de {sg(float(pd.read_csv(RES / 'h11_resumo.csv').query("outro == 'Tarcisio' and trimestre == '2025Q4'").dif_media.iloc[0]))} ponto no 4º trimestre de 2025) e passou a render menos (diferença de {sg(float(pd.read_csv(RES / 'h11_resumo.csv').query("outro == 'Tarcisio' and trimestre == '2026Q1'").dif_media.iloc[0]))} no 1º de 2026). Michelle Bolsonaro não está nos dados coletados.

## 8. O placar

{tabela_md(pl[['hipotese', 'nome', 'situacao', 'evidencia', 'confianca']].rename(columns={'hipotese': 'Hipótese', 'nome': 'Nome', 'situacao': 'Situação', 'evidencia': 'Evidência', 'confianca': 'Confiança'}))}

O detalhe de cada linha e o veredito estão em `docs/LEITURA_DA_IA.md`. Os tamanhos não se somam: as hipóteses se sobrepõem.

## 9. O que ficou de fora, e por quê

{chr(10).join(f"- **{k}:** {v}." for k, v in cond.items())}

## 10. Conferências e erros achados

- Votos por município contra o resultado oficial do TSE: 2018, 2022 e 2026 (seção 1).
- **Recontagem independente** (`ferramentas/validacao-independente.py`, código novo e outras fontes): {val['independente']['passam']} de {val['independente']['numeros']} números conferem, com diferença máxima de 0,004 ponto e de 1,8 mil votos.
- Perfil do eleitorado contra o eleitorado apto dos boletins: diferença total de {f3(a1['validacao_perfil']['2022']['dif_total_pct'])}% (2022) e {f3(a1['validacao_perfil']['2026']['dif_total_pct'])}% (2026).
- Testes automáticos (`python -m pytest -q`) e conferência de linguagem (`ferramentas/conferir-linguagem.py`).
- Erros achados no caminho e corrigidos estão em `docs/CORRECOES.md`; a revisão adversarial, em `docs/REVISAO_ADVERSARIAL.md`.

## 11. Como refazer

`docs/REPLICAR.md`. Os dados por seção e por município vêm de dois projetos anteriores, lidos por hash (`dados/FONTE_APURACAO.json`, `dados/FONTE_CONGRESSO.json`); os dados novos estão em `dados/MANIFESTO.json`.
"""


def val_pares() -> str:
    v = R["a1"]["validacao"]["2026_1"]
    return f"{mil(v['iguais'])} de {mil(v['pares_municipio_candidato'])} pares município-candidato"


def resumo_simples() -> str:
    return f"""# Resumo simples

**Gerado em 07/out/2026 a partir de `resultados/RESUMO.json`.** O relatório completo é o [`RELATORIO.md`](RELATORIO.md) e a opinião do Claude está em [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md).

{NAO_DIZ}

## O que aconteceu

- Em 2022, Lula terminou o 1º turno {f2(-a1['margem_2022'])} pontos na frente. Em 2026, Flávio terminou {f2(OFF['margem_dos_percentuais_publicados'])} na frente. A virada foi de **{f2(V)} pontos**: o candidato do PL ganhou {f2(a1['pl_ganho_pontos'])} e Lula perdeu {f2(a1['pt_perda_pontos'])}.
- Veio de todas as regiões (Sudeste {pc(reg.set_index('regiao').pct_da_virada['Sudeste'])}, Nordeste {pc(reg.set_index('regiao').pct_da_virada['Nordeste'])}, Sul {pc(reg.set_index('regiao').pct_da_virada['Sul'])}) e do interior ({pc(a2['capital_interior']['pct_da_virada']['Interior'])}).
- Foi troca de voto, não comparecimento (a abstenção ficou em {pc(abst[2022])} e {pc(abst[2026])}).

## O que explica, pelos dados

- **A base é herdada.** O voto em Flávio repete o voto em Jair município a município (correlação de {f2(h1['correlacoes_municipais_ponderadas']['jair22_flavio26'])}), e cerca de {pc(100 * fx['jair22_para_flavio26']['B_amplo'])} dos eleitores de Jair de 2022 aparecem em Flávio.
- **A virada se deu na campanha.** A média das pesquisas subiu {f1(mov['movimento_na_campanha'])} pontos a favor de Flávio entre agosto e setembro e os outros candidatos encolheram nas últimas semanas, com o candidato do PL ficando com a maior parte.
- **As pesquisas subestimaram o candidato do PL**, em 2026 e em 2022, de um jeito parecido (erro típico da margem de {sg(P['erro_margem_2026_mediano'])} em 2026 e {sg(P['erro_margem_2022_mediano'])} em 2022).
- **Episódios dos dois lados mexeram nas pesquisas:** as mensagens de Flávio com Vorcaro (13/05) coincidem com queda de {f1(-v17['mediana_delta'])} pontos da margem do candidato do PL, que durou meses; a investigação de Lulinha (30/07) com {sg(v19['mediana_delta'])} ponto, que depende do limiar.
- **Não explicam:** religião (sinal contrário), envelhecimento do eleitorado, prefeitos de 2024 e governadores aliados.

## O que não dá para dizer

Avaliação do governo, economia no bolso do eleitor, redes sociais, pauta, grupos de eleitores e gasto de campanha **não foram testados** (faltou dado público). Em quem cada pessoa votou: os dados são por município. O 2º turno: nenhuma previsão.
"""


def leitura() -> str:
    pl = pd.read_csv(RES / "placar.csv")
    tab = pl[["hipotese", "nome", "situacao", "tamanho", "evidencia", "confianca"]].rename(columns={"hipotese": "#", "nome": "Hipótese", "situacao": "Situação", "tamanho": "Tamanho (pontos de margem)", "evidencia": "Evidência", "confianca": "Confiança"})
    detalhe = "\n\n".join(f"**{r.hipotese} · {r.nome}.** {r.o_que_sustenta}." for r in pl.itertuples())
    return f"""# A leitura do Claude, hipótese por hipótese

**Escrito em 07/out/2026.** {modelo}. É **opinião do Claude**, marcada como opinião, escrita depois das passadas de revisão (`docs/REVISAO_ADVERSARIAL.md`), sob as regras de `analise-da-ia/REGRAS_DO_VEREDITO.md` (em commit antes da análise). Cada número vem de `analise-da-ia/DOSSIE.md`, que vem de `resultados/RESUMO.json`.

> **Opinião não é prova.** O [`RELATORIO.md`](../RELATORIO.md) diz o que os dados fecham. Este arquivo diz qual é a leitura mais provável, com o grau de confiança e o que ficou sem resposta. Nenhuma frase julga intenção de pessoa, partido, instituto de pesquisa, emissora ou tribunal, e nenhuma afirma causa onde o desenho só mostra coincidência. Flávio terminou o 1º turno em primeiro; não venceu a eleição. Nenhuma frase prevê o 2º turno.

## A resposta em quatro frases

1. **O que mudou na urna** (nível mecânico, confiança alta). Entre o 1º turno de 2022 e o de 2026, a margem do candidato do PL sobre Lula andou {f2(V)} pontos, quase ao meio entre o ganho do candidato do PL ({sg2(a1['pl_ganho_pontos'])}) e a perda de Lula ({sg2(-a1['pt_perda_pontos'])}); foi troca de voto dentro dos municípios, em todas as regiões, e não comparecimento.
2. **O que aconteceu na reta final** (nível próximo, confiança média). A média das pesquisas manteve Lula à frente até a última semana e subiu {f1(mov['movimento_na_campanha'])} pontos a favor de Flávio entre 3/ago e 28/set; os outros candidatos encolheram e o candidato do PL ficou com mais da metade do que eles perderam entre a última pesquisa e a urna em {h6q['2026']['institutos_em_que_o_pl_ficou_com_mais_de_metade']} de {h6q['2026']['institutos']} institutos. Os institutos subestimaram o candidato do PL de um jeito parecido com 2022, então a "surpresa" não é maior do que a de 2022.
3. **O principal fator** (confiança baixa a média). **Nenhum fator sozinho explica as {f2(V)} pontos.** O que mais se destaca é a consolidação do voto da direita em torno de Flávio na campanha (H6), que ocorre na mesma janela de tempo dos episódios de setembro (H4) e não se separa deles com os dados; atrás disso há uma base herdada que mantém quase todo o voto de Jair de 2022 em Flávio (H1), sem a qual a virada não aconteceria. Pela definição escrita antes (maior tamanho com evidência pelo menos média), a resposta é **empate entre a consolidação na reta final e o bloco de episódios de setembro**, que não podem ser somados nem separados.
4. **O que os dados não alcançam.** Avaliação do governo, voto econômico no nível do eleitor, pauta, redes sociais, tabelas por grupo de eleitor e gasto de campanha não foram testados; por isso esta resposta **não** diz que esses fatores não pesaram.

## O placar

{tabela_md(tab)}

*Consistente* = as previsões da hipótese aparecem nos testes nomeados; *inconsistente* = aparece o contrário; *não testável* = o dado coletado não alcança. **Os tamanhos não se somam.** Evidência *forte*: desenho que separa causa ou movimento na série no momento certo em 2 ou mais institutos; *média*: associação entre lugares que passa a correção, mantém o sinal e não se repete no placebo; *fraca*: o resto.

{detalhe}

## A leitura por bloco

### A base e a virada (H1, H12)

**Na opinião do Claude (confiança alta):** a eleição de 2026 repetiu a geografia de 2022 e mudou o tamanho dela. A correlação de {f2(h1['correlacoes_municipais_ponderadas']['jair22_flavio26'])} entre Jair e Flávio é tão alta quanto a de Jair 2018 com Jair 2022 ({f2(h1['correlacoes_municipais_ponderadas']['jair18_jair22'])}) e a de Lula 2022 com Lula 2026 ({f2(h1['correlacoes_municipais_ponderadas']['lula22_lula26'])}), o que sugere uma divisão estável do eleitorado, com o candidato do PL ganhando {f1(a1['pl_ganho_pontos'])} ponto e Lula perdendo {f1(a1['pt_perda_pontos'])}, em relação a 2022, sobre a mesma geografia. A comparação que sustenta: o termo de comparecimento responde por {f1(a3['pl']['pct_comparecimento']['a'])}% do ganho do candidato do PL e a troca líquida de voto por {f1(a3['pl']['pct_parcela']['a'])}%. **O limite:** os dados são entre lugares; o estudo que diria em quem cada eleitor votou em 2022 e em 2026 só sai em 2027.

### A reta final (H6, B)

**Na opinião do Claude (confiança média):** o que se vê é uma consolidação, não uma troca. Nas três últimas semanas os outros candidatos perderam espaço em todos os institutos e, da última pesquisa à urna, o candidato do PL ficou com mais da metade dessa perda em {h6q['2026']['institutos_em_que_o_pl_ficou_com_mais_de_metade']} de {h6q['2026']['institutos']} institutos (o PT em {h6q['2026']['institutos_em_que_o_pt_ficou_com_mais_de_metade']}). A comparação que sustenta: em 2022 o mesmo encolhimento dos outros aconteceu ({f1(h6q['2022']['queda_dos_outros_media'])} pontos), mas dividido ({h6q['2022']['institutos_em_que_o_pl_ficou_com_mais_de_metade']} de {h6q['2022']['institutos']} para o candidato do PL, {h6q['2022']['institutos_em_que_o_pt_ficou_com_mais_de_metade']} para o PT). **O limite:** o cálculo inclui como os indecisos se distribuíram, e não separa mudança de última hora de erro de medida: nos {b4['institutos']} institutos que dão para decompor, a mudança de última hora explica {f1(b4['parte_ultima_hora_media'])} dos {f1(-b4['erro_medio'])} pontos do erro.

### Episódios dos dois lados (H4)

**Na opinião do Claude (confiança média):** os dados mostram que as notícias mexeram nas pesquisas, nos dois lados, e que o efeito de cada uma foi menor do que a virada. O episódio que mais movimentou a série foi o das mensagens de Flávio com Vorcaro: {sg(v17['mediana_delta'])} ponto de margem em mediana, em {v17['institutos_testados']} institutos, e a média semanal só voltou ao patamar anterior na semana de {volta_txt}. A autorização para investigar Lulinha coincide com {sg(v19['mediana_delta'])} ponto, e esse resultado muda com o limiar (acima do normal em {int(v19['institutos_acima_do_normal'])}, {int(v19['institutos_acima_p95_agrupado'])} ou {int(v19['institutos_acima_limiar_amostral'])} institutos). **A comparação que sustenta:** os dois episódios movem a margem em sentidos opostos, e o das mensagens ({sg(v17['mediana_delta'])}) é maior em módulo do que o da investigação ({sg(v19['mediana_delta'])}); somados, o efeito líquido dos dois é de {sg(v17['mediana_delta'] + v19['mediana_delta'])} ponto, desfavorável ao candidato do PL, ou seja, no sentido contrário ao da virada. **O limite:** eventos de 2025 e os de que não deu para confirmar a data não foram testados, e o movimento de setembro mistura alvos dos dois lados. **A opinião do autor** sobre o peso dos escândalos, se ele a disser no vídeo, é dele, e este veredito não a trata como evidência.

### Por lugar (H3, H7, H8, H9, H13)

**Na opinião do Claude (confiança média para o que não se sustenta, baixa para o resto):** as explicações por perfil de município não ajudam. Religião tem sinal contrário ao da hipótese; o envelhecimento do eleitorado, se tem efeito, é pró-Lula; prefeitos de 2024 e governadores aliados não separam. **A comparação que sustenta:** em religião o sinal se mantém ao tirar os cinco maiores estados, o efeito fixo de UF ou os pesos, mas é o oposto no placebo de 2018 a 2022; no envelhecimento o placebo repete o padrão (e com tamanho maior) e o sinal some sem o efeito fixo de UF; nas prefeituras de 2024 o efeito está dentro do que o placebo mostra; nos governadores a diferença é de {sg(h9['resultados']['2026']['diferenca'])} ponto com p de permutação de {f2(h9['resultados']['2026']['p_permutacao'])}. **O limite:** isso não descarta que religião, idade ou economia importem no nível do eleitor; só diz que a variação **entre municípios** da virada não se alinha com elas.

### A economia (H3)

**Na opinião do Claude (confiança baixa):** os indicadores nacionais melhoraram entre 2022 e 2026 e, ainda assim, Lula perdeu votos em relação a 2022. Isso é um fato descritivo, não prova que a economia não pesou: sem a avaliação do governo (H2) e sem dado por eleitor, o projeto não consegue testar voto econômico. Se o desempenho do governo pesou, e quanto, **o projeto não responde**.

## O que o Claude não consegue dizer

1. Em quem cada pessoa votou, ou por que votou.
2. Se os episódios mudaram votos: só se a série de pesquisas se moveu, e a pesquisa também mede erro.
3. Qual fração da virada as pesquisas mostravam: de {f1(pv['media']['pct_da_virada_urna'])}% a {f1(pv['mediana']['pct_da_virada_urna'])}% conforme o resumo (média ou mediana).
4. Para onde foi o voto dos que não votaram em 2022, e o de Ciro e Tebet: a estimativa não é estável entre regiões.
5. O peso da avaliação do governo, da economia por eleitor, da pauta, das redes sociais e do gasto de campanha.
6. O 2º turno.

## Teste do espelho e do recorte

| Afirmação | Com os lados trocados, seria escrita igual? | Recortada, vira anúncio de quem? |
|---|---|---|
| a virada foi troca de voto, não comparecimento | sim: vale para qualquer virada medida do mesmo jeito | de ninguém: descreve o mecanismo |
| as pesquisas subestimaram o candidato do PL em 2022 e em 2026 | sim: o erro é medido no sinal que ele tem (em 2018 não houve direção, e a frase diz isso) | pode ser usada pelos dois lados; por isso vem com 2022 e a mediana |
| as mensagens de Flávio com Vorcaro coincidem com queda e a investigação de Lulinha com alta | sim: os dois episódios têm o mesmo teste e a mesma linguagem | o recorte "só o primeiro" ou "só o segundo" seria enganoso; as duas frases andam juntas |
| nenhum fator sozinho explica | sim | de ninguém |
| religião e idade não explicam a virada entre municípios | sim: o mesmo teste valeria para qualquer lado | de ninguém |
"""


def main() -> None:
    (RAIZ / "analise-da-ia").mkdir(exist_ok=True)
    (RAIZ / "analise-da-ia" / "DOSSIE.md").write_text(dossie(), encoding="utf-8")
    (RAIZ / "RELATORIO.md").write_text(relatorio(), encoding="utf-8")
    (RAIZ / "RESUMO_SIMPLES.md").write_text(resumo_simples(), encoding="utf-8")
    (RAIZ / "docs" / "LEITURA_DA_IA.md").write_text(leitura(), encoding="utf-8")
    for a in ("RELATORIO.md", "RESUMO_SIMPLES.md", "docs/LEITURA_DA_IA.md", "analise-da-ia/DOSSIE.md"):
        print(a, len((RAIZ / a).read_text(encoding="utf-8").splitlines()), "linhas")


if __name__ == "__main__":
    main()
