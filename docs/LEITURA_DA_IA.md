# A leitura do Claude, hipótese por hipótese

**Escrito em 07/out/2026 e revisto em 11/out/2026** (emendas 9 e 10, a pedido do autor). Claude Sonnet 5.5 (Anthropic), no Claude Code (aplicativo para computador), em 07/out/2026; o planejamento e a validação do plano foram do Claude Opus 5.5, na mesma sessão de trabalho. É **opinião do Claude**, marcada como opinião, escrita depois das passadas de revisão (`docs/REVISAO_ADVERSARIAL.md`), sob as regras de `analise-da-ia/REGRAS_DO_VEREDITO.md` (em commit antes da análise). Cada número vem de `analise-da-ia/DOSSIE.md`, que vem de `resultados/RESUMO.json`.

> **Opinião não é prova.** O [`RELATORIO.md`](../RELATORIO.md) diz o que os dados fecham. Este arquivo diz qual é a leitura mais provável, com o grau de confiança e o que ficou sem resposta. Nenhuma frase julga intenção de pessoa, partido, instituto de pesquisa, emissora ou tribunal, e nenhuma afirma causa onde o desenho só mostra coincidência. Flávio terminou o 1º turno em primeiro; não venceu a eleição. Nenhuma frase prevê o 2º turno.

## A resposta em quatro frases

1. **O que mudou na urna** (nível mecânico, confiança alta). Entre o 1º turno de 2022 e o de 2026, a margem do candidato do PL sobre Lula andou 7,10 pontos, quase ao meio entre o ganho do candidato do PL (+3,83) e a perda de Lula (-3,27); foi troca de voto dentro dos municípios, em todas as regiões, e não comparecimento.
2. **O que aconteceu na reta final** (nível próximo, confiança média). A média das pesquisas manteve Lula à frente até a última semana e subiu 6,9 pontos a favor de Flávio entre 3/ago e 28/set; os outros candidatos encolheram e o candidato do PL ficou com mais da metade do que eles perderam entre a última pesquisa e a urna em 8 de 10 institutos. Os institutos subestimaram o candidato do PL de um jeito parecido com 2022, e esse é o quarto 1º turno seguido em que a urna dá ao principal candidato contra o PT mais do que as pesquisas mostravam.
3. **O principal fator** (confiança baixa a média). **Nenhum fator sozinho explica as 7,10 pontos.** O que mais se destaca é a consolidação do voto da direita em torno de Flávio na campanha (H6), que ocorre na mesma janela de tempo dos episódios de setembro (H4) e não se separa deles com os dados; atrás disso há uma base herdada que mantém quase todo o voto de Jair de 2022 em Flávio (H1), sem a qual a virada não aconteceria. Pela definição escrita antes (maior tamanho com evidência pelo menos média), a resposta é **empate entre a consolidação na reta final e o bloco de episódios de setembro**, que não podem ser somados nem separados.
4. **O que os dados não alcançam.** Avaliação do governo, voto econômico no nível do eleitor, pauta, redes sociais, tabelas por grupo de eleitor e gasto de campanha não foram testados; por isso esta resposta **não** diz que esses fatores não pesaram. Entre eles, a economia do bolso é, na opinião do Claude, o candidato mais forte: o custo de vida acumulado, a dívida no maior nível desde 2005 e a sensação de piora da maioria apontam no mesmo sentido da virada (seção "A economia").

## O placar

| # | Hipótese | Situação | Tamanho (pontos de margem) | Evidência | Confiança |
|---|---|---|---|---|---|
| H1 | Herança e identidade (a base) | consistente | n/a (explica o piso, não a virada) | forte para a base | alta |
| H2 | Referendo sobre o governo | não testável | n/e | não testável | baixa |
| H3 | Economia (o bolso) | consistente em parte (descritivo, emenda 10) | n/e | fraca (descritivo, cruzado entre fontes) | baixa |
| H4 | Episódios e eventos dos dois lados | consistente em parte | mensagens Flávio-Vorcaro: -5,4 ponto de margem (contra Flávio); Lulinha: +1,2 (mediana de todos os institutos) | forte pela regra literal; depende do limiar (Lulinha) | média |
| H5 | Pauta | não testável | n/e | não testável | baixa |
| H6 | Consolidação e voto útil da direita | consistente | +6,9 ponto de margem na média das pesquisas entre 3/ago e 28/set; 4,1 da última pesquisa à urna (mediana), parecido com 2022 (4,5) | forte (movimento na série e aritmética pesquisa-urna em vários institutos) | média |
| H7 | Máquina local (prefeitos de 2024) | inconsistente | n/e | desenho causal sem efeito detectado | média |
| H8 | Religião e valores | inconsistente | n/e | fraca | média |
| H9 | Governadores aliados | inconsistente | n/e | fraca | baixa |
| H10 | Estrutura de campanha | não testável | n/e | não testável | baixa |
| H11 | O candidato (por que Flávio e não "a direita") | consistente em parte | n/e | fraca | baixa |
| H12 | Comparecimento | inconsistente | n/e | forte (conta exata) | alta |
| H13 | Renovação do eleitorado | inconsistente (envelhecimento) | n/e | fraca (o placebo repete o padrão) | baixa |
| H14 | Redes sociais | não testável | n/e | não testável | baixa |

*Consistente* = as previsões da hipótese aparecem nos testes nomeados; *inconsistente* = aparece o contrário; *não testável* = o dado coletado não alcança. **Os tamanhos não se somam.** Evidência *forte*: desenho que separa causa ou movimento na série no momento certo em 2 ou mais institutos; *média*: associação entre lugares que passa a correção, mantém o sinal e não se repete no placebo; *fraca*: o resto.

**H1 · Herança e identidade (a base).** correlação municipal ponderada entre o voto em Jair (2022) e em Flávio (2026) de 0,98; retenção de 97% dos eleitores de Jair em Flávio (intervalo entre as regiões: 89% a 100%).

**H2 · Referendo sobre o governo.** a única série estruturada de avaliação do governo (Wikipédia) termina em nov/2025 e tem no máximo 6 medições por instituto, abaixo das 8 exigidas; não executa. A comparação dos cinco presidentes também não foi montada.

**H3 · Economia (o bolso).** o emprego melhorou de verdade (96,4 para 103,1 milhões de ocupados; informalidade de 40,0% para 37,4%), mas o custo de vida acumulou e a dívida chegou ao maior nível desde 2005: de out/2022 a set/2026 o IPCA somou 20,8%, a comida em casa 16,4% (e 65,1% desde jan/2020), o café 43,9% (chegou a 80,9% em jun/2025); a parte da renda das famílias que vai para pagar dívida chegou a 28,7%, a maior desde 2005; 84,0 milhões de pessoas com nome sujo (eram 66,6); 2466 empresas em recuperação judicial em 2025, o maior número desde 2012; e 44% diziam que a economia piorou contra 20% que melhorou (Genial/Quaest, jun/2026). O salário mínimo subiu mais que a cesta do DIEESE (+33,7% contra +20,1%). Sem dado por eleitor e sem a série de avaliação do governo (H2), não há teste de voto econômico.

**H4 · Episódios e eventos dos dois lados.** o episódio das mensagens coincide com movimento no sentido esperado (4 de 6 institutos acima do normal); o da investigação de Lulinha coincide (4 de 9, e 1 pelo limiar amostral); o bloco de setembro move a margem, mas mistura alvos dos dois lados e tem só 3 institutos.

**H5 · Pauta.** não foram coletadas 5 medições do "principal problema" do mesmo instituto em 2026; não executa.

**H6 · Consolidação e voto útil da direita.** os outros candidatos caíram 3,7 pontos da última pesquisa à urna e o candidato do PL ficou com 113% da queda (mediana 94%); em 8 de 10 institutos ficou com mais da metade, e o PT em 2. Em 2022 os outros também caíram (3,9 pontos) e o candidato do PL ficou com mais da metade em 9 de 13 institutos: o encolhimento dos outros na reta final não é novidade de 2026; o que muda é a concentração no mesmo lado.

**H7 · Máquina local (prefeitos de 2024).** descontinuidade em 477 municípios: efeito de +1,39 ponto (erro padrão 0,96, p = 0,15), dentro do que o placebo de 2018-2022 mostra (+1,15).

**H8 · Religião e valores.** a virada foi MENOR onde há mais evangélicos (-1,21 ponto por desvio-padrão de 10,3 pontos, p = 0,003); no placebo de 2018-2022 o sinal foi o oposto (+1,71); o sinal permanece ao controlar pelo voto de Jair em 2022 (-1,01, p = 0,024), então não se explica só por efeito teto.

**H9 · Governadores aliados.** virada média de 8,5 ponto nas 10 UFs com governador apoiador de Flávio e de 7,6 nas 5 com governador apoiador de Lula (diferença +0,8; p de permutação = 0,63).

**H10 · Estrutura de campanha.** propaganda gratuita e gasto parcial não foram coletados em formato legível por máquina; não executa.

**H11 · O candidato (por que Flávio e não "a direita").** Caiado, Zema e Ratinho Júnior rendiam bem menos que Flávio nos cenários; Tarcísio rendia perto ou um pouco mais até o fim de 2025 e menos que Flávio no primeiro trimestre de 2026; Michelle Bolsonaro não está nos dados.

**H12 · Comparecimento.** o termo de comparecimento é pequeno e de sinal contrário: -3,8% do ganho de votos do candidato do PL e -1,1% da perda do PT; a troca líquida de voto responde por 93% e 122% (o segundo passa de 100% porque os outros termos têm sinal contrário).

**H13 · Renovação do eleitorado.** municípios cujo eleitorado envelheceu mais tiveram virada menor (-0,68 ponto por desvio-padrão); o placebo de 2018-2022 mostra o mesmo sinal (-1,19), e sem efeito fixo de UF o sinal some.

**H14 · Redes sociais.** redes sociais: sem dado público confiável; não testável.

## A leitura por bloco

### As pesquisas, instituto por instituto (B6)

**Na opinião do Claude (confiança alta para o padrão, nenhuma para o motivo):** existe um padrão, e ele é do 1º turno. Em quatro eleições seguidas, a urna deu ao principal candidato contra o PT de 3,7 a 6,6 pontos a mais do que a mediana das pesquisas, e o voto do candidato do PT ficou perto do que elas mostravam. Datafolha e Ipec (antigo Ibope) mostraram esse candidato mais fraco do que a urna em todas as rodadas desde 2014 (7 de 7 e 6 de 6), inclusive quando a maioria dos institutos errou para o outro lado (2º turno de 2014); a Veritá errou sempre para o lado contrário (4 de 4). **A comparação que sustenta:** no 2º turno, com dois nomes só, o erro cai para perto de zero e muda de lado, o que é consistente com a reta final do 1º turno (voto útil, indecisos e eleitores de outros candidatos indo para o principal candidato contra o PT) não ser bem captada pela última pesquisa. **O limite:** erro com lado fixo é um padrão medido, e o dado não diz se vem de método, de quem aceita responder, de quem decide no fim ou de quem vai votar; chamar isso de intenção seria dizer mais do que o dado mostra.

### A base e a virada (H1, H12)

**Na opinião do Claude (confiança alta):** a eleição de 2026 repetiu a geografia de 2022 e mudou o tamanho dela. A correlação de 0,98 entre Jair e Flávio é tão alta quanto a de Jair 2018 com Jair 2022 (0,96) e a de Lula 2022 com Lula 2026 (0,98), o que sugere uma divisão estável do eleitorado, com o candidato do PL ganhando 3,8 ponto e Lula perdendo 3,3, em relação a 2022, sobre a mesma geografia. A comparação que sustenta: o termo de comparecimento responde por -3,8% do ganho do candidato do PL e a troca líquida de voto por 93,2%. **O limite:** os dados são entre lugares; o estudo que diria em quem cada eleitor votou em 2022 e em 2026 só sai em 2027.

### A reta final (H6, B)

**Na opinião do Claude (confiança média):** o que se vê é uma consolidação, não uma troca. Nas três últimas semanas os outros candidatos perderam espaço em todos os institutos e, da última pesquisa à urna, o candidato do PL ficou com mais da metade dessa perda em 8 de 10 institutos (o PT em 2). A comparação que sustenta: em 2022 o mesmo encolhimento dos outros aconteceu (3,9 pontos), mas dividido (9 de 13 para o candidato do PL, 4 para o PT). **O limite:** o cálculo inclui como os indecisos se distribuíram, e não separa mudança de última hora de erro de medida: nos 6 institutos que dão para decompor, a mudança de última hora explica 0,2 dos 2,2 pontos do erro.

### Episódios dos dois lados (H4)

**Na opinião do Claude (confiança média):** os dados mostram que as notícias mexeram nas pesquisas, nos dois lados, e que o efeito de cada uma foi menor do que a virada. O episódio que mais movimentou a série foi o das mensagens de Flávio com Vorcaro: -5,4 ponto de margem em mediana, em 6 institutos, e a média semanal só voltou ao patamar anterior na semana de 14/09. A autorização para investigar Lulinha coincide com +1,2 ponto, e esse resultado muda com o limiar (acima do normal em 4, 2 ou 1 institutos). **A comparação que sustenta:** os dois episódios movem a margem em sentidos opostos, e o das mensagens (-5,4) é maior em módulo do que o da investigação (+1,2); somados, o efeito líquido dos dois é de -4,2 ponto, desfavorável ao candidato do PL, ou seja, no sentido contrário ao da virada. **O limite:** eventos de 2025 e os de que não deu para confirmar a data não foram testados, e o movimento de setembro mistura alvos dos dois lados. **A opinião do autor** sobre o peso dos escândalos, se ele a disser no vídeo, é dele, e este veredito não a trata como evidência.

### Por lugar (H3, H7, H8, H9, H13)

**Na opinião do Claude (confiança média para o que não se sustenta, baixa para o resto):** as explicações por perfil de município não ajudam. Religião tem sinal contrário ao da hipótese; o envelhecimento do eleitorado, se tem efeito, é pró-Lula; prefeitos de 2024 e governadores aliados não separam. **A comparação que sustenta:** em religião o sinal se mantém ao tirar os cinco maiores estados, o efeito fixo de UF ou os pesos, mas é o oposto no placebo de 2018 a 2022; no envelhecimento o placebo repete o padrão (e com tamanho maior) e o sinal some sem o efeito fixo de UF; nas prefeituras de 2024 o efeito está dentro do que o placebo mostra; nos governadores a diferença é de +0,8 ponto com p de permutação de 0,63. **O limite:** isso não descarta que religião, idade ou economia importem no nível do eleitor; só diz que a variação **entre municípios** da virada não se alinha com elas.

### A economia (H3)

**Na opinião do Claude (confiança baixa para o efeito no voto, alta para a descrição):** o retrato de 07/out estava incompleto. O emprego melhorou de verdade, e outras fontes confirmam (96,4 para 103,1 milhões de ocupados; o salário mínimo subiu mais do que a cesta do DIEESE). Mas o preço não volta: a comida em casa está +65,1% acima de 2020, o café quase triplicou, e desde 2022 café, tomate, luz e gasolina subiram bem acima da média. A dívida apertou: a parte da renda que vai para pagar dívida é a maior desde 2005, há 84,0 milhões de pessoas com nome sujo, e as empresas em recuperação judicial chegaram ao maior número desde 2012. E a maioria sentia isso: 44% diziam que a economia piorou, contra 20%. **A comparação que sustenta:** quatro fontes que não são a mesma (IBGE, DIEESE, Serasa, Banco Central) e uma pesquisa de opinião apontam no mesmo sentido, e esse sentido é o da virada. **O limite:** é descrição, não teste; sem a série de avaliação do governo e sem dado por eleitor, o projeto não mede quanto disso virou voto. Entre as explicações que o projeto não consegue testar, é a que o Claude considera mais forte.

## O que o Claude não consegue dizer

1. Em quem cada pessoa votou, ou por que votou.
2. Se os episódios mudaram votos: só se a série de pesquisas se moveu, e a pesquisa também mede erro.
3. Qual fração da virada as pesquisas mostravam: de 77,6% a 106,5% conforme o resumo (média ou mediana).
4. Para onde foi o voto dos que não votaram em 2022, e o de Ciro e Tebet: a estimativa não é estável entre regiões.
5. O peso da avaliação do governo, da economia no voto de cada eleitor, da pauta, das redes sociais e do gasto de campanha.
6. Por que alguns institutos erram sempre para o mesmo lado.
7. O 2º turno.

## Teste do espelho e do recorte

| Afirmação | Com os lados trocados, seria escrita igual? | Recortada, vira anúncio de quem? |
|---|---|---|
| a virada foi troca de voto, não comparecimento | sim: vale para qualquer virada medida do mesmo jeito | de ninguém: descreve o mecanismo |
| no 1º turno, as pesquisas subestimaram o principal candidato contra o PT em quatro eleições seguidas | sim: o erro é medido no sinal que ele tem, e o 2º turno (sem lado fixo) vem junto | pode ser usada pelos dois lados; por isso vem com o 2º turno e com os institutos que erraram para o outro lado |
| Datafolha e Ipec mostraram o candidato contra o PT mais fraco em todas as rodadas desde 2014; a Veritá, mais forte | sim: os dois lados do erro são nomeados com a mesma régua | a frase diz direção do erro e nunca intenção |
| o emprego melhorou, mas o custo de vida e a dívida pesaram | sim: vale para qualquer governo medido do mesmo jeito | as duas metades andam juntas |
| as mensagens de Flávio com Vorcaro coincidem com queda e a investigação de Lulinha com alta | sim: os dois episódios têm o mesmo teste e a mesma linguagem | o recorte "só o primeiro" ou "só o segundo" seria enganoso; as duas frases andam juntas |
| nenhum fator sozinho explica | sim | de ninguém |
| religião e idade não explicam a virada entre municípios | sim: o mesmo teste valeria para qualquer lado | de ninguém |
