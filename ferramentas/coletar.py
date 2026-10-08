"""Coleta dos dados novos, um download por vez, com sha256 no dados/MANIFESTO.json.

Uso: python ferramentas/coletar.py [grupo ...]     grupos: wikipedia tse
Sem argumento, coleta todos. Nao repete arquivo ja baixado.
"""
from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import BRUTOS  # noqa: E402
from presidente.manifesto import baixar  # noqa: E402

CDN = "https://cdn.tse.jus.br/estatistica/sead/odsele"
WIKI = "https://{l}.wikipedia.org/w/api.php?action=parse&page={p}&prop=wikitext&format=json&formatversion=2"
WIKIHTML = "https://{l}.wikipedia.org/w/api.php?action=parse&page={p}&prop=text&format=json&formatversion=2"

GRUPOS = {
    "wikipedia": [
        (WIKI.format(l="en", p=quote("Opinion_polling_for_the_2026_Brazilian_presidential_election")), "wikipedia/pesquisas-2026-en.json"),
        (WIKI.format(l="en", p=quote("Opinion_polling_for_the_2022_Brazilian_presidential_election")), "wikipedia/pesquisas-2022-en.json"),
        (WIKIHTML.format(l="en", p=quote("Opinion_polling_for_the_2026_Brazilian_presidential_election")), "wikipedia/pesquisas-2026-en-html.json"),
        (WIKIHTML.format(l="en", p=quote("Opinion_polling_for_the_2022_Brazilian_presidential_election")), "wikipedia/pesquisas-2022-en-html.json"),
        (WIKI.format(l="en", p=quote("2026_Brazilian_general_election")), "wikipedia/eleicao-2026-en.json"),
        (WIKI.format(l="pt", p=quote("Eleição_presidencial_no_Brasil_em_2026")), "wikipedia/eleicao-presidencial-2026-pt.json"),
    ],
    "tse": [
        (f"{CDN}/pesquisa_eleitoral/pesquisa_eleitoral_2026.zip", "tse/pesquisa_eleitoral_2026.zip"),
        (f"{CDN}/perfil_eleitorado/perfil_eleitorado_2022.zip", "tse/perfil_eleitorado_2022.zip"),
        (f"{CDN}/perfil_eleitorado/perfil_eleitorado_2026.zip", "tse/perfil_eleitorado_2026.zip"),
        (f"{CDN}/eleitorado_locais_votacao/eleitorado_local_votacao_2022.zip", "tse/eleitorado_local_votacao_2022.zip"),
        (f"{CDN}/eleitorado_locais_votacao/eleitorado_local_votacao_2026.zip", "tse/eleitorado_local_votacao_2026.zip"),
        (f"{CDN}/votacao_candidato_munzona/votacao_candidato_munzona_2024.zip", "tse/votacao_candidato_munzona_2024.zip"),
        (f"{CDN}/consulta_cand/consulta_cand_2024.zip", "tse/consulta_cand_2024.zip"),
    ],
}


def main() -> None:
    quais = sys.argv[1:] or list(GRUPOS)
    for g in quais:
        for url, rel in GRUPOS[g]:
            e = baixar(url, BRUTOS / rel, pausa=2.0)
            print(g, rel, e["bytes"], e["sha256"][:12], flush=True)


if __name__ == "__main__":
    main()
