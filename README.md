# Presidente, 1º turno de 2026: o que explica o resultado

Projeto aberto em que o autor coloca o **Claude** (modelo de IA da Anthropic) para analisar, com regras escritas **antes** de ver os resultados, as explicações concorrentes para Flávio Bolsonaro ter terminado o 1º turno de 2026 na frente de Lula.

> **O que o projeto não diz:** em quem cada pessoa votou, nem por que votou (tudo é entre municípios) · intenção de ninguém · quem vai ganhar o 2º turno (25/10/2026) · se as pesquisas foram "tendenciosas" · o efeito das redes sociais, da avaliação do governo, da economia no bolso do eleitor e do gasto de campanha (não testados por falta de dado público) · causa onde o desenho só mostra coincidência. **Flávio terminou o 1º turno em primeiro; não venceu a eleição.**

## Por onde começar

| Quer | Abra |
|---|---|
| a resposta em uma página | [`RESUMO_SIMPLES.md`](RESUMO_SIMPLES.md) |
| tudo o que os dados fecham, com tabelas | [`RELATORIO.md`](RELATORIO.md) |
| a opinião do Claude, hipótese por hipótese, e o placar | [`docs/LEITURA_DA_IA.md`](docs/LEITURA_DA_IA.md) |
| ver como a análise foi feita e o que foi corrigido | [`docs/PLANO.md`](docs/PLANO.md), [`docs/PRE_REGISTRO.md`](docs/PRE_REGISTRO.md), [`docs/REVISAO_ADVERSARIAL.md`](docs/REVISAO_ADVERSARIAL.md) |
| as regras que o veredito seguiu e o que ele leu | [`analise-da-ia/`](analise-da-ia/) |
| de onde vem cada dado | [`docs/FONTES_DE_DADOS.md`](docs/FONTES_DE_DADOS.md), `dados/MANIFESTO.json`, `dados/CAPTURAS.csv` |
| refazer | [`docs/REPLICAR.md`](docs/REPLICAR.md) |
| os gráficos | `resultados/figuras/video/` (1920 x 1080) |

## Quem fez a análise

O **autor** montou e dirigiu o processo e decidiu o repositório. A **análise e o veredito** são do Claude (Claude Sonnet 5.5, no Claude Code, em 07/out/2026; o planejamento e a validação do plano foram do Claude Opus 5.5). Os testes e os limiares foram gravados em commit (`014e6b7`) antes de qualquer análise; as emendas posteriores estão no §12 do pré-registro, cada uma dizendo se foi feita antes ou depois de ver o resultado. A revisão adversarial foi feita pelo mesmo modelo, **não por uma pessoa**.

## Projetos que este lê (sem copiar dados)

- [`apuracao-eleicoes-2026`](https://github.com/Gabriel-Alexandre/apuracao-eleicoes-2026) (boletins de urna de 2026 e votos por seção de 2018 e 2022), commit `740fe519`.
- [`congresso-e-governos-eleicoes-2026`](https://github.com/Gabriel-Alexandre/congresso-e-governos-eleicoes-2026) (município TSE e IBGE, perfil do Censo 2022, pesquisas de 2014 a 2022), commit `f6a1f9e`.

Sem licença: a fala sobre este projeto diz "aberto", não "código aberto".
