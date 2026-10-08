# Pré-registro: os testes e os critérios, escritos antes das análises

**Escrito em:** 07/out/2026, em commit antes de qualquer análise. O hash do commit entra no relatório. Critério mudado depois entra na §12, dizendo se foi antes ou depois de ver o resultado.

---

## 0. O que já foi visto antes deste registro (declaração)

Um pré-registro não consegue ser cego à manchete. O que ele garante é que **os testes, os limiares e a definição de "principal fator" estão escritos antes de qualquer conta**. Já foi visto e se declara:

- o resultado nacional do 1º turno de 2026 (arquivo oficial do TSE) e as contas do plano: virada de 7,10 pontos na diferença entre os dois primeiros contra 2022, dividida em 3,83 (candidato do PL) e 3,27 (Lula);
- as pesquisas da véspera do Datafolha e da Quaest e a série do Datafolha de setembro e outubro, e a reportagem de que a maioria dos institutos subestimou Flávio Bolsonaro e de que os votos de Cury, Caiado e Zema migraram na reta final;
- a cronologia da candidatura (aval em dez/2025, convenção em 25/jul/2026) e a não desistência de Zema;
- **a estrutura** (colunas e seções, sem os valores) da tabela de pesquisas da Wikipédia em inglês, e os textos das seções de campanha e controvérsias dos artigos da Wikipédia em português e inglês sobre a eleição, de onde saiu a lista de episódios;
- tudo o que os projetos `apuracao-eleicoes-2026` e `congresso-e-governos-eleicoes-2026` já publicaram, incluindo a resposta de que as pesquisas de governador de 2026 não mostraram a direita mais fraca que a urna.

**Não foi visto:** nenhuma série de pesquisa de presidente além da véspera, nenhuma conta por município da virada, nenhuma matriz de transição, nenhum valor da tabela de pesquisas da Wikipédia, nenhum dado de prefeito de 2024 ou de perfil do eleitorado.

---

## 1. Definições

- **Unidade de comparação entre eleições:** o **município** (código TSE, mesmo `uf` e `mun` em 2018, 2022 e 2026). O voto no exterior (`uf = ZZ`) entra nos totais nacionais e fora das análises por município. A seção só entra **dentro** de 2026. O local de votação só entra se casar por código e coordenada, com a taxa de casamento declarada.
- **Votos válidos:** soma dos votos nominais aos candidatos (sem brancos e nulos). Candidato fora da lista oficial conta como nulo, como no arquivo oficial.
- **Margem:** (candidato do PL ou Jair) menos (Lula), em pontos percentuais dos válidos. **Virada** V = margem de 2026 menos margem do 1º turno de 2022.
- **Abstenção:** com o voto no exterior nos totais nacionais; por município, sem o exterior. A base é dita sempre que o número aparece.
- **Campo de candidato e de partido** (regra de três grupos do autor, de 07/out): direita = direita + centro-direita; centro = só centro; esquerda = esquerda + centro-esquerda, pela autodeclaração dos partidos (Valor Econômico, ago/2026). Candidatos de 2026: direita = Flávio (PL), Renan Santos (Missão), Zema (Novo); centro = Caiado (PSD), Cury (Avante); esquerda = Lula (PT) e os candidatos de PSTU, PCB, UP e PCO; DC e Democrata em "outros". **Sensibilidade:** Caiado na direita. Candidatos de 2022: direita = Jair (PL), Soraya (União), Felipe d'Avila (Novo); centro = Tebet (MDB); esquerda = Lula, Ciro (PDT) e os demais de esquerda.
- **Aliado e prefeito:** governador **por apoio declarado a Flávio ou a Lula** (CNN Brasil e g1, regra de 05/out); prefeito de 2024 **por partido** (não existe apoio declarado a Flávio em 2024). As duas escolhas se declaram no relatório.
- **Valor válido de uma pesquisa:** o percentual de cada candidato dividido por (100 menos branco, nulo e indeciso), quando a pesquisa publica só o total. Conferido contra as pesquisas que publicam os dois (a Datafolha da véspera: 42 e 40 no total, 45 e 42 nos válidos).
- **Janelas:** "véspera" = campo terminado de 28/set a 03/out de 2026 (e de 17/set a 01/out de 2022).

---

## 2. Bloco A · O que aconteceu

**A1 · Resultado.** Votos e percentuais dos válidos de Jair/Flávio, Lula e os demais, em 2018, 2022 e 2026, por UF e região, com a abstenção, os brancos e os nulos. Totais de 2026 conferidos contra o arquivo oficial.

**A2 · Onde está a virada.** Decomposição exata de V em contribuições de região, UF, capital contra interior e porte do município (faixas de população do Censo 2022: até 20 mil, 20 a 100 mil, 100 a 500 mil, acima de 500 mil), pelo método de deslocamento e participação: V = soma de (peso médio × variação da margem) mais soma de (margem média × variação do peso). Reporta-se também a parte "dentro" e a parte "composição".

**A3 · Troca de voto ou comparecimento.** Por município, a variação dos votos de cada candidato entre 2022 e 2026 decompõe-se em quatro termos, nesta ordem: (a) crescimento do eleitorado apto; (b) variação da taxa de comparecimento; (c) variação da fração de votos válidos entre os comparecidos; (d) variação da **parcela do candidato entre os válidos** (a troca líquida de voto). Soma exata. A ordem inversa dos quatro termos é calculada e o intervalo entre as duas ordens vai junto.

**A4 · Para onde foi o voto de 2022.** Regressão ecológica com restrições. Origem (parcelas do eleitorado apto em 2022): Lula, Jair, Ciro, Tebet, outros candidatos, branco e nulo, abstenção. Destino (parcelas do eleitorado apto em 2026): Flávio, Lula, Caiado, Cury, Renan Santos, Zema, outros, branco e nulo, abstenção. Para cada município, y = x · B, com B não negativo e cada linha somando 1; mínimos quadrados ponderados pelo eleitorado apto de 2022. Ajusta-se por **região** (5) e, para os estados com mais de 100 municípios, por **UF**. **Intervalo:** 300 reamostragens dos municípios com semente 20261007. **Conferência:** o total previsto de Flávio, Lula e abstenção em cada ajuste tem de ficar a até 1,0% do total real; se não, o ajuste sai marcado como "não confiável". Limite de nascença: a base muda de 2022 para 2026 (morreu e entrou gente), e isso entra como transição. Resultado dito como **inferência ecológica**, nunca como voto de ninguém.

**A5 · Dentro das cidades (só 2026).** Regressão do voto em Flávio e em Lula por seção contra o perfil do eleitorado da seção (idade, escolaridade, sexo) e a renda do setor censitário do local de votação, com efeito fixo de município. **Condição:** só executa se a renda por setor ou área de ponderação do Censo 2022 estiver publicada e o local de votação tiver coordenada (§10).

**A6 · Entre quem.** Voto de Lula e do candidato do PL por religião, faixa etária, renda e escolaridade na véspera de 2022 e de 2026, em pelo menos 3 institutos, com a margem de cada grupo. **Condição:** só executa se existirem tabelas por grupo, publicadas, de pelo menos 2 institutos nos dois anos (§10). Sem isso, H8 e H13 ficam em evidência no máximo fraca.

---

## 3. Bloco B · A reta final e as pesquisas

**Série de pesquisas.** Fonte: a tabela de pesquisas da Wikipédia em inglês (texto bruto capturado com hash), que cita cada pesquisa. **Entra** a pesquisa que (i) aparece no registro do TSE (`pesquisa_eleitoral_2026`) pelo mesmo instituto e com data de campo até 3 dias de diferença; (ii) tem valores de Lula e de Flávio no mesmo cenário. **Verificação:** 20 pesquisas sorteadas (semente 20261007) são conferidas contra a fonte citada; se mais de 2 divergirem em mais de 1,0 ponto, a série inteira é reconstruída da fonte primária ou a análise B sai. As pesquisas da véspera são conferidas todas, em 2 veículos. Pesquisas que não casam no registro do TSE saem, e a contagem do que saiu vai para o relatório. Pesquisa de instituto com menos de 8 rodadas em 2026 entra no cálculo de média e fora das análises por instituto.

**B1 · Trajetória.** Média móvel de 14 dias, com cada instituto corrigido pelo próprio desvio médio em relação à média de todos os institutos (efeito de casa), de Lula e Flávio nos válidos, de dez/2025 à véspera. Ao lado, a trajetória de 2022 (Lula e Jair), pela base do Pindograma já capturada e pela tabela da Wikipédia de 2022.

**B2 · Erro de cada instituto.** Para cada instituto com pesquisa na véspera de 2018, 2022 e 2026 para presidente: erro de Lula, do candidato do PL e da margem contra o resultado do 1º turno, nos válidos. Mesma conta do Congresso (C4), agora com presidente.

**B3 · A migração da reta final.** (a) Os "outros" na última pesquisa de cada instituto contra os "outros" na urna (7,81%). (b) A série dos últimos 14 dias dos três institutos com mais rodadas. (c) Onde os "outros" caíram mais em relação à média de 2022 (por município), e quanto Flávio e Lula ganharam ali (regressão por município, efeito fixo de UF). (d) A matriz da A4 para as colunas Caiado, Cury, Renan e Zema.

**B4 · Decomposição do erro.** Para a margem de cada instituto na véspera: parte consistente com mudança de última hora (extrapolação linear da tendência do mesmo instituto, limitada ao próprio erro), parte consistente com comparecimento diferencial (correlação do erro da UF com a variação do comparecimento contra 2022, dita como fraca: 27 estados) e resíduo.

**B5 · Rejeição.** Série de rejeição de cada candidato. **Condição:** só executa se existirem pelo menos 5 medições de rejeição de Lula e de Flávio em um mesmo instituto em 2026 (§10).

---

## 4. Bloco C · As hipóteses

Para cada uma: teste, o que **confirmaria** e o que **derrubaria**. **Tamanho** é o teto em pontos de margem que a hipótese explica **sozinha**, pela conta mais generosa a ela, ou "não estimável". **Os tamanhos não se somam** (§7).

**H1 · Herança e identidade (explica a base, não a virada).** Correlação entre municípios do voto em Jair em 2022 e em Flávio em 2026, ponderada por válidos, e a retenção de A4. Confirmaria: correlação acima de 0,85 e retenção de eleitores de Jair em Flávio acima de 85%. Derrubaria: correlação abaixo de 0,6 ou retenção abaixo de 70%. Tamanho: n/a (explica o piso).

**H2 · Referendo sobre o governo.** Dois testes. (i) Dentro de 2026, por instituto com 8 ou mais rodadas: correlação entre a série de avaliação do governo e a do voto em Lula, em primeira diferença. (ii) Comparação, dita como comparação e não como modelo, dos cinco presidentes que tentaram a reeleição (1998, 2006, 2014, 2022, 2026): voto no 1º turno contra avaliação na véspera. Confirmaria: correlação positiva em primeira diferença em 2 ou mais institutos e Lula na linha dos outros quatro. Derrubaria: correlação nula ou negativa, ou Lula fora da faixa dos outros quatro. Tamanho: não estimável.

**H3 · Economia.** (i) Séries nacionais (inflação de alimentos, renda real, desocupação, juros) contra B1: só descritivo, dito como descritivo. (ii) Por município: regressão da virada de 2022 para 2026 contra a variação dos beneficiários do Bolsa Família por 100 habitantes (agosto de 2022 contra agosto de 2026), com efeito fixo de UF. (iii) Por UF: a virada contra a variação da desocupação e da renda do trabalho (PNAD Contínua), 27 pontos, dito como fraco. Confirmaria: coeficiente de (ii) com sinal contrário ao do placebo e BH abaixo de 5%. Derrubaria: sem relação. Tamanho: coeficiente vezes a variação média, em pontos de margem.

**H4 · Episódios e eventos dos dois lados.** O teste está na §5. Confirmaria: o evento move a série além do normal em 2 ou mais institutos, na direção compatível com o alvo do evento. Derrubaria: a série não se move além do normal. Tamanho: soma dos movimentos acima do normal dentro da janela de campanha, em pontos de margem.

**H5 · Pauta.** Série do "principal problema do país" e do assunto mais lembrado, contra os movimentos de B1. **Condição:** só executa se existirem pelo menos 5 medições do "principal problema" em um mesmo instituto em 2026 (§10).

**H6 · Consolidação e voto útil da direita.** (a) Os "outros" caíram na reta final (B3a e B3b)? (b) Para onde foi a diferença (B3c, B3d)? (c) Contra 2022, em que os "outros" também caíram na reta final e o voto não migrou para Jair (Ciro e Tebet). Confirmaria: "outros" caem 3 pontos ou mais da última pesquisa à urna **e** a A4 manda a maior parte (mais de 50%) das colunas de Caiado, Cury, Renan e Zema que migraram para Flávio. Derrubaria: queda menor que 1,5 ponto ou a maior parte indo para Lula, branco, nulo ou abstenção. Tamanho: pontos de margem entre a parte que migrou para Flávio e a que migrou para Lula.

**H7 · Máquina local (prefeitos de 2024).** Descontinuidade em eleições apertadas: município em que o candidato de direita (por partido, regra de três grupos) ganhou a prefeitura por pouco contra município em que perdeu por pouco, entre os dois primeiros da rodada decisiva de 2024. Variável de corte: margem do candidato de direita entre os dois primeiros, em pontos. Efeito: variação da margem Flávio menos Lula de 2022 para 2026 no município. Estimador: regressão linear local com núcleo triangular, janela de 5 pontos (3 e 10 como sensibilidade), erro padrão agrupado por UF. **Placebo:** o mesmo teste com a variação da margem de 2018 para 2022; precisa dar efeito próximo de zero. **Porta de poder:** menos de 200 municípios na janela de 5 pontos faz o resultado sair como "sem poder para dizer". **Variante:** só o PL. **Manipulação:** contagem de municípios acima e abaixo do corte. Confirmaria: efeito positivo, BH abaixo de 5%, placebo próximo de zero. Derrubaria: efeito dentro do intervalo do placebo. Tamanho: efeito vezes a fração de municípios com direita vencedora apertada, em pontos de margem.

**H8 · Religião e valores.** Regressão municipal da virada contra a proporção de evangélicos do Censo 2022, com efeito fixo de UF e controle de urbanização, escolaridade e cor. Placebo: a virada de 2018 para 2022. Confirmaria: coeficiente positivo, BH abaixo de 5%, placebo diferente (menor) e A6 apontando o mesmo. Derrubaria: sem relação. Tamanho: coeficiente vezes o desvio-padrão da proporção.

**H9 · Governadores aliados.** O teste dos 30 casos da apuração, estendido: voto em Flávio menos voto no governador aliado, por estado, 2026 contra 2022 e 2018, e a virada em estados com governador aliado de cada lado (apoio declarado).

**H10 · Estrutura de campanha.** **Descritivo, sem teste de causa:** tempo de propaganda gratuita e gasto declarado parcial, se disponíveis (§10).

**H11 · O candidato (por que Flávio e não "a direita").** Nos cenários da série de pesquisas em que o mesmo instituto testa Lula contra Flávio e contra outro nome da direita (Tarcísio, Michelle Bolsonaro, Ratinho Júnior, Caiado, Zema) com campo no mesmo mês, a diferença de desempenho (voto válido) entre o outro nome e Flávio. Resumida por nome e por trimestre. Interpretação fixada: o outro nome rende **mais** que Flávio de forma estável em 2 ou mais institutos: "há algo no candidato, que o campo sozinho não explica"; rende o **mesmo**: "o fator é o campo"; rende **menos**: "o fator está fora do candidato". Margem de tolerância para "mesmo": 1,5 ponto.

**H12 · Comparecimento.** A3 e o comparecimento por faixa etária (perfil do eleitorado). Confirmaria: o termo (b) da A3 explica mais de 25% da variação de votos de Flávio ou de Lula. Derrubaria: menos de 10%.

**H13 · Renovação do eleitorado.** Variação do perfil etário do eleitorado apto (TSE, 2022 contra 2026) por município contra a virada, com efeito fixo de UF. Com A6, o efeito de composição por idade (variação da composição vezes o voto por idade). Sem A6, a evidência fica no máximo fraca.

**H14 · Redes sociais.** **Não testável** com dado público confiável. Entra no placar como não testável.

---

## 5. Eventos e episódios (H4)

- **A lista é `dados/eventos.csv`, fechada neste commit.** Origem: os eventos E1 a E12 do projeto do Congresso, os episódios das seções de campanha e controvérsias dos artigos da Wikipédia em português e em inglês, e dois marcos de consolidação da direita. Evento novo só entra pela §12.
- **Alvo:** o alvo é quem o fato trata, não o lado que o fato "ajudaria". Para eventos herdados do Congresso mantém-se a classificação de lá. **Eventos `ambos` são testados sem direção:** conta movimento nos dois sentidos.
- **Confirmação:** cada evento precisa de data confirmada por ato oficial e duas reportagens independentes. Sem isso o evento sai e a contagem do que saiu vai para o relatório.
- **Série testada:** eventos de 2025 (antes de dezembro) **não** são testados contra a série Lula contra Flávio. São testados contra (i) a série de avaliação do governo e (ii) o voto de Lula nos cenários que não incluem Flávio, quando existirem. Eventos de dezembro de 2025 em diante entram na série Lula contra Flávio. Evento do tipo `marco` entra em H6, não em H4.
- **Estatística do evento:** para cada instituto com 8 ou mais rodadas, a mudança da margem entre a última pesquisa antes e a primeira depois do evento, **se a distância entre as duas for de até 45 dias e o cenário tiver o mesmo número de candidatos**. O **movimento normal** do instituto é o percentil 95 do valor absoluto das mudanças entre rodadas seguidas, calculado **fora das janelas de evento** (de 7 dias antes a 21 dias depois de qualquer evento da lista). O evento **coincide com movimento** se a mudança passa do movimento normal em **2 ou mais institutos**, no mesmo sentido. Eventos a menos de 30 dias um do outro são testados juntos e ditos juntos.
- **Leitura:** "coincide com movimento" não é causa. A série só vira indício de causa quando o sentido é o esperado pelo alvo **e** o movimento aparece nos dois ou mais institutos **e** o evento não está dentro de uma janela de 30 dias com outro evento de alvo oposto.

---

## 6. Estatística

Pesos pelo eleitorado (apto ou válido, dito em cada tabela). Erro padrão agrupado por UF nas regressões municipais. **Benjamini-Hochberg a 5%** entre os testes de H3, H7, H8, H12 e H13. Sementes fixas (20261007). Intervalos de reamostragem com 300 repetições (A4) e 1000 (demais). Versões de biblioteca fixadas em `requirements.txt`. Todo teste roda também com a sensibilidade de campo (Caiado na direita) e sem os cinco maiores estados em eleitorado.

---

## 7. O placar e a definição de "principal fator"

1. **Tamanho (T):** o teto em pontos de margem da hipótese, sozinha. **Os tamanhos não se somam**: as hipóteses se sobrepõem. Onde existir um modelo único (regressão municipal com as covariáveis juntas), a divisão entre as covariáveis é dada pela ordem média de entrada, dita como divisão de modelo.
2. **Evidência (E):** *forte* = desenho que separa causa (H7 com placebo e poder) **ou** movimento na série no momento certo em 2 ou mais institutos (H4, H6); *média* = associação entre lugares que (a) passa BH, (b) mantém o sinal com e sem os cinco maiores estados e com a sensibilidade de campo e (c) **não** aparece com o mesmo sinal e tamanho no placebo 2018 para 2022; *fraca* = associação entre lugares que falha em alguma das três ou coincidência no tempo; *não testável*.
3. **Confiança (C):** alta, média ou baixa, dada pelo nível mecânico, próximo ou de fundo (mecânico = conta; próximo = o que mudou no caminho; de fundo = por que o eleitor quis isso) e pelo tamanho do intervalo.
4. **Principal fator:** o de **maior tamanho com evidência pelo menos média**. Se nenhuma hipótese tiver evidência pelo menos média, a resposta é **"nenhum fator sozinho; os dados mostram uma soma de N coisas"**. Se duas hipóteses tiverem tamanhos com intervalos que se sobrepõem, a resposta é "empate entre X e Y".
5. A resposta separa **a base** (H1) **da virada** (as demais) e **o que mudou na urna** **do que as pesquisas não mediram** (B).

---

## 8. O veredito

As regras estão em `analise-da-ia/REGRAS_DO_VEREDITO.md` (em commit neste mesmo momento). O veredito é do Claude, marcado como opinião.

---

## 9. Conferências de dado (dois caminhos)

- Totais de 2026: soma dos boletins contra o arquivo oficial do TSE (nacional e por município; a diferença conhecida de 15 seções sem arquivo é declarada).
- Pesquisas: registro do TSE (existência, data, instituto) e fonte citada pela tabela (valor). As da véspera, em 2 veículos, **total e válidos separados**.
- Pindograma: 20 números contra a imprensa da época.
- Matriz de transição: total reconstruído contra o oficial em cada ajuste (A4).
- Prefeitos de 2024: o vencedor por município contra o resultado de totalização de 2024.
- Perfil do eleitorado: total por município contra o eleitorado apto do arquivo de resultado.
- Eventos: data por ato oficial e duas reportagens.
- Recontagem independente (código novo) dos 10 números mais importantes do relatório.

---

## 10. Condições de não execução

Cada item abaixo executa **só se a condição for verdadeira na Fase 2**. Se não for, o item **não executa**, a razão e a data entram em `docs/FONTES_DE_DADOS.md` e na §12 deste registro, e a hipótese entra no placar como "não testável com os dados coletados".

- **A5:** renda por setor censitário (ou por área de ponderação) publicada pelo IBGE e coordenada no arquivo de local de votação.
- **A6:** tabelas por grupo de pelo menos 2 institutos nos dois anos, publicadas.
- **B5, H5:** pelo menos 5 medições da mesma pergunta em um mesmo instituto em 2026.
- **H2 (i) e o teste de eventos de 2025 contra a avaliação do governo (§5):** pelo menos 8 medições de avaliação do governo, do mesmo instituto, entre jan/2025 e out/2026, legíveis em fonte publicada. Sem isso, H2 (i) e os eventos de 2025 saem como "não testáveis com os dados coletados", e H2 (ii) (a comparação dos cinco presidentes) segue se existirem os cinco valores.
- **H10:** dados de propaganda e de gasto parcial publicados em formato legível por máquina.
- **H7:** resultado de 2024 por candidato e município; o teste sai como "sem poder para dizer" se houver menos de 200 municípios na janela.

---

## 11. Palavras que não entram no relatório

*fraude, manipulada, comprada, encomendada, tendenciosa (como conclusão), golpe (fora do nome da ação penal), massacre, humilhação, lavada, varrida, mentiu, mentira, corrupto ou culpado (sem condenação), deslize, venceu a eleição*.

---

## 12. Emendas a este registro

Nenhuma até a data deste commit.

| # | Data | Mudança | Antes ou depois de ver o resultado |
|---|---|---|---|
| 1 | 07/out/2026 | O registro de pesquisas do TSE de 2026 só tem pesquisa registrada a partir de 1º/jan/2026 (a lei exige registro no ano eleitoral). A regra "entra só quem casa no registro" (bloco B) não se aplica a pesquisa com fim de campo até 31/dez/2025. Essas entram **se a fonte citada for capturada e contiver os valores de Lula e de Flávio** (desvio de até 0,5 ponto no par; até 1,0 com ressalva dita). Pesquisa de 2025 que não confere sai e é contada | **depois** de ver o casamento (131 de 131 de 2026 casam; 39 de 2025 não têm como casar), **antes** de ver qualquer valor da série |
| 2 | 07/out/2026 | A conferência dos valores usa o **par** (Lula e Flávio) a até 400 caracteres de distância no texto da fonte, em valor bruto ou válido, com tolerância de 0,5 ponto (0,5 a 1,0 vale com ressalva). Para a véspera, a segunda fonte é a Revista Fórum. Pesquisa da véspera sem fonte que confere **fica na série**, **marcada**, e **sai do cálculo de erro por instituto (B2)** | **depois** de ver que o texto de algumas fontes usa só os válidos, **antes** de ver qualquer valor da série |
