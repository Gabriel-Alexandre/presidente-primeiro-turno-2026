# Plano e método: o que explica o resultado de presidente no 1º turno de 2026

**Escrito em:** 07/out/2026. O plano de origem está em `contexto/projetos-externos/PRESIDENTE_PRIMEIRO_TURNO_2026.md` do repositório do autor (v2, validado). Este arquivo é o método deste projeto; o pré-registro (`PRE_REGISTRO.md`) tem os testes.

## 0. Em uma frase

Um projeto aberto em que o autor **coloca o Claude para analisar**, com regras escritas antes de ver os resultados, as explicações concorrentes para Flávio Bolsonaro ter terminado o 1º turno de 2026 na frente de Lula. O Claude mede quanto de cada explicação os dados sustentam e diz qual pesou mais, marcando o que é opinião dele e o que os dados não alcançam.

## 1. O pedido, nas palavras do autor (07/out)

*"colocar a inteligência artificial para fazer uma análise muito bem aprofundada sobre as principais motivações que levaram o Flávio Bolsonaro a ter essa vitória no primeiro turno"*, *"qual foi o principal fator determinante? [...] O que é que a inteligência artificial acha sobre isso?"*, *"quais fatores a mais podem ter influenciado, por exemplo, escândalos no STF, deslizes do candidato Lula, ou algumas outras coisas"*, *"o projeto ele tem que ser público"*, *"eu vou precisar fazer um relatório no final para colocar na descrição"*. E a correção dele no mesmo dia: o enquadramento é *"eu coloquei uma IA para analisar"*, o Claude, não *"eu criei uma IA"*.

## 2. O que o projeto não promete

Em quem cada pessoa votou · intenção de ninguém · quem vai ganhar o 2º turno · se as pesquisas foram "tendenciosas" · causa onde o desenho só mostra coincidência · o efeito das redes sociais. **Flávio terminou o 1º turno em primeiro; não venceu a eleição.**

## 3. Fatos de partida (do arquivo oficial do TSE, 05/out)

Flávio Bolsonaro (PL) 47,03% dos válidos (56.104.503 votos), Lula (PT) 45,16% (53.879.538), Augusto Cury (Avante) 2,89%, Renan Santos (Missão) 2,24%, Ronaldo Caiado (PSD) 2,18%, Romeu Zema (Novo) 0,27%. Abstenção de 21,08% (33.469.244 de 158.745.502, com o exterior). 2º turno em 25/10/2026. Os números por município e a comparação com 2022 saem de script na Fase 4.

## 4. As perguntas

- **Bloco A · o que aconteceu** (A1 a A6): onde, entre quem, troca de voto ou comparecimento, para onde foi o voto de 2022, dentro das cidades.
- **Bloco B · a reta final** (B1 a B5): trajetória, erro dos institutos, migração dos "outros", decomposição do erro, rejeição.
- **Bloco C · por quê** (H1 a H14): herança, governo, economia, episódios dos dois lados, pauta, consolidação da direita, máquina local, religião, aliados, estrutura de campanha, o candidato, comparecimento, renovação do eleitorado, redes sociais.
- **Bloco D · o veredito** do Claude, em `analise-da-ia/`.

## 5. As fases

| Fase | Saída | Porta de saída |
|---|---|---|
| 0 · Sondagem | `docs/FONTES_DE_DADOS.md` | feito em 07/out |
| 1 · Estrutura e pré-registro em commit | este repositório, `PRE_REGISTRO.md`, `REGRAS_DO_VEREDITO.md`, `dados/eventos.csv`, `FONTE_*.json` | hash do commit no relatório |
| 2 · Coleta | tudo com sha256 em `dados/MANIFESTO.json`; capturas em `dados/CAPTURAS.csv` | manifesto completo |
| 3 · Validação | os caminhos da §9 do pré-registro | se a soma não fecha, para e registra |
| 4 · Análise | A, depois B, depois C | |
| 5 · Revisão, veredito e segunda revisão | `docs/REVISAO_ADVERSARIAL.md`, `analise-da-ia/` | 100% dos achados tratados |
| 6 · Relatório e gráficos | `RELATORIO.md`, `RESUMO_SIMPLES.md`, `docs/LEITURA_DA_IA.md`, `resultados/figuras/video/` | |

## 6. Reprodutibilidade

- Os dados por seção e por município vêm dos dois repositórios anteriores, **lidos sem cópia** e conferidos por hash (`dados/FONTE_APURACAO.json`, `dados/FONTE_CONGRESSO.json`). Os dados novos entram em `dados/MANIFESTO.json`.
- Aleatoriedade com semente fixa (20261007). Versões de biblioteca em `requirements.txt`.
- Erro achado depois da publicação vai para `docs/CORRECOES.md` com o antes e o depois.

## 7. Travas do assunto

As quatro do projeto de checagem (nada de contar mentira de ninguém, nada de recomendação de voto, nada de julgar intenção, nada de testar um lado só), as três do projeto do Congresso (causa só com desenho, investigação não é condenação, adjetivo só medido) e as deste projeto, em `.cursor/rules/presidente-fundamentos.mdc`: "terminou na frente" e não "venceu a eleição", simetria em toda hipótese, "principal fator" pela definição escrita antes, lugar não é pessoa, campo pela regra de três grupos, nenhuma previsão do 2º turno.

## 8. Riscos conhecidos

| Risco | O que o método faz |
|---|---|
| o Claude escolhe o fator mais comentado | definição de "principal fator" em commit antes (pré-registro §7) |
| série de pesquisa incompleta | só entra pesquisa que casa com o registro do TSE; o que saiu vai contado |
| total e válidos misturados | os dois separados em toda pesquisa |
| eventos escolhidos a dedo | lista fechada em commit antes das séries; alvo é quem o fato trata |
| falácia ecológica | todo resultado por lugar vem com a ressalva; A6 só quando existir |
| seção que não casa entre eleições | município como unidade; local de votação só com a taxa de casamento declarada |
| inferência ecológica errando o total | restrições e conferência contra o oficial em cada ajuste |
| o TSE devolve 429 | um coletor só, com limitador adaptativo |
| o vídeo vira peça de campanha | teste do recorte em cada frase |

## 9. O que foi executado (07/out/2026)

| Parte | Estado | Observação |
|---|---|---|
| A1, A2, A3 | ✅ | resultado, onde está a virada, troca de voto contra comparecimento |
| A4 | ✅ | regressão ecológica com restrições; só os fluxos estáveis entram nas conclusões |
| A5, A6 | ⛔ | condição do §10 do pré-registro falsa (renda por setor não publicada; tabelas por grupo não coletadas) |
| B1 a B4 | ✅ | B4 só em 3 institutos |
| B5 | ⛔ | rejeição não coletada |
| H1, H11, H12 | ✅ | |
| H2 | ⛔ | avaliação do governo sem 8 medições por instituto |
| H3 | 🟡 | descritivo nacional e por UF; por município, não (Bolsa Família de 2022) |
| H4 | 🟡 | 13 episódios com data confirmada; 3 grupos testados; eventos de 2025 não testados |
| H5, H10 | ⛔ | condições falsas |
| H6 | ✅ | pela aritmética pesquisa-urna (emenda 4) |
| H7, H8, H9, H13 | ✅ | com placebo, correção de Benjamini-Hochberg onde cabe |
| H14 | ⛔ | não testável |
| Veredito | ✅ | `docs/LEITURA_DA_IA.md`, com revisão adversarial; **sem** as cinco leituras |
