# Revisão adversarial

**Feita em 07/out/2026 pelo Claude, depois da análise e antes do veredito, e repetida sobre o texto do veredito.** Duas das checagens abaixo (o efeito de teto e o deixar um instituto de fora) viraram números em `resultados/RESUMO.json` (chave `revisao`, `ferramentas/revisao-adversarial.py`). Esta revisão é do mesmo modelo que fez a análise, **não de uma pessoa**: ela reduz erro de método e de linguagem, mas não substitui um revisor externo.

O que mudou no texto por causa da revisão está marcado com **→**.

## Passada 1: o leitor que mais desconfiaria de uma conclusão favorável ao candidato do PL

1. **"As pesquisas erraram mais contra o PL em 2026 do que em 2022."** Era o título do primeiro gráfico. A mediana do erro da margem é -4,1 em 2026 e -4,5 em 2022; a média de 2022 (-2,0) é puxada por dois institutos fora da curva (média sem os extremos: -3,4). **→ O título e o texto passaram a dizer que o erro típico foi parecido nos dois anos.**
2. **"Dois terços da virada só apareceram na urna."** O primeiro rascunho dizia isso a partir da média (77,6% da virada visível nas pesquisas). Pela média aparada são 95,3% e pela mediana 106,5%. **→ A frase saiu; o relatório mostra a faixa e diz que o dado não decide.**
3. **O movimento de campanha de +6,9 ponto depende da correção de instituto?** Sem a correção são +6,6; por instituto, 6 de 7 institutos mostram movimento a favor do candidato do PL (de -1,0 a +8,7). **Aguenta.**
4. **O erro de 2026 aguenta deixar um instituto de fora?** Média de -4,2 a -3,1; mediana de -4,2 a -4,0. **Aguenta.**
5. **A fração dos "outros" que ficou com o candidato do PL inclui como os indecisos se distribuíram.** Com só os cinco institutos mais conhecidos (Datafolha, MDA, PoderData, Quaest, Real Time): média de 128,0%, mínima de 87,7%. **→ O texto passou a dizer, ao lado do número, que ele inclui os indecisos.**
6. **"A queda de Flávio com as mensagens de Vorcaro se recuperou."** Estava no primeiro rascunho. A média semanal ficou abaixo do patamar anterior por meses. **→ Corrigido para "durou meses", com as semanas.** Leave-one-out: mediana de -5,5 a -5,3, mesmo sinal em todas as exclusões.

## Passada 2: o leitor que mais desconfiaria de uma conclusão favorável a Lula

1. **A investigação de Lulinha.** A mediana de +1,2 ponto é pequena e muda com o limiar (4, 2 ou 1 institutos). Sem um instituto, vai de +0,7 a +1,8. **→ O texto diz "depende do limiar" em todos os lugares.**
2. **A economia.** "Os indicadores melhoraram e Lula perdeu votos" pode soar como se a economia não importasse. É descritivo; H2 não foi testada. **→ A leitura diz que o projeto não responde se o desempenho do governo pesou.**
3. **A estimativa ecológica de quem não votou em 2022.** O fluxo "abstenção de 2022 para Flávio" (14,4%) poderia ser lido contra Lula; varia de 0,0% a 29,5% entre as regiões. **→ Fica fora das conclusões, marcado como instável.**
4. **Religião.** O resultado (a virada foi menor onde há mais evangélicos) é contrário ao que se espera e poderia parecer favorável a um lado. Pensei em "efeito teto" e testei: controlando pelo voto de Jair em 2022 o coeficiente vai de -1,208 a -1,007 (p = 0,024). **→ O texto que dizia "compatível com teto" saiu; o relatório diz que o sinal permanece e que o desenho não separa o porquê.** Envelhecimento do eleitorado: de -0,684 a -0,660, também permanece.
5. **Simetria da lista de episódios.** Confirmados por duas reportagens: 5 com alvo no governo, 5 com alvo em Flávio e a oposição, 3 dos dois lados. Sem confirmação saíram 5, 4 e 3, respectivamente. A remoção não favorece um lado.
6. **"Os dois episódios movem a margem em tamanhos parecidos."** Estava no primeiro rascunho do veredito; os números são -5,4 e +1,2. **→ Corrigido: o das mensagens é maior em módulo, e a soma é desfavorável ao candidato do PL.**

## Passada 3: método e linguagem (teste do espelho)

- **Palavras proibidas, travessão e adjetivo sem medida:** `ferramentas/conferir-linguagem.py` nos textos públicos: 5 arquivos conferidos, 0 achados. "Venceu a eleição" só aparece na negação.
- **Causa:** o texto usa "coincide com", "consistente com" e "não separa". Ocorrências de "causou", "provocou", "fez com que", "por causa de" ou "devido a" nos textos públicos: 0.
- **Tamanhos somados:** nenhum. O placar diz que não se somam, e o "principal fator" saiu como empate entre duas hipóteses que ocupam a mesma janela de tempo.
- **Placebo:** toda associação por lugar vem com o placebo de 2018 a 2022; H13 e H8 foram lidas pelo que o placebo mostra.
- **Teste do espelho aplicado a cada frase do veredito:** a tabela está no fim de `docs/LEITURA_DA_IA.md`.
- **Fatos sem duas fontes:** as datas dos episódios têm duas reportagens capturadas (`dados/CAPTURAS.csv`); onde não houve, o episódio saiu.

## Segunda revisão: só o texto do veredito

1. **Número no veredito que não está no dossiê:** nenhum (o veredito e o dossiê saem do mesmo `RESUMO.json`).
2. **Afirmação de causa:** a frase "sem a qual a virada não aconteceria" sobre a base herdada é uma condição lógica (o candidato do PL precisava de um piso para chegar a 47%), não uma causa medida. **→ Mantida, com a leitura "base" separada de "virada" no §6.2 do plano.**
3. **Teste do recorte:** nenhuma frase isolada serve de material de campanha de um lado só; as três que poderiam (as mensagens de Flávio com Vorcaro, a investigação de Lulinha e o erro das pesquisas) vêm sempre ao lado da sua contraparte.
4. **Previsão do 2º turno:** nenhuma.

## Passada 4 (11/out/2026): o retorno do autor, e o que ele derrubou

O autor leu o roteiro do vídeo e questionou três coisas: se as pesquisas tinham sido cruzadas com as eleições anteriores, instituto por instituto; se a economia descrita batia com a vida real; e se o caso de Nossa Senhora Aparecida era notícia falsa. As três perguntas acharam defeito.

1. **O 2018 da série de pesquisas estava errado.** O código lia, no Pindograma, a coluna com o resultado da urna (`pct`) no lugar da coluna da pesquisa (`valid_result`); por isso 2018 aparecia com erro "perto de zero" e "sem direção". **→ Corrigido em `analise-3`; 2018 passa a ter o voto de Jair subestimado em 8 de 10 institutos.** A versão de 07/out do roteiro dizia "em 2018 o erro ficou perto de zero", e a frase saiu.
2. **Três pesquisas da véspera de 2026 tinham saído da conta por defeito de coleta, não de fonte.** AtlasIntel e Futura publicam o número em PDF; a página da Palver foi salva comprimida e o verificador não descomprimia. As três foram conferidas na fonte original em 11/out e entraram (`dados/CAPTURAS_INSTITUTOS.csv`); a Futura entrou com o número do PDF, diferente da tabela da Wikipédia. Com elas, os institutos verificados de 2026 vão de 7 para 10, e a frase "os 7 institutos subestimaram o candidato do PL" vira "os 10 deram a ele menos voto do que a urna; na diferença, 8 de 10 mostraram o PL pior" (Futura e Palver mostravam Flávio na frente).
3. **"7 de 7" do Datafolha inclui erros pequenos.** Das 7 rodadas desde 2014, em 3 o erro na diferença foi de até 2 pontos (dentro do que a margem de erro explica) e em 4 passou disso. **→ O relatório e o roteiro dizem "às vezes por pouco, às vezes por quase dez pontos".** As rodadas também não são independentes (um mesmo choque de eleição pesa em todos os institutos), então o padrão não vira probabilidade.
4. **A economia de 07/out estava incompleta.** O texto dizia que "os indicadores melhoraram", o que é verdade para o emprego e para a inflação em 12 meses, mas deixava de fora o preço acumulado, a dívida das famílias, as empresas em recuperação judicial e a sensação das pessoas. **→ Emenda 10 e seção 7A do relatório, com 16 trechos conferidos no texto original de fontes que não são do governo (DIEESE, Serasa, Genial/Quaest) além do IBGE e do Banco Central.** A H3 passou de "inconsistente" para "consistente em parte (descritivo)". Teste do outro lado: o autor disse que "tudo ficou pelo menos três vezes mais caro"; na média os índices não mostram isso (a comida em casa subiu 65% desde 2020); para o café, mostram (165% desde 2020). O relatório diz as duas coisas.
5. **Nossa Senhora Aparecida.** O episódio V23 estava descrito como "reportagem da GloboNews e reação de Flávio e da CNBB", sem dizer que a afirmação era falsa. **→ O relatório diz que o TSE manteve fora do ar os posts que ligavam Flávio a ela (30/09).**

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
| 11 | 2018: a série lia o resultado da urna no lugar do da pesquisa | pergunta do autor sobre 2018, 11/out | coluna certa; passada 4 |
| 12 | três pesquisas da véspera de 2026 fora da conta por PDF e página comprimida | pergunta do autor sobre o cruzamento das pesquisas, 11/out | conferidas na fonte original; passada 4 |
| 13 | a economia descrita só pelo emprego e pela inflação em 12 meses | retorno do autor, 10/out | emenda 10, seção 7A |
| 14 | V23 descrito sem dizer que a afirmação era falsa | retorno do autor, 10/out | nota no relatório |
