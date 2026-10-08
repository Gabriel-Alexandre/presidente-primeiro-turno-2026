# ESTADO: onde o trabalho parou

**Atualizado em:** 07/out/2026.

## Em uma frase

Executado de ponta a ponta: pré-registro em commit antes de qualquer análise, coleta com hash, validação por dois caminhos (13 de 13 números na recontagem independente), análises dos blocos A, B e C, revisão adversarial, placar, veredito do Claude, relatório e 14 gráficos. **Não** foram testados: avaliação do governo, voto econômico por eleitor, pauta, redes sociais, tabelas por grupo de eleitor e gasto de campanha (condições do §10 do pré-registro).

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
