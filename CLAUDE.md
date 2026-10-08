# CLAUDE.md: como operar neste repositório

As regras moram em `.cursor/rules/*.mdc`, que o Cursor carrega sozinho e o Claude Code não. Este arquivo é roteador: se um fato aqui contradisser o arquivo dono, o dono ganha.

## Leia antes de qualquer coisa

| Ordem | Arquivo | Para quê |
|---|---|---|
| 1 | `ESTADO.md` | onde o trabalho parou |
| 2 | `.cursor/rules/presidente-fundamentos.mdc` | a doutrina, sempre |
| 3 | `docs/PLANO.md` | o método e as fases |
| 4 | `docs/PRE_REGISTRO.md` | os testes e os critérios; nenhuma análise roda antes de ele estar em commit |
| 5 | `docs/FONTES_DE_DADOS.md` | de onde vem cada dado |
| 6 | `analise-da-ia/REGRAS_DO_VEREDITO.md` | o que o veredito pode afirmar |
| 7 | `docs/LEITURA_DA_IA.md` e `RELATORIO.md` | o resultado, quando a pergunta for sobre ele |

## O que nunca fazer

- Dar número que não saiu de script sobre dado com hash.
- Escrever nos repositórios `apuracao-eleicoes-2026` e `congresso-e-governos-eleicoes-2026`, ou ler deles sem conferir o hash de `dados/FONTE_*.json`.
- Mudar critério sem a entrada na §12 do pré-registro.
- Escrever número à mão no relatório.
- Usar as palavras da lista da doutrina, ou "venceu a eleição".
- Prever o 2º turno, ou escrever frase que, recortada, vire material de campanha.
- Baixar em massa sem teto de requisições (o TSE devolve 429) e sem manifesto.
- Fazer commit ou push sem o autor confirmar (o autor mandou o commit e o push desta execução em 07/out/2026; isso não vale para as próximas).
