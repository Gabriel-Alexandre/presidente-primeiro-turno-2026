# Fontes de dados: o que existe, onde, e o que não existe

**Sondagem de 07/out/2026** (Fase 0): só confirma se a fonte existe, onde está e em que formato. Nenhum valor foi tabulado. Cada linha vira, na Fase 2, uma entrada em `dados/MANIFESTO.json` com sha256.

| # | Dado | Fonte | Existe? | Observação |
|---|---|---|---|---|
| base | Votos por seção e município, 2018, 2022 e 2026 | projeto `apuracao-eleicoes-2026`, commit `740fe51`, lido por hash (`dados/FONTE_APURACAO.json`) | ✅ | 28 UFs, 499.192 seções em 2026; derivados fora do git de lá |
| base | Resultado oficial nacional de 2026 | `oficial.sqlite` do projeto da apuração (arquivo do TSE de 05/out 12h51) | ✅ | 99,99% apurado |
| base | Município TSE para IBGE, perfil do Censo 2022, religião, Bolsa Família de ago/2026 | projeto `congresso-e-governos-eleicoes-2026`, commit `f6a1f9e`, lido por hash | ✅ | 5.567 municípios no `municipios.parquet` |
| N1 | Pesquisas de presidente, 1º turno, 2026 | Wikipédia em inglês, "Opinion polling for the 2026 Brazilian presidential election" (texto bruto via API do MediaWiki, atualizado em 05/out) | ✅ | tabelas por período (jan a mar, abr a ago, ago a out; 2025 jun a dez; 2025 jan a mai); colunas por candidato e "Blank/Null/Undec." (percentual da amostra bruta) |
| N1 | Registro de pesquisas no TSE | dados abertos do TSE, `pesquisa_eleitoral_2026.zip` (CSV) | ✅ a abrir na Fase 2 | serve para a existência, a data e o instituto, não para o resultado |
| N1 | Pesquisas de presidente 2014, 2018 e 2022 | Pindograma (já capturado no projeto do Congresso) e Wikipédia em inglês de 2022 | ✅ | 2022 vai de 09/jan a 01/out |
| N2 | Avaliação do governo, 2025 e 2026 | não existe página dedicada na Wikipédia; a procurar em "Second presidency of Lula da Silva", "Governo Lula (2023 a presente)" e nas reportagens de Datafolha e Quaest | 🟡 | condição na §10 do pré-registro |
| N3 | Pesquisa por grupo (religião, idade, renda), véspera de 2022 e 2026 | relatórios e reportagens de Datafolha, Quaest e outros | 🟡 a procurar | condição na §10 (A6) |
| N4 | "Principal problema do país" em série | Datafolha, Quaest | 🟡 a procurar | condição na §10 (H5) |
| N5 | Perfil do eleitorado por município (idade, sexo, escolaridade) 2022 e 2026 | dados abertos do TSE, `eleitorado-2022` e `eleitorado-2026` (`perfil_eleitorado_<ano>.zip`) | ✅ | |
| N5 | Eleitorado por local de votação, com coordenada | `eleitorado_local_votacao_<ano>.zip` | ✅ a abrir | para A5 |
| N6 | Renda por setor censitário ou área de ponderação | IBGE, Censo 2022 | 🟡 a confirmar | condição na §10 (A5) |
| N7 | Religião por município | tabela SIDRA 10198, já no projeto do Congresso | ✅ | |
| N8 | Bolsa Família ago/2026 | já no projeto do Congresso | ✅ | |
| N8 | Auxílio Brasil / Bolsa Família ago/2022 por município | Portal da Transparência, `202208_AuxilioBrasil` | 🟡 a confirmar | para H3 |
| N8 | Desocupação e renda por UF, inflação, juros | SIDRA (PNAD Contínua, IPCA), Banco Central | ✅ | séries nacionais para o descritivo de H3 |
| N9 | Prefeitos de 2024, votação por candidato e município | dados abertos do TSE, `votacao_candidato_munzona_2024.zip` e `consulta_cand_2024.zip` | ✅ | para H7 |
| N10 | Linha do tempo de eventos | `dados/eventos.csv` (fechada) | ✅ | datas a confirmar na Fase 2 |
| N11 | Volume de notícia por dia | GDELT | 🟡 exploratório | fora do núcleo |
| N12 | Propaganda gratuita e gasto parcial | DivulgaCand, prestação parcial | 🟡 | condição na §10 (H10) |
| N13 | Cenários de pesquisa com outros nomes da direita | as mesmas tabelas de N1 | ✅ | os cenários de 2025 trazem Tarcísio, Ciro, Ratinho, Zema e Caiado |

## O que não existe

- O **Estudo Eleitoral Brasileiro (ESEB)** de 2026, com o voto declarado de cada entrevistado: só em 2027.
- A **prestação de contas final** de campanha: só depois do 2º turno.
- Medida confiável de **alcance em redes sociais**: não é público. H14 entra como não testável.
- O CSV de **votação por seção de 2026** dos dados abertos do TSE: ainda não saiu. Não é necessário: o projeto da apuração tem os boletins.

## Limites de nascença das fontes

- A Wikipédia é um índice de pesquisas com fonte em cada linha, **não** a fonte do valor. O pré-registro (§3) exige o registro do TSE e a conferência por amostra.
- As pesquisas publicam percentuais da amostra bruta; os válidos são calculados (pré-registro §1).
- Os derivados do projeto da apuração não estão no git de lá; o `REPLICAR.md` diz como regenerar.
