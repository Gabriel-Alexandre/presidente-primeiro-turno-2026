"""Sintese: o que as pesquisas mostraram e o que so apareceu na urna, H6 pela aritmetica pesquisa-urna, intervalos dos tamanhos,
condicoes de nao execucao e o PLACAR (tamanho, evidencia, confianca) segundo a secao 7 do pre-registro. Nenhum numero e digitado: tudo sai do RESUMO.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import RES, SEMENTE, verificar_fontes  # noqa: E402
from presidente.saida import ler, registrar, tabela  # noqa: E402


def boot_ic(x: np.ndarray, f=np.mean, rep: int = 2000) -> tuple[float, float]:
    rng = np.random.default_rng(SEMENTE)
    x = np.asarray(x, float)
    b = [f(rng.choice(x, len(x), replace=True)) for _ in range(rep)]
    return float(np.percentile(b, 5)), float(np.percentile(b, 95))


def main() -> None:
    verificar_fontes()
    R = json.load(open(RES / "RESUMO.json", encoding="utf-8"))
    e = pd.read_csv(RES / "b2_erro_por_instituto.csv")
    e = e[e.verificada]
    m22, m26 = R["a1"]["margem_2022"], R["a1"]["margem_2026"]
    V = R["a1"]["virada_2022_2026"]
    # --- o que as pesquisas mostraram contra o que so apareceu na urna
    e26, e22 = e[e.ano == 2026], e[e.ano == 2022]
    def aparada(x: pd.Series) -> float:
        v = np.sort(x.to_numpy())
        return float(v[1:-1].mean())

    # A virada vista nas pesquisas da vespera depende do resumo usado (a distribuicao de 2022 e larga: Brasmarket e Veritá)
    resumo = {"media": np.mean, "mediana": np.median, "media_aparada": lambda v: aparada(pd.Series(v))}
    pesq_virada = {}
    for nome, fn in resumo.items():
        a26, a22 = fn(e26.margem_pesquisa.to_numpy()), fn(e22.margem_pesquisa.to_numpy())
        pesq_virada[nome] = {"margem_pesquisas_2022": float(a22), "margem_pesquisas_2026": float(a26), "virada_nas_pesquisas": float(a26 - a22), "pct_da_virada_urna": float(100 * (a26 - a22) / V),
                             "erro_2022": float(fn(e22.erro_margem.to_numpy())), "erro_2026": float(fn(e26.erro_margem.to_numpy()))}
    pm26 = e26.margem_pesquisa.mean()
    pm22 = e22.margem_pesquisa.mean()
    seg = pd.read_csv(RES / "b1_semanal_2026.csv", parse_dates=["semana"]).set_index("semana").margem_flavio_menos_lula
    ini, fim = seg.loc["2026-08-03"], seg.loc["2026-09-28"]
    s = {
        "virada_urna_a_urna": V,
        "virada_vista_nas_pesquisas_por_resumo": pesq_virada,
        "margem_media_das_pesquisas_semanais": {"semana_de_3_ago": float(ini), "semana_de_28_set": float(fim), "movimento_na_campanha": float(fim - ini)},
        "margem_das_pesquisas_2022_vespera": float(pm22), "margem_das_pesquisas_2026_vespera": float(pm26),
        "virada_nas_pesquisas_de_vespera": float(pm26 - pm22),
        "diferenca_entre_urna_e_pesquisa": float(V - (pm26 - pm22)),
        "pct_da_virada_visivel_nas_pesquisas": float(100 * (pm26 - pm22) / V),
        "erro_margem_2026_medio": float(e26.erro_margem.mean()), "erro_margem_2026_ic90": boot_ic(e26.erro_margem.to_numpy()), "erro_margem_2026_mediano": float(e26.erro_margem.median()),
        "erro_margem_2022_medio": float(e22.erro_margem.mean()), "erro_margem_2022_ic90": boot_ic(e22.erro_margem.to_numpy()), "erro_margem_2022_mediano": float(e22.erro_margem.median()),
        "erro_margem_2022_sem_extremos_media": aparada(e22.erro_margem), "erro_margem_2026_sem_extremos_media": aparada(e26.erro_margem),
        "institutos_com_pl_subestimado_2026": int((e26.erro_pl < 0).sum()), "institutos_com_pl_subestimado_2022": int((e22.erro_pl < 0).sum()),
        "institutos_2026": int(len(e26)), "institutos_2022": int(len(e22)),
        "erro_pl_2026_medio": float(e26.erro_pl.mean()), "erro_pl_2022_medio": float(e22.erro_pl.mean()),
        "erro_pt_2026_medio": float(e26.erro_pt.mean()), "erro_pt_2022_medio": float(e22.erro_pt.mean()),
    }
    registrar("sintese.pesquisas_e_urna", s)
    # --- H6 pela aritmetica pesquisa-urna
    h6 = {}
    for ano in (2026, 2022):
        x = e[e.ano == ano]
        h6[str(ano)] = {"institutos": int(len(x)), "queda_dos_outros_media": float(-x.queda_outros.mean()), "queda_dos_outros_ic90": [float(-v) for v in boot_ic(x.queda_outros.to_numpy())][::-1],
                        "institutos_com_queda_de_3_ou_mais": int((x.queda_outros <= -3).sum()),
                        "fracao_media_que_ficou_com_o_candidato_do_pl": float(x.fracao_pl.mean()), "fracao_mediana": float(x.fracao_pl.median()),
                        "institutos_em_que_o_pl_ficou_com_mais_de_metade": int((x.fracao_pl > 0.5).sum()),
                        "institutos_em_que_o_pt_ficou_com_mais_de_metade": int(((x.erro_pt * -1) / (-x.queda_outros) > 0.5).sum())}
    registrar("h6.pesquisa_urna", h6)
    # --- tamanhos com intervalo (pontos de margem)
    g = pd.DataFrame(R["h4"]["grupos"])
    t = pd.read_csv(RES / "h4_eventos_por_instituto.csv")
    tam = {}
    for ids in ("V17", "V19", "V09,V21,V23,V26,V27"):
        d = t[t.ids == ids].delta.to_numpy()
        if len(d) >= 2:
            tam[ids] = {"mediana_todos_os_institutos": float(np.median(d)), "ic90": boot_ic(d, np.median), "n": int(len(d))}
    registrar("h4.tamanhos_mediana_de_todos_os_testados", tam)
    # --- condicoes de nao execucao (pre-registro, secao 10)
    cond = {
        "A5": "renda por setor censitario nao publicada pelo IBGE na pasta de agregados por setor (lista de 20/mai/2026: sem arquivo de rendimento); nao executa",
        "A6": "nao foram coletadas tabelas por grupo de pelo menos 2 institutos nos dois anos; nao executa",
        "B5": "nao foram coletadas 5 medicoes de rejeicao do mesmo instituto em 2026; nao executa",
        "H5": "nao foram coletadas 5 medicoes do 'principal problema' do mesmo instituto em 2026; nao executa",
        "H10": "propaganda gratuita e gasto parcial nao coletados em formato legivel por maquina; nao executa",
        "H2": "a unica serie estruturada de avaliacao do governo (Wikipedia) termina em nov/2025 e tem no maximo 6 medicoes por instituto; abaixo das 8 exigidas; nao executa. A comparacao dos cinco presidentes tambem nao foi montada",
        "H3_municipal": "Bolsa Familia de agosto de 2022 por municipio nao esta nas URLs publicas de download; so a parte por UF (PNAD) e a descritiva nacional foram feitas",
        "eventos_2025": "V01 a V04 (e os demais de 2025) sem teste: depende da serie de avaliacao do governo (H2)",
        "H14": "redes sociais: sem dado publico confiavel; nao testavel",
    }
    registrar("condicoes_nao_executadas", cond)
    # --- o placar
    hc = lambda k: R[k]
    ev = R["h4"]["grupos"]
    v17 = next(x for x in ev if x["ids"] == "V17")
    v19 = next(x for x in ev if x["ids"] == "V19")
    sep = next(x for x in ev if x["ids"].startswith("V09"))
    h8 = R["h8"]["evangelicos_por_dp"]
    h13 = {k: R["h13"][k] for k in ("jovens_16_a_24_por_dp", "60_mais_por_dp", "superior_por_dp")}
    h7 = R["h7"]["resultados"]["direita_vs_nao_direita_h5"]
    h9 = R["h9"]["resultados"]["2026"]
    h3 = R["h3"]["por_uf"]
    bh = R["bh"]["passa_a_5pct"]
    corr = R["h1"]["correlacoes_municipais_ponderadas"]
    ret = R["a4"]["fluxo"]["jair22_para_flavio26"]
    linhas = [
        ("H1", "Heranca e identidade (a base)", "consistente", "n/a (explica o piso, nao a virada)", "forte para a base",
         "alta", f"correlacao municipal ponderada entre o voto em Jair (2022) e em Flavio (2026) de {corr['jair22_flavio26']:.2f}; retencao de {100*ret['B_amplo']:.0f}% dos eleitores de Jair em Flavio (intervalo regional {100*ret['min_regioes']:.0f} a {100*ret['max_regioes']:.0f}%)"),
        ("H2", "Referendo sobre o governo", "nao testavel", "n/e", "nao testavel", "baixa", cond["H2"]),
        ("H3", "Economia", "inconsistente (descritivo)", "n/e", "fraca",
         "baixa", f"indicadores nacionais melhoraram entre 2022 e 2026 (desocupacao {R['h3']['nacional_descritivo']['desocupacao_trimestral']['t2_2022']}% para {R['h3']['nacional_descritivo']['desocupacao_trimestral']['t2_2026']}%, renda real {R['h3']['nacional_descritivo']['rendimento_real_reais']['variacao_pct']:+.1f}%) enquanto o PT caiu; entre as 27 UFs, a virada foi maior onde a desocupacao caiu menos (coeficiente {h3['d_desocupacao_pontos']['coef']:.2f} ponto por ponto, p = {h3['d_desocupacao_pontos']['p']:.3f}), sem repetir no placebo"),
        ("H4", "Episodios e eventos dos dois lados", "consistente em parte", f"mensagens Flavio-Vorcaro: {v17['mediana_delta']:.1f} ponto de margem (contra Flavio); Lulinha: {v19['mediana_delta']:+.1f} (mediana de todos os institutos)", "forte pela regra literal; depende do limiar (Lulinha)",
         "media", f"V17 coincide com movimento no sentido esperado ({v17['institutos_acima_do_normal']:.0f} de {v17['institutos_testados']} institutos acima do normal); V19 coincide ({v19['institutos_acima_do_normal']:.0f} de {v19['institutos_testados']}, {v19['institutos_acima_limiar_amostral']:.0f} pelo limiar amostral); o bloco de setembro move a margem mas mistura alvos dos dois lados e tem so {sep['institutos_testados']} institutos"),
        ("H5", "Pauta", "nao testavel", "n/e", "nao testavel", "baixa", cond["H5"]),
        ("H6", "Consolidacao e voto util da direita", "consistente", f"{s['margem_media_das_pesquisas_semanais']['movimento_na_campanha']:+.1f} ponto de margem na media das pesquisas entre 3/ago e 28/set; {-s['erro_margem_2026_mediano']:.1f} da ultima pesquisa a urna (mediana), parecido com 2022 ({-s['erro_margem_2022_mediano']:.1f})", "forte (movimento na serie e aritmetica pesquisa-urna em varios institutos)",
         "media", f"os outros candidatos cairam {h6['2026']['queda_dos_outros_media']:.1f} pontos da ultima pesquisa a urna e o candidato do PL ficou com {100*h6['2026']['fracao_media_que_ficou_com_o_candidato_do_pl']:.0f}% da queda (mediana {100*h6['2026']['fracao_mediana']:.0f}%); em {h6['2026']['institutos_em_que_o_pl_ficou_com_mais_de_metade']} de {h6['2026']['institutos']} institutos ficou com mais de metade e o PT em {h6['2026']['institutos_em_que_o_pt_ficou_com_mais_de_metade']}. Em 2022 os outros tambem cairam ({h6['2022']['queda_dos_outros_media']:.1f} pontos) e o candidato do PL ficou com mais de metade em {h6['2022']['institutos_em_que_o_pl_ficou_com_mais_de_metade']} de {h6['2022']['institutos']} institutos: o encolhimento dos outros na reta final nao e novidade de 2026, o que muda e a concentracao no mesmo lado"),
        ("H7", "Maquina local (prefeitos de 2024)", "inconsistente", "n/e", "desenho causal sem efeito detectado", "media",
         f"descontinuidade em {h7['V']['n']} municipios: efeito de {h7['V']['efeito']:+.2f} ponto (erro padrao {h7['V']['se']:.2f}, p = {h7['V']['p']:.2f}), dentro do que o placebo de 2018-2022 mostra ({h7['placebo_V0']['efeito']:+.2f})"),
        ("H8", "Religiao e valores", "inconsistente", "n/e", "fraca", "media",
         f"a virada foi MENOR onde ha mais evangelicos ({h8['principal']['coef']:+.2f} ponto por desvio-padrao de {R['h8']['dp_pct_evangelicos_pontos']:.1f} pontos, p = {h8['principal']['p']:.3f}); no placebo de 2018-2022 o sinal foi o oposto ({h8['placebo_2018_2022']['coef']:+.2f}); leitura compativel com teto (onde Jair ja tinha muito, sobrou menos para subir)"),
        ("H9", "Governadores aliados", "inconsistente", "n/e", "fraca", "baixa",
         f"virada media de {h9['virada_media_bolsonaristas']:.1f} ponto nas {len(h9['ufs_bolsonaristas'])} UFs com governador apoiador de Flavio e de {h9['virada_media_lula']:.1f} nas {len(h9['ufs_lula'])} com governador apoiador de Lula (diferenca {h9['diferenca']:+.1f}; p de permutacao = {h9['p_permutacao']:.2f})"),
        ("H10", "Estrutura de campanha", "nao testavel", "n/e", "nao testavel", "baixa", cond["H10"]),
        ("H11", "O candidato (por que Flavio e nao 'a direita')", "consistente em parte", "n/e", "fraca", "baixa",
         "Caiado, Zema e Ratinho rendiam bem menos que Flavio nos cenarios; Tarcisio rendia perto ou um pouco mais ate o fim de 2025 e menos que Flavio em 2026 (primeiro trimestre); Michelle Bolsonaro nao esta nos dados"),
        ("H12", "Comparecimento", "inconsistente", "n/e", "forte (conta exata)", "alta",
         f"o termo de comparecimento responde por {R['a3']['pl']['pct_comparecimento']['a']:.1f}% do ganho de votos do candidato do PL e por {R['a3']['pt']['pct_comparecimento']['a']:.1f}% da perda do PT; a troca liquida de voto, por {R['a3']['pl']['pct_parcela']['a']:.0f}% e {R['a3']['pt']['pct_parcela']['a']:.0f}%"),
        ("H13", "Renovacao do eleitorado", "inconsistente (envelhecimento)", "n/e", "fraca (o placebo repete o padrao)", "baixa",
         f"municipios cujo eleitorado envelheceu mais tiveram virada menor ({h13['60_mais_por_dp']['principal']['coef']:+.2f} ponto por desvio-padrao); o placebo de 2018-2022 mostra o mesmo sinal ({h13['60_mais_por_dp']['placebo_2018_2022']['coef']:+.2f}), e sem efeito fixo de UF o sinal some"),
        ("H14", "Redes sociais", "nao testavel", "n/e", "nao testavel", "baixa", cond["H14"]),
    ]
    p = pd.DataFrame(linhas, columns=["hipotese", "nome", "situacao", "tamanho", "evidencia", "confianca", "o_que_sustenta"])
    tabela("placar", p)
    registrar("placar", p.to_dict("records"))
    print(p[["hipotese", "situacao", "tamanho", "evidencia", "confianca"]].to_string())
    print(json.dumps(s, ensure_ascii=False, indent=1)[:1500])
    print(json.dumps(h6, ensure_ascii=False, indent=1))
    print(json.dumps(tam, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
