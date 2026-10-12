# Correções

Erro achado **depois da publicação** entra aqui com o antes e o depois. Até a primeira publicação (07/out/2026) não houve nenhum.

Os erros de método achados e corrigidos **durante a execução** estão em [`REVISAO_ADVERSARIAL.md`](REVISAO_ADVERSARIAL.md) (tabela do fim) e as emendas ao pré-registro, em [`PRE_REGISTRO.md`](PRE_REGISTRO.md) §12, cada uma dizendo se foi feita antes ou depois de ver o resultado.

## 08/out/2026 · rótulos achados ao escrever o roteiro do vídeo

| Onde | Antes | Depois | Muda algum número? |
|---|---|---|---|
| `RELATORIO.md` §1, tabela do resultado | a linha "Candidato do PL" trazia o valor de 2018 sem ressalva | "Candidato do PL (em 2018, Jair Bolsonaro pelo PSL)": em 2018 o candidato concorreu pelo PSL | não |
| gráfico `08_erro_dos_institutos` | o rodapé não dizia o partido de 2018 | rodapé com "em 2018, Jair Bolsonaro concorreu pelo PSL" | não |
| gráfico `05_transicao_2022_2026` | o rodapé citava dois critérios de estabilidade | os três critérios, como manda a emenda 8 (o valor nacional dentro do intervalo das regiões) | não: a tabela e as conclusões já usavam os três |

## 11/out/2026 · o que o retorno do autor derrubou

| Onde | Antes | Depois | Muda algum número publicado? |
|---|---|---|---|
| pesquisas de 2018 (`analise-3`, B2; gráfico `08`) | lia a coluna `pct` do Pindograma, que é o **resultado da urna**; por isso 2018 aparecia com erro "perto de zero" e "sem direção" | lê `valid_result`, que é a pesquisa; e a última pesquisa não pode ser do dia da votação (boca de urna). 2018: erro mediano da diferença de -1,2 e o voto de Jair subestimado em 8 de 10 institutos | **sim**: "em 2018 o erro foi de +0,3, sem direção" estava errado |
| véspera de 2026 (B2, H6, B4) | AtlasIntel e Futura (PDF) e Palver (página salva comprimida) saíram como "não verificável" e ficaram fora do erro por instituto | conferidas na fonte original e incluídas; a Futura com o número do PDF (44,8 e 42,6), diferente da tabela da Wikipédia | **sim**: de 7 para 10 institutos verificados; "os 7 subestimaram o candidato do PL" vira "os 10 deram a ele menos voto do que a urna; na diferença, 8 de 10 mostraram o PL pior"; H6 passa a 8 de 10 institutos com mais da metade da queda dos outros para o PL; o quanto da virada as pesquisas mostravam vai a 78%, 95% e 106% (média, média aparada e mediana); B4 passa a 6 institutos |
| H3, economia | descrita só pelo emprego e pela inflação em 12 meses ("os indicadores melhoraram") | emenda 10: preço acumulado, cesta do DIEESE, dívida das famílias, nome sujo, recuperação judicial e sensação (seção 7A do relatório) | **sim**: a situação da H3 muda para "consistente em parte (descritivo)" |
| episódio V23 | "reportagem da GloboNews e reação de Flávio e da CNBB" | a afirmação era falsa, e o TSE manteve fora do ar os posts que ligavam Flávio a ela (30/09) | não |

## 12/out/2026 · achados na revisão da edição do vídeo

| Onde | Antes | Depois | Muda algum número publicado? |
|---|---|---|---|
| gráficos `02`, `15`, `17` e `19` (e o `10`) | o rótulo do eixo y saía pela esquerda da figura ("…mida subiu", "…onta de luz") e, no `15`, o "1º turno" do eixo x encostava no rodapé da fonte | `presidente/comum.py` ganhou `caber_na_figura` e `descolar_da_fonte`, chamados antes de salvar todo gráfico: o eixo só se move quando o texto não cabe | não |

### ⬜ Registrado para o autor decidir: voto válido publicado × voto válido recalculado (12/out)

O erro da véspera de 2026 (B2, gráficos `08` e `15`, a mediana de +3,7) usa o voto válido **recalculado pelos votos totais arredondados** em 7 institutos e o **número publicado** em 3 (AtlasIntel e Futura, do PDF; Palver, o estimulado da matéria). Conferido nas fontes de `dados/CAPTURAS_INSTITUTOS.csv` em 12/out:

| Instituto | Flávio, válido publicado | Flávio, recalculado | Diferença | Por quê |
|---|---|---|---|---|
| Datafolha (3/out) | 42 (g1: *"Lula, 45%; Flávio Bolsonaro, 42%"*) | 43,0 (40 de 93) | 1,0 | arredondamento dos totais |
| Quaest (3/out) | 45 (g1: *"Lula, 46%; Flávio Bolsonaro, 45%"*) | 43,7 | 1,3 | a Quaest publica os válidos pelo modelo de quem vai votar |
| PoderData (2/out) | 43 (Poder360: *"o presidente registra 45% [...] o senador tem 43%"*) | 43,6 | 0,6 | arredondamento |
| MDA (2/out) | 42,1 (CNN) | 42,1 | 0 | |
| Real Time, Vox Brasil, Indexa | não publicam válido na fonte | | | só a conta uniforme compara os 10 |

Nada foi mudado: a conta uniforme é a única que alcança os 10, e trocar o método muda a mediana de 2026 e o erro de cada instituto. A direção não muda (o Datafolha segue mostrando o Flávio mais fraco que a urna). ⬜ Decisão do autor.
