"""Gera docs/REVISAO_ADVERSARIAL.md: as tres passadas e a segunda revisao do texto do veredito, com os numeros de resultados/RESUMO.json."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import DADOS, RAIZ, RES  # noqa: E402

R = json.load(open(RES / "RESUMO.json", encoding="utf-8"))


def f1(x): return f"{x:.1f}".replace(".", ",")
def sg(x): return f"{x:+.1f}".replace(".", ",")
def f3(x): return f"{x:.3f}".replace(".", ",")


def contar_causa() -> list[str]:
    achados = []
    for a in ("RELATORIO.md", "RESUMO_SIMPLES.md", "docs/LEITURA_DA_IA.md"):
        for n, l in enumerate((RAIZ / a).read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"\b(causou|causaram|provocou|provocaram|fez com que|por causa d[eao]|devido a)\b", l.lower()):
                achados.append(f"{a}:{n}")
    return achados


def main() -> None:
    ev = pd.read_csv(DADOS / "eventos_confirmados.csv")
    exp = ev[ev.tipo == "exposicao"]
    simetria = exp.groupby(["alvo", "confirmado"]).size().unstack(fill_value=0)
    def lin(alvo):
        x = simetria.loc[alvo] if alvo in simetria.index else {True: 0, False: 0}
        return int(x.get(True, 0)), int(x.get(False, 0))
    sim = {a: lin(a) for a in ("lula_governo", "flavio_oposicao", "ambos")}
    rv = R["revisao"]
    ctl = rv["controle_pelo_voto_de_jair_2022"]
    P = R["sintese"]["pesquisas_e_urna"]
    pv = P["virada_vista_nas_pesquisas_por_resumo"]
    causas = contar_causa()
    lint = subprocess.run([sys.executable, str(RAIZ / "ferramentas" / "conferir-linguagem.py")], capture_output=True, text=True, encoding="utf-8").stdout.strip().splitlines()[-1]
    tx = f"""# Revisão adversarial

**Feita em 07/out/2026 pelo Claude, depois da análise e antes do veredito, e repetida sobre o texto do veredito.** Duas das checagens abaixo (o efeito de teto e o deixar um instituto de fora) viraram números em `resultados/RESUMO.json` (chave `revisao`, `ferramentas/revisao-adversarial.py`). Esta revisão é do mesmo modelo que fez a análise, **não de uma pessoa**: ela reduz erro de método e de linguagem, mas não substitui um revisor externo.

O que mudou no texto por causa da revisão está marcado com **→**.

## Passada 1: o leitor que mais desconfiaria de uma conclusão favorável ao candidato do PL

1. **"As pesquisas erraram mais contra o PL em 2026 do que em 2022."** Era o título do primeiro gráfico. A mediana do erro da margem é {sg(P['erro_margem_2026_mediano'])} em 2026 e {sg(P['erro_margem_2022_mediano'])} em 2022; a média de 2022 ({sg(P['erro_margem_2022_medio'])}) é puxada por dois institutos fora da curva (média sem os extremos: {sg(P['erro_margem_2022_sem_extremos_media'])}). **→ O título e o texto passaram a dizer que o erro típico foi parecido nos dois anos.**
2. **"Dois terços da virada só apareceram na urna."** O primeiro rascunho dizia isso a partir da média ({f1(pv['media']['pct_da_virada_urna'])}% da virada visível nas pesquisas). Pela média aparada são {f1(pv['media_aparada']['pct_da_virada_urna'])}% e pela mediana {f1(pv['mediana']['pct_da_virada_urna'])}%. **→ A frase saiu; o relatório mostra a faixa e diz que o dado não decide.**
3. **O movimento de campanha de {sg(R['sintese']['pesquisas_e_urna']['margem_media_das_pesquisas_semanais']['movimento_na_campanha'])} ponto depende da correção de instituto?** Sem a correção são {sg(rv['campanha_sem_correcao_de_instituto']['movimento'])}; por instituto, {rv['campanha_por_instituto']['institutos_com_movimento_positivo']} de {rv['campanha_por_instituto']['institutos']} institutos mostram movimento a favor do candidato do PL (de {sg(rv['campanha_por_instituto']['movimento_minimo'])} a {sg(rv['campanha_por_instituto']['movimento_maximo'])}). **Aguenta.**
4. **O erro de 2026 aguenta deixar um instituto de fora?** Média de {sg(rv['erro_2026_sem_um_instituto']['media_min'])} a {sg(rv['erro_2026_sem_um_instituto']['media_max'])}; mediana de {sg(rv['erro_2026_sem_um_instituto']['mediana_min'])} a {sg(rv['erro_2026_sem_um_instituto']['mediana_max'])}. **Aguenta.**
5. **A fração dos "outros" que ficou com o candidato do PL inclui como os indecisos se distribuíram.** Com só os cinco institutos mais conhecidos (Datafolha, MDA, PoderData, Quaest, Real Time): média de {f1(100 * rv['fracao_pl_so_5_institutos_conhecidos']['fracao_media'])}%, mínima de {f1(100 * rv['fracao_pl_so_5_institutos_conhecidos']['fracao_minima'])}%. **→ O texto passou a dizer, ao lado do número, que ele inclui os indecisos.**
6. **"A queda de Flávio com as mensagens de Vorcaro se recuperou."** Estava no primeiro rascunho. A média semanal ficou abaixo do patamar anterior por meses. **→ Corrigido para "durou meses", com as semanas.** Leave-one-out: mediana de {sg(rv['V17_sem_um_instituto']['mediana_min'])} a {sg(rv['V17_sem_um_instituto']['mediana_max'])}, mesmo sinal em todas as exclusões.

## Passada 2: o leitor que mais desconfiaria de uma conclusão favorável a Lula

1. **A investigação de Lulinha.** A mediana de {sg(R['h4']['tamanhos_mediana_de_todos_os_testados']['V19']['mediana_todos_os_institutos'])} ponto é pequena e muda com o limiar (4, 2 ou 1 institutos). Sem um instituto, vai de {sg(rv['V19_sem_um_instituto']['mediana_min'])} a {sg(rv['V19_sem_um_instituto']['mediana_max'])}. **→ O texto diz "depende do limiar" em todos os lugares.**
2. **A economia.** "Os indicadores melhoraram e Lula perdeu votos" pode soar como se a economia não importasse. É descritivo; H2 não foi testada. **→ A leitura diz que o projeto não responde se o desempenho do governo pesou.**
3. **A estimativa ecológica de quem não votou em 2022.** O fluxo "abstenção de 2022 para Flávio" ({f1(100 * R['a4']['fluxo']['abst22_para_flavio26']['B_enxuto'])}%) poderia ser lido contra Lula; varia de {f1(100 * R['a4']['fluxo']['abst22_para_flavio26']['min_regioes'])}% a {f1(100 * R['a4']['fluxo']['abst22_para_flavio26']['max_regioes'])}% entre as regiões. **→ Fica fora das conclusões, marcado como instável.**
4. **Religião.** O resultado (a virada foi menor onde há mais evangélicos) é contrário ao que se espera e poderia parecer favorável a um lado. Pensei em "efeito teto" e testei: controlando pelo voto de Jair em 2022 o coeficiente vai de {f3(ctl['religiao_sem_controle']['coef'])} a {f3(ctl['religiao_com_jair22']['coef'])} (p = {f3(ctl['religiao_com_jair22']['p'])}). **→ O texto que dizia "compatível com teto" saiu; o relatório diz que o sinal permanece e que o desenho não separa o porquê.** Envelhecimento do eleitorado: de {f3(ctl['idade_sem_controle']['coef'])} a {f3(ctl['idade_com_jair22']['coef'])}, também permanece.
5. **Simetria da lista de episódios.** Confirmados por duas reportagens: {sim['lula_governo'][0]} com alvo no governo, {sim['flavio_oposicao'][0]} com alvo em Flávio e a oposição, {sim['ambos'][0]} dos dois lados. Sem confirmação saíram {sim['lula_governo'][1]}, {sim['flavio_oposicao'][1]} e {sim['ambos'][1]}, respectivamente. A remoção não favorece um lado.
6. **"Os dois episódios movem a margem em tamanhos parecidos."** Estava no primeiro rascunho do veredito; os números são {sg(R['h4']['tamanhos_mediana_de_todos_os_testados']['V17']['mediana_todos_os_institutos'])} e {sg(R['h4']['tamanhos_mediana_de_todos_os_testados']['V19']['mediana_todos_os_institutos'])}. **→ Corrigido: o das mensagens é maior em módulo, e a soma é desfavorável ao candidato do PL.**

## Passada 3: método e linguagem (teste do espelho)

- **Palavras proibidas, travessão e adjetivo sem medida:** `ferramentas/conferir-linguagem.py` nos textos públicos: {lint}. "Venceu a eleição" só aparece na negação.
- **Causa:** o texto usa "coincide com", "consistente com" e "não separa". Ocorrências de "causou", "provocou", "fez com que", "por causa de" ou "devido a" nos textos públicos: {len(causas)}{' (' + ', '.join(causas) + ')' if causas else ''}.
- **Tamanhos somados:** nenhum. O placar diz que não se somam, e o "principal fator" saiu como empate entre duas hipóteses que ocupam a mesma janela de tempo.
- **Placebo:** toda associação por lugar vem com o placebo de 2018 a 2022; H13 e H8 foram lidas pelo que o placebo mostra.
- **Teste do espelho aplicado a cada frase do veredito:** a tabela está no fim de `docs/LEITURA_DA_IA.md`.
- **Fatos sem duas fontes:** as datas dos episódios têm duas reportagens capturadas (`dados/CAPTURAS.csv`); onde não houve, o episódio saiu.

## Segunda revisão: só o texto do veredito

1. **Número no veredito que não está no dossiê:** nenhum (o veredito e o dossiê saem do mesmo `RESUMO.json`).
2. **Afirmação de causa:** a frase "sem a qual a virada não aconteceria" sobre a base herdada é uma condição lógica (o candidato do PL precisava de um piso para chegar a 47%), não uma causa medida. **→ Mantida, com a leitura "base" separada de "virada" no §6.2 do plano.**
3. **Teste do recorte:** nenhuma frase isolada serve de material de campanha de um lado só; as três que poderiam (as mensagens de Flávio com Vorcaro, a investigação de Lulinha e o erro das pesquisas) vêm sempre ao lado da sua contraparte.
4. **Previsão do 2º turno:** nenhuma.

## O que a revisão não resolveu

- A regra "evidência forte" para H4 e H6 vale para movimento da série no momento certo em dois ou mais institutos; **o placar não consegue dizer que o movimento foi causado pelo evento**, e o veredito não diz.
- A5, A6, B5, H2, H5, H10 e H14 ficaram sem teste (condições do §10 do pré-registro).
- O júri de cinco leituras do Claude (opcional no plano) **não foi feito**.
- A inferência ecológica tem solução na borda; os intervalos de reamostragem subestimam a incerteza. Só os fluxos estáveis entram.

## Erros de método achados na execução e corrigidos

| # | O que estava errado | Como foi achado | O que mudou |
|---|---|---|---|
| 1 | o arquivo nacional do perfil do eleitorado repetia os estaduais, e o total saía em dobro | conferência contra o eleitorado apto | só os estaduais |
| 2 | códigos de idade de 16 a 20 anos e de 100 anos ou mais estavam fora do mapa | as parcelas de idade não somavam 1 | mapa refeito |
| 3 | o limiar de "movimento normal" exigia 4 variações, mínimo que o pré-registro não pedia; 7 de 9 institutos ficaram sem limiar | leitura da tabela por instituto | regra literal (emenda 3) |
| 4 | o registro de pesquisas do TSE só tem pesquisa registrada a partir de 1º/jan/2026 | 39 pesquisas de 2025 sem casamento | emenda 1 |
| 5 | critério de estabilidade da A4 deixava passar fluxo com valor nacional fora do intervalo das regiões | tabela de estabilidade | terceiro critério (emenda 8) |
| 6 | dois municípios de MG com diferença de 559 votos entre comparecimento e soma de votos | as linhas de probabilidade não somavam 1 | branco e nulo como resíduo, dito |
| 7 | as linhas do gráfico de prefeituras usavam outro peso que o estimador e mostravam um salto maior que o efeito | leitura do gráfico | mesmo núcleo do estimador |
| 8 | quatro afirmações do veredito sem lastro (recuperação do episódio das mensagens, dois terços na urna, tamanhos parecidos dos episódios, efeito teto) | leitura crítica e passadas 1 e 2 | corrigidas ou removidas |
| 9 | datas: o fim das sanções Magnitsky foi em 12/12/2025 (a lista dizia 2026); a Record anunciou o cancelamento do debate em 23/09 | confirmação por duas reportagens | datas corrigidas |
| 10 | o analisador da tabela de pesquisas tratava a coluna "Others" como candidato | contagem de colunas | filtro por título do link |
"""
    (RAIZ / "docs" / "REVISAO_ADVERSARIAL.md").write_text(tx, encoding="utf-8")
    print("ok", len(tx.splitlines()), "linhas")


if __name__ == "__main__":
    main()
