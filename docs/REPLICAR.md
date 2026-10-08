# Como refazer

Tudo roda em Python 3.11 com as versões de `requirements.txt` (`pip install -r requirements.txt`). Os dois projetos de origem precisam estar ao lado deste, nos commits fixados:

```
Downloads/repositorios/
  apuracao-eleicoes-2026                  commit 740fe519 (dados/FONTE_APURACAO.json)
  congresso-e-governos-eleicoes-2026      commit f6a1f9e  (dados/FONTE_CONGRESSO.json)
  presidente-primeiro-turno-2026          este projeto
```

Caminhos diferentes: variáveis de ambiente `PRESIDENTE_APURACAO` e `PRESIDENTE_CONGRESSO`. **Os derivados desses dois projetos não estão no git deles**; para regenerá-los, siga o `docs/REPLICAR.md` de cada um (a apuração coleta e decodifica os boletins de urna; o Congresso coleta o IBGE e o Bolsa Família). A função `verificar_fontes` (`presidente/comum.py`) confere o sha256 do manifesto e de cada arquivo lido, e para se algo mudou.

## A ordem

| Passo | Comando | O que faz |
|---|---|---|
| 1 | `python ferramentas/coletar.py` | baixa Wikipédia, TSE (pesquisas, perfil do eleitorado, local de votação, prefeitos de 2024, resultados de 2018 e 2022) e economia (SIDRA e Banco Central), com sha256 em `dados/MANIFESTO.json` |
| 2 | `python ferramentas/derivar-pesquisas.py` | série de pesquisas e casamento com o registro do TSE |
| 3 | `python ferramentas/verificar-pesquisas.py` | confere os valores na fonte citada (véspera, 2025 e uma amostra de 20) |
| 4 | `python ferramentas/confirmar-eventos.py` | confirma a data de cada episódio em duas reportagens |
| 5 | `python ferramentas/gerar-capturas.py` | `dados/CAPTURAS.csv` com os trechos copiados |
| 6 | `python ferramentas/derivar-votos.py` e `validar-votos.py` | votos por município (2018, 2022, 2026) e conferência contra o oficial |
| 7 | `python ferramentas/derivar-perfil.py` e `derivar-prefeitos.py` | perfil do eleitorado e prefeitos de 2024 |
| 8 | `python ferramentas/analise-1-resultado.py` | A1, A2, A3 |
| 9 | `python ferramentas/analise-2-transicao.py` | A4 (cerca de 30 minutos, 300 reamostragens; `PRESIDENTE_REP=3` para um teste rápido) e depois `analise-2b-estabilidade.py` |
| 10 | `python ferramentas/analise-3-pesquisas.py` | B1 a B4 |
| 11 | `python ferramentas/analise-4-eventos-e-candidato.py` e `analise-5-candidato.py` | H4 e H11 |
| 12 | `python ferramentas/analise-6-municipal.py` | H1, H3, H6 por município, H7, H8, H9, H13 |
| 13 | `python ferramentas/revisao-adversarial.py` | verificações numéricas da revisão |
| 14 | `python ferramentas/analise-7-sintese.py` | síntese, condições de não execução e o placar |
| 15 | `python ferramentas/validacao-independente.py` | recontagem com código e fontes novos |
| 16 | `python ferramentas/analise-8-graficos.py` | gráficos 1920 x 1080 em `resultados/figuras/video/` |
| 17 | `python ferramentas/analise-9-relatorio.py` e `analise-10-revisao.py` | `RELATORIO.md`, `RESUMO_SIMPLES.md`, `docs/LEITURA_DA_IA.md`, `analise-da-ia/DOSSIE.md`, `docs/REVISAO_ADVERSARIAL.md` |
| 18 | `python -m pytest -q` e `python ferramentas/conferir-linguagem.py` | testes e linguagem |

Aleatoriedade com semente 20261007. O que pode dar resultado diferente entre execuções é só o que depende de página da internet (as páginas de imprensa e a Wikipédia mudam): o `dados/MANIFESTO.json` guarda o hash do que foi usado.
