# ESTADO: onde o trabalho parou

🧹 **14/out/2026: as bases pesadas baixadas do TSE e afins foram apagadas do disco** (pedido do autor, depois do vídeo longo 8 pronto). Resultados, relatório, código e manifestos seguem no git; as capturas de páginas e os derivados leves ficaram no disco. O que saiu, o tamanho e o comando de cada download: `docs/DADOS_LOCAIS.md`.

**Atualizado em:** 11/out/2026.

## Em uma frase

Executado de ponta a ponta: pré-registro em commit antes de qualquer análise, coleta com hash, validação por dois caminhos (13 de 13 números na recontagem independente), análises dos blocos A, B e C, revisão adversarial, placar, veredito do Claude, relatório e 19 gráficos (15 a 19 em 11/out). **Não** foram testados: avaliação do governo, voto econômico por eleitor, pauta, redes sociais, tabelas por grupo de eleitor e gasto de campanha (condições do §10 do pré-registro).

## 11/out/2026: o retorno do autor

Três perguntas dele acharam defeito, e tudo foi corrigido e registrado (`docs/CORRECOES.md`, emendas 9 e 10 do pré-registro, passada 4 de `docs/REVISAO_ADVERSARIAL.md`): o 2018 das pesquisas lia a coluna da urna; três pesquisas da véspera de 2026 tinham ficado de fora por defeito de coleta; e a economia estava descrita só pelo emprego. Novos: **instituto por instituto desde 2014** (`analise-13`, seção 5.1 do relatório: no 1º turno, quatro eleições seguidas em que a urna deu ao principal candidato contra o PT de 3,7 a 6,6 pontos a mais; Datafolha 7 de 7 e Ipec 6 de 6 mostrando esse candidato mais fraco; Veritá 4 de 4 mais forte) e **a economia cruzando fontes** (`analise-14`, seção 7A). Gráficos 15 a 19.

## O que está pronto

| Peça | Estado |
|---|---|
| Plano, pré-registro (commit `014e6b7`), regras do veredito, lista de eventos | ✅ |
| Coleta com sha256 e capturas | ✅ `dados/MANIFESTO.json`, `dados/CAPTURAS.csv` |
| Validação (porta) | ✅ votos por município contra o oficial; recontagem independente |
| Análises A, B e C | ✅ `resultados/RESUMO.json` |
| Revisão adversarial | ✅ `docs/REVISAO_ADVERSARIAL.md` |
| Relatório, resumo simples, leitura e dossiê | ✅ `RELATORIO.md`, `RESUMO_SIMPLES.md`, `docs/LEITURA_DA_IA.md`, `analise-da-ia/DOSSIE.md` |
| Gráficos 1920 x 1080 | ✅ `resultados/figuras/video/` |
| Testes | ✅ `python -m pytest -q` (9) |
| Cinco leituras do Claude (opcional) | ⬜ não feito |

## O que observar ao retomar

- O 2º turno é em 25/10/2026. **Nenhuma previsão aqui.**
- Se o autor quiser tratar a avaliação do governo (H2), o que falta é uma série de pelo menos 8 medições por instituto em 2025 e 2026, em fonte publicada.
- O TSE pode republicar arquivos: compare os hashes do manifesto.
