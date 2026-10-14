# Dados locais: o que foi apagado e como refazer

**14/out/2026, pedido do autor:** depois do vídeo longo 8 pronto, apagar as bases pesadas baixadas para a pesquisa dos vídeos longos, mantendo tudo documentado. Este projeto é o do **vídeo longo 7** (presidente, 1º turno).

## O que foi apagado

| Pasta | O que tinha | Tamanho | Como refazer (`docs/REPLICAR.md`, passo 1) |
|---|---|---|---|
| `dados/brutos/tse/` | os zips do TSE: pesquisas registradas de 2026, perfil do eleitorado de 2022 e 2026, locais de votação, prefeitos de 2024 e resultados de 2018 e 2022 | ~1,7 GB | `python ferramentas/coletar.py` (os endereços estão no próprio script) |

**Total liberado: ~1,7 GB.** Cada arquivo baixado tem endereço e sha256 em `dados/MANIFESTO.json`, no git.

## O que ficou no disco, de propósito

| Pasta | Por quê |
|---|---|
| `dados/brutos/capturas-*/`, `economia*/` e `wikipedia/` (~42 MB) | páginas de institutos, imprensa, economia e Wikipédia capturadas; página muda ou sai do ar e não volta igual |
| `dados/derivados/` | as tabelas derivadas, leves |

## O que nunca dependeu dos brutos

`resultados/` inteiro, a `analise-da-ia/`, o `RELATORIO.md`, o código e os registros de captura (`dados/CAPTURAS*.csv`): tudo no git. Os dois projetos de origem (`apuracao-eleicoes-2026` e `congresso-e-governos-eleicoes-2026`) também tiveram as bases pesadas apagadas e guardaram os derivados que este projeto lê (`docs/DADOS_LOCAIS.md` de cada um).

⚠️ **Risco registrado uma vez:** o TSE já tirou do ar arquivos de eleição anterior (os logs de 2022). Se isso acontecer com os de 2026, o download não volta igual; o `dados/MANIFESTO.json`, que está no git, continua provando o que foi lido (endereço, hora, tamanho e sha256 de cada arquivo).
