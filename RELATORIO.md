# Relatório: presidente, 1º turno de 2026

> **O que este projeto não diz.** Em quem cada pessoa votou, nem por que votou: tudo aqui é entre municípios, instituições e datas. Intenção de ninguém. **Quem vai ganhar o 2º turno** (25/10/2026): nenhuma previsão. Se as pesquisas foram "tendenciosas": a palavra não entra, e o que se mede é erro e direção do erro. O peso das **redes sociais**, da **avaliação do governo**, da **economia no bolso do eleitor** e do **gasto de campanha**: não foi possível testar com dado público (seção 9). Causa onde o desenho só mostra coincidência. **Flávio Bolsonaro terminou o 1º turno em primeiro; ele não venceu a eleição.**

**Quem fez a análise.** Claude Sonnet 5.5 (Anthropic), no Claude Code (aplicativo para computador), em 07/out/2026; o planejamento e a validação do plano foram do Claude Opus 5.5, na mesma sessão de trabalho. O autor montou e dirigiu o processo; as leituras e o veredito são do Claude e vêm marcados. Os testes e os limiares foram escritos e gravados em commit (`014e6b7`) **antes** de qualquer análise (`docs/PRE_REGISTRO.md`); as emendas, cada uma com "antes ou depois de ver o resultado", estão na §12 de lá. Todo número deste texto sai de `resultados/RESUMO.json`.

## Em dez achados

1. Flávio Bolsonaro (PL) terminou o 1º turno em primeiro, com 47,03% dos votos válidos (arquivo oficial), e Lula (PT) com 45,16%. O 2º turno é em 25/10/2026. Em 2022, Lula terminou o 1º turno 5,23 pontos na frente do candidato do PL; em 2026, o candidato do PL terminou 1,87 na frente: uma **virada de 7,10 pontos** na margem.
2. A virada se divide quase ao meio: o candidato do PL ganhou 3,83 pontos e Lula perdeu 3,27. Em votos, são 5,03 milhões a mais para um e 3,38 milhões a menos para o outro.
3. Ela veio de todas as regiões e é um fenômeno do interior: Sudeste 37,9%, Nordeste 23,5%, Sul 22,4%, Centro-Oeste 8,9%, Norte 7,3%; interior 90,4%, capitais 9,6%.
4. Quase todo o ganho foi **troca de voto dentro dos municípios** (93,2% do ganho do candidato do PL), e não comparecimento (-3,8%). A abstenção quase não mexeu (20,9% para 21,1%).
5. A **base é herdada**: a correlação entre o voto em Jair em 2022 e em Flávio em 2026, município a município, é 0,98, e a estimativa ecológica põe cerca de 97,1% dos eleitores de Jair em Flávio (estável entre regiões e especificações).
6. A média das pesquisas (instituto a instituto corrigida) manteve **Lula à frente até a última semana** (-1,5 ponto de margem), e **subiu 6,9 pontos a favor de Flávio entre 3/ago e 28/set**. Todos os 7 institutos verificados subestimaram o candidato do PL na última pesquisa (erro da margem: mediana -4,2, média -4,7); em 2022 foi parecido (mediana -4,5, 11 de 13 institutos).
7. Nas três últimas semanas, os outros candidatos encolheram em todos os institutos que mais pesquisaram, e da última pesquisa à urna perderam 4,2 pontos; o candidato do PL ficou com mais da metade dessa queda em 7 de 7 institutos e Lula em 0. Em 2022 os outros também encolheram, e o candidato do PL ficou com mais da metade em 9 de 13.
8. **Episódios dos dois lados.** As mensagens de Flávio com Daniel Vorcaro (13/05) coincidem com uma queda de 5,4 pontos na margem do candidato do PL (mediana entre os institutos); a média semanal ficou em -9,0 entre as semanas de 18/05 e 27/07, contra -4,3 nas semanas anteriores, e só voltou ao patamar anterior na semana de 14/09; a autorização do STF para investigar Lulinha (30/07) coincide com +1,2 ponto (mediana), um movimento que depende do limiar usado; os cinco episódios de setembro juntos coincidem com +4,5, mas misturam alvos dos dois lados e só 3 institutos têm par de pesquisas.
9. **Por lugar, quatro hipóteses não se sustentam:** a virada foi menor onde há mais evangélicos; o envelhecimento do eleitorado não a explica (e o padrão aparece também no placebo de 2018 a 2022); quem ganhou a prefeitura por pouco em 2024 não se distingue de quem perdeu; e os estados com governador apoiador de Flávio não tiveram virada diferente dos de governador apoiador de Lula.
10. **O que não dá para testar com dado público:** avaliação do governo, voto econômico no nível do eleitor, pauta, redes sociais, tabelas por grupo de eleitor e gasto de campanha. Os indicadores nacionais melhoraram entre 2022 e 2026 (desocupação de 9,3% para 5,4% no 2º trimestre; renda real do trabalho +19,2%), o que é um fato descritivo e não um teste.

## 1. O resultado (A1)

|  | 2018 | 2022 | 2026 |
|---|---|---|---|
| Candidato do PL | 46,0% | 43,2% | 47,0% |
| Lula (ou Haddad) | 29,3% | 48,4% | 45,2% |
| Outros | 24,7% | 8,4% | 7,8% |
| Margem (PL menos PT), pontos | +16,8 | -5,2 | +1,9 |
| Abstenção, com o exterior | 20,3% | 20,9% | 21,1% |

Fonte: soma dos boletins de urna (projeto `apuracao-eleicoes-2026`), conferida contra o resultado oficial do TSE por município: 2022 em 34.506 de 34.506 pares município-candidato; 2026 em 34.530 de 34.542 pares município-candidato (diferença total de 3.926 votos, de seções sem boletim publicado). Os 47,03% e 45,16% citados acima são do arquivo oficial nacional; a soma dos boletins dá 47,0% e 45,2%.

Estados com a maior virada: TO (+13,4), RS (+13,3), MT (+10,5). Com a menor: AP (+2,2), RR (+1,7), DF (-1,6). Tabela completa em `resultados/a1_uf.csv`.

## 2. Onde está a virada (A2)

Decomposição exata da mudança da margem em contribuição de cada grupo de municípios (deslocamento e participação; a soma dá 7,10 pontos em todas as quatro formas).

| Região | Margem 2022 | Margem 2026 | Contribuição à virada (pontos) | % da virada |
|---|---|---|---|---|
| Sudeste | +4,9 | +11,7 | 2,69 | 37,9% |
| Nordeste | -39,8 | -32,9 | 1,67 | 23,5% |
| Sul | +17,8 | +28,8 | 1,59 | 22,4% |
| Centro-Oeste | +15,9 | +23,9 | 0,63 | 8,9% |
| Norte | -1,6 | +4,5 | 0,52 | 7,3% |
| Exterior | -5,6 | -4,1 | 0,00 | 0,0% |

| Porte do município | Contribuição (pontos) | % da virada |
|---|---|---|
| 100 a 500 mil | 1,71 | 24,0% |
| 20 a 100 mil | 2,44 | 34,4% |
| acima de 500 mil | 1,00 | 14,0% |
| ate 20 mil | 1,95 | 27,4% |

Leitura: nenhuma região e nenhuma faixa de tamanho de cidade carrega a virada sozinha. As cidades de 20 a 100 mil habitantes e as de até 20 mil somam 61,8%; as acima de 500 mil, 14,0%. O efeito de composição (mudança do peso de cada grupo) é pequeno (-0,34 ponto por região); o que mudou foi a margem dentro de cada grupo.

## 3. Troca de voto ou comparecimento (A3)

Para cada município, a variação de votos de 2022 para 2026 se decompõe, na ordem, em crescimento do eleitorado apto, variação do comparecimento, variação da fração de votos válidos e variação da **parcela do candidato** entre os válidos (a troca líquida de voto). A soma é exata; a ordem inversa dá o intervalo.

- Candidato do PL: 5.028.158 votos; parcela do candidato 4.686.605 (93,2% na ordem principal, 92,1% na inversa); comparecimento -188.579; eleitorado apto 691.341.
- Lula: -3.382.476 votos; parcela do candidato -4.115.709 (121,7% da perda); comparecimento 38.570; eleitorado apto 976.309.
- Se cada município tivesse a taxa de comparecimento de 2022, a margem de 2026 seria +1,96 em vez de +1,86: o comparecimento muda a margem em 0,10 ponto.

## 4. Para onde foi o voto de 2022 (A4, inferência ecológica)

Regressão ecológica com restrições, 5.570 municípios, 300 reamostragens. **É uma estimativa entre lugares: não diz em quem ninguém votou.** As soluções ficam muitas vezes na borda (muitos zeros exatos) e os intervalos de reamostragem subestimam a incerteza real; por isso só entra como resultado o fluxo que passa em três critérios (as duas especificações diferem em até 3 pontos, as cinco regiões variam até 15 pontos e o valor nacional fica dentro do intervalo das regiões).

| Fluxo | Estimativa | Intervalo entre as 5 regiões | Estável? |
|---|---|---|---|
| eleitores de Jair 2022 que aparecem em Flávio | 97,2% | 89,2% a 100,0% | sim |
| eleitores de Lula 2022 que aparecem em Flávio | 1,9% | 0,0% a 12,2% | sim |
| eleitores de Jair 2022 que aparecem na abstenção | 1,5% | 0,0% a 5,9% | sim |
| eleitores de Ciro, Tebet e outros de 2022 que aparecem em Caiado | 14,2% | 9,2% a 14,6% | sim |
| eleitores de Ciro, Tebet e outros de 2022 que aparecem em Renan Santos | 23,4% | 9,8% a 24,1% | sim |
| eleitores de Lula 2022 que aparecem em Lula | 93,3% | 70,2% a 93,2% | não |
| abstenção de 2022 que aparece em Flávio | 14,4% | 0,0% a 29,5% | não |

Composição do voto de Flávio na especificação ampla: 89,6% de eleitores de Jair de 2022, 8,4% do grupo que não votou em 2022 (inclui eleitores novos e o efeito de quem saiu do cadastro), 2,0% de eleitores de Lula de 2022. **Os fluxos de e para a abstenção e o de Lula para Lula não são estáveis entre regiões**, e a base de eleitores muda entre 2022 e 2026 (mortes, novos títulos), o que a regressão trata como transição. O fluxo que se sustenta é o da herança.

## 5. As pesquisas e a reta final (B)

**Como a série foi montada.** 170 pesquisas na tabela da Wikipédia (que cita a fonte de cada linha). Todas as 131 de 2026 aparecem no registro de pesquisas do TSE (instituto e data); as 39 de 2025 não têm como aparecer (a lei só exige registro no ano eleitoral) e entram só se a fonte citada confirma os valores; 4 saíram por não conferir. Conferência na fonte: amostra sorteada de 20, 19 conferem; véspera, 11 de 14. A véspera sem fonte que confere fica na série, marcada, e fora do cálculo de erro.

**Trajetória (B1).** Margem média semanal do candidato do PL menos Lula, com cada instituto corrigido pelo próprio desvio: -26,2 na semana de 01/12/2025, -8,4 em 3/ago e -1,5 em 28/set. Nenhuma semana teve o candidato do PL à frente. A urna deu +1,9.

**Erro por instituto (B2).** Na última pesquisa de cada instituto, o candidato do PL foi subestimado em todos os 7 institutos verificados de 2026 e em 11 de 13 de 2022; em 2018 o erro foi de +0,3 (sem direção). O erro da margem foi de mediana -4,2 e média -4,7 (intervalo de 90% da média: -6,2 a -3,3) em 2026, e de mediana -4,5 e média -2,0 em 2022; a média de 2022 é puxada por dois institutos muito fora da curva (média sem os dois extremos: -3,4). **O erro típico de 2026 foi do tamanho do de 2022, não maior.**

| Instituto | Fim do campo | Lula (válidos) | Flávio (válidos) | Erro da margem (pontos) |
|---|---|---|---|---|
| Datafolha | 2026-10-03 | 45,2 | 43,0 | -4,0 |
| Indexa | 2026-09-29 | 43,8 | 38,2 | -7,5 |
| MDA | 2026-10-02 | 47,7 | 42,1 | -7,5 |
| PoderData | 2026-10-02 | 44,7 | 43,6 | -2,9 |
| Quaest | 2026-10-03 | 46,0 | 43,7 | -4,2 |
| Real Time | 2026-09-30 | 45,7 | 41,5 | -6,1 |
| Vox Brasil | 2026-10-01 | 45,0 | 45,9 | -1,0 |

**Quanto da virada as pesquisas mostravam.** Entre as vésperas de 2022 e de 2026, a margem das pesquisas andou 4,3 pontos pela média (60,8% da virada de 7,10), 5,6 pela média aparada (78,7%) e 7,5 pela mediana (105,4%). **O dado não permite dizer qual fração apareceu só na urna**; a resposta depende do resumo usado.

**Os outros candidatos (B3).** Da última pesquisa verificada à urna, os outros caíram 4,2 pontos (intervalo de 90%: 2,6 a 6,0); o candidato do PL ficou com 116,2% dessa queda em média (mediana 100,0%). Isso inclui como os indecisos se distribuíram, porque o valor válido da pesquisa tira os indecisos em proporção. Nas três últimas semanas, em cada um dos 5 institutos com mais rodadas, os outros encolheram (começo da janela: de 12,4% a 19,3% dos válidos; fim: de 9,0% a 14,8%), e a margem do candidato do PL melhorou em 4 deles. A comparação por município de 2022 para 2026 (B3c) não mostra o mesmo padrão: onde os outros caíram mais, foi Lula, não o candidato do PL, que mais ganhou (coeficiente de Lula sobre a queda dos outros -1,12; do candidato do PL +0,12); mas os "outros" de 2022 (Ciro, Tebet) e de 2026 (Caiado, Cury, Renan) são pessoas diferentes.

**Decomposição do erro (B4).** Só 3 institutos têm última pesquisa verificada e pelo menos 3 pesquisas em 21 dias. Neles o erro médio da margem foi de -3,7; a parte consistente com mudança de última hora (extrapolação da tendência do instituto) foi de +0,7 e o resíduo de -4,5. A parte atribuível a comparecimento diferencial não pôde ser medida (exigiria pesquisa por UF).

## 6. Episódios dos dois lados (H4)

Lista fechada em commit antes das séries (`dados/eventos.csv`); 13 dos 25 episódios tiveram a data confirmada em duas reportagens (`dados/eventos_confirmados.csv`, capturas em `dados/CAPTURAS.csv`) e 12 saíram, como o pré-registro manda. O alvo de cada episódio é quem o fato trata, não quem ele "ajudaria".

| Id | Episódio | Data | Alvo |
|---|---|---|---|
| V01 | INSS: operação da PF e da CGU sobre descontos em benefícios | 2025-04-23 | lula_governo |
| V02 | IOF: decreto do governo e derrubada pelo Congresso | 2025-06-25 | lula_governo |
| V03 | Tarifa dos EUA e sanções da Lei Magnitsky ao ministro Alexandre de Moraes | 2025-07-30 | flavio_oposicao |
| V04 | Condenação de Jair Bolsonaro pela 1ª Turma do STF | 2025-09-11 | flavio_oposicao |
| V09 | Mensagens entre Daniel Vorcaro e o ministro Alexandre de Moraes divulgadas e crise do STF (1 a 15 de setembro) | 2026-09-01 | lula_governo |
| V12 | Fim das sanções da Lei Magnitsky ao ministro | 2025-12-12 | ambos |
| V16 | Fala de Flávio sobre desistir em troca de favores e retratação | 2025-12-07 | flavio_oposicao |
| V17 | Banco Master: relações de Flávio Bolsonaro com Daniel Vorcaro | 2026-05-13 | flavio_oposicao |
| V19 | INSS: investigação de Fábio Luís Lula da Silva e do chefe de gabinete Marco Aurélio Santana | 2026-07-30 | lula_governo |
| V21 | Debate da Record cancelado sem Lula e Flávio | 2026-09-23 | ambos |
| V23 | Nossa Senhora Aparecida: reportagem da GloboNews e reação de Flávio e da CNBB | 2026-09-24 | flavio_oposicao |
| V26 | Lula avisa que não vai ao debate da Globo | 2026-09-30 | lula_governo |
| V27 | TV Globo cancela o debate e Flávio desiste de comparecer | 2026-10-01 | ambos |

Teste (pré-registro, §5): por instituto com 8 ou mais rodadas, a mudança da margem entre a última pesquisa antes e a primeira depois do episódio (ou do grupo de episódios a menos de 30 dias um do outro), com par a até 45 dias e o mesmo número de candidatos; o movimento é "acima do normal" se passa do percentil 95 das variações do próprio instituto fora das janelas de episódio; coincide com movimento quando 2 ou mais institutos passam, no mesmo sentido.

| Episódio | Alvo | Institutos com par | Mediana (pontos) | Acima do normal (regra literal) | pelo p95 agrupado | pelo limiar amostral | Leitura |
|---|---|---|---|---|---|---|---|
| 13/05, mensagens Flávio-Vorcaro | Flávio | 6 | -5,4 | 4 | 4 | 2 | coincide, no sentido esperado |
| 30/07, STF autoriza investigar Lulinha | Lula e governo | 9 | +1,2 | 4 | 2 | 1 | coincide, no sentido esperado; **depende do limiar** |
| Setembro (V09, V21, V23, V26, V27) | dos dois lados | 3 | +4,5 | 2 | 1 | 1 | coincide, sem sentido esperado |

As duas colunas de sensibilidade foram definidas **depois** de ver as diferenças por instituto (emenda 3). V16 e V12 (dezembro de 2025) não têm instituto com par antes e depois. **Os episódios de 2025 (V01 a V04) não foram testados**, porque dependiam da série de avaliação do governo, que não alcança as 8 medições exigidas. Sem confirmação de data saíram 12 episódios, entre eles os de ministros do STF no caso Master anteriores a setembro, o da Operação Contenção e o das sanções e tarifas de 2026.

Efeito não é causa: "coincide com movimento" quer dizer que a série se moveu além do normal naquela janela. O movimento depois das mensagens de Flávio com Vorcaro **durou meses**: a média semanal foi de -4,3 entre 30/03 e 11/05, de -9,0 entre 18/05 e 27/07, e só voltou a esse patamar anterior na semana de 14/09, já na campanha.

## 7. Por lugar (H1, H3, H7, H8, H9, H13)

Todas as regressões usam o município como unidade, peso pelos válidos de 2026, efeito fixo de UF e erro agrupado por UF; o placebo repete a regressão sobre a virada de 2018 para 2022. Lugar não é pessoa.

| Hipótese | Resultado | Placebo 2018-2022 | Sem os 5 maiores estados | Passa a correção de Benjamini-Hochberg? |
|---|---|---|---|---|
| H8, evangélicos (por desvio-padrão de 10,3 pontos) | -1,21 (p = 0,003) | +1,71 | -1,04 | sim |
| H13, mais eleitores com 60 anos ou mais | -0,68 (p = 0,005) | -1,19 | -0,54 | sim |
| H13, mais eleitores de 16 a 24 anos | +0,42 (p = 0,241) | +1,46 | +0,86 | não |
| H13, mais eleitores com superior | -0,34 (p = 0,243) | -0,05 | -0,03 | não |
| H7, descontinuidade em prefeituras de 2024 (n = 477) | +1,39 (p = 0,147) | +1,15 | n/a | não |
| H3, mudança da desocupação por UF (27 pontos, por ponto percentual) | +1,06 (p = 0,016) | +0,47 | n/a | sim |

- **H1 (herança):** correlação ponderada de 0,98 entre Jair 2022 e Flávio 2026 (de 0,96 entre Jair 2018 e Jair 2022; de 0,98 para Lula). A virada tem correlação de -0,09 com o voto em Jair de 2022: ela se espalha por todo o mapa, com um pouco mais de força onde Jair tinha menos (virada média de 8,6 pontos onde Jair tinha até 25%, 6,7 onde tinha mais de 65%).
- **H8 (religião):** o sinal é **contrário** ao da hipótese. Onde há mais evangélicos, a virada foi menor. O sinal permanece ao controlar pelo voto de Jair em 2022 (-1,01, p = 0,024), então não é só efeito teto (quem já tinha muito voto sobraria menos para subir). O sinal oposto no placebo de 2018 a 2022 mostra que, em 2022, Jair ganhou mais onde havia mais evangélicos; o que o desenho não separa é por que isso se inverteu.
- **H13 (renovação do eleitorado):** onde o eleitorado envelheceu mais, a virada foi menor, e o placebo repete o padrão (sinal igual, tamanho maior); sem efeito fixo de UF o sinal some. A variação média ponderada de eleitores com 60 anos ou mais foi de +2,7 ponto e a de 16 a 24 anos, -1,7: se há efeito de composição, ele ajudaria Lula, não Flávio. Sem pesquisa por idade (A6), a evidência não passa de fraca.
- **H7 (máquina local):** 477 municípios na janela de 5 pontos (259 com direita vencedora e 218 com direita perdedora); o efeito de +1,39 ponto está dentro do intervalo do placebo. Poder suficiente (mais de 200 municípios). A variante só com o PL, janela de 5 pontos: +0,97 (p = 0,551).
- **H9 (governadores aliados):** virada média de 8,5 pontos nas 10 UFs com governador apoiador de Flávio e de 7,6 nas 5 com governador apoiador de Lula; diferença de +0,8 (p de permutação 0,626).
- **H3 (economia):** descritivo nacional, não é teste. Desocupação de 9,3% no 2º trimestre de 2022 para 5,4% no de 2026 (mínimo de 5,1% no 4º trimestre de 2025); renda real do trabalho de R$ 3.136 para R$ 3.738 (+19,2%); inflação em 12 meses de 4,1% (set/2022) para 3,1% (set/2026), e a de alimentos de 9,5% para 3,5%; Selic meta de 13,75% em out/2022 e 13,75% em set/2026 (chegou a 15,00% no período). Entre as 27 UFs, a virada foi maior onde a desocupação caiu menos (p = 0,016), mas o placebo não confirma e 27 pontos são poucos.
- **H11 (por que Flávio e não outro nome):** nos cenários de pesquisa, Caiado, Zema e Ratinho Júnior rendiam muito menos que Flávio contra Lula; Tarcísio rendia perto (diferença média de +0,8 ponto no 4º trimestre de 2025) e passou a render menos (diferença de -4,8 no 1º de 2026). Michelle Bolsonaro não está nos dados coletados.

## 8. O placar

| Hipótese | Nome | Situação | Evidência | Confiança |
|---|---|---|---|---|
| H1 | Herança e identidade (a base) | consistente | forte para a base | alta |
| H2 | Referendo sobre o governo | não testável | não testável | baixa |
| H3 | Economia | inconsistente (descritivo) | fraca | baixa |
| H4 | Episódios e eventos dos dois lados | consistente em parte | forte pela regra literal; depende do limiar (Lulinha) | média |
| H5 | Pauta | não testável | não testável | baixa |
| H6 | Consolidação e voto útil da direita | consistente | forte (movimento na série e aritmética pesquisa-urna em vários institutos) | média |
| H7 | Máquina local (prefeitos de 2024) | inconsistente | desenho causal sem efeito detectado | média |
| H8 | Religião e valores | inconsistente | fraca | média |
| H9 | Governadores aliados | inconsistente | fraca | baixa |
| H10 | Estrutura de campanha | não testável | não testável | baixa |
| H11 | O candidato (por que Flávio e não "a direita") | consistente em parte | fraca | baixa |
| H12 | Comparecimento | inconsistente | forte (conta exata) | alta |
| H13 | Renovação do eleitorado | inconsistente (envelhecimento) | fraca (o placebo repete o padrão) | baixa |
| H14 | Redes sociais | não testável | não testável | baixa |

O detalhe de cada linha e o veredito estão em `docs/LEITURA_DA_IA.md`. Os tamanhos não se somam: as hipóteses se sobrepõem.

## 9. O que ficou de fora, e por quê

- **A5:** a renda por setor censitário não está publicada pelo IBGE na pasta de agregados por setor (lista de 20/mai/2026, sem arquivo de rendimento); não executa.
- **A6:** não foram coletadas tabelas por grupo de pelo menos 2 institutos nos dois anos; não executa.
- **B5:** não foram coletadas 5 medições de rejeição do mesmo instituto em 2026; não executa.
- **Episódios de 2025:** V01 a V04 ficam sem teste: dependem da série de avaliação do governo (H2).
- **H10:** propaganda gratuita e gasto parcial não foram coletados em formato legível por máquina; não executa.
- **H14:** redes sociais: sem dado público confiável; não testável.
- **H2:** a única série estruturada de avaliação do governo (Wikipédia) termina em nov/2025 e tem no máximo 6 medições por instituto, abaixo das 8 exigidas; não executa. A comparação dos cinco presidentes também não foi montada.
- **H3 por município:** o Bolsa Família de agosto de 2022 por município não está nas URLs públicas de download; só a parte por UF (PNAD) e o quadro descritivo nacional foram feitos.
- **H5:** não foram coletadas 5 medições do "principal problema" do mesmo instituto em 2026; não executa.

## 10. Conferências e erros achados

- Votos por município contra o resultado oficial do TSE: 2018, 2022 e 2026 (seção 1).
- **Recontagem independente** (`ferramentas/validacao-independente.py`, código novo e outras fontes): 13 de 13 números conferem, com diferença máxima de 0,004 ponto e de 1,8 mil votos.
- Perfil do eleitorado contra o eleitorado apto dos boletins: diferença total de 0,000% (2022) e 0,004% (2026).
- Testes automáticos (`python -m pytest -q`) e conferência de linguagem (`ferramentas/conferir-linguagem.py`).
- Erros achados no caminho e corrigidos estão em `docs/CORRECOES.md`; a revisão adversarial, em `docs/REVISAO_ADVERSARIAL.md`.

## 11. Como refazer

`docs/REPLICAR.md`. Os dados por seção e por município vêm de dois projetos anteriores, lidos por hash (`dados/FONTE_APURACAO.json`, `dados/FONTE_CONGRESSO.json`); os dados novos estão em `dados/MANIFESTO.json`.
