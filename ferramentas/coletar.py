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

SIDRA = "https://apisidra.ibge.gov.br/values"
BCB = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{n}/dados?formato=json&dataInicial=01/01/2022&dataFinal=30/09/2026"

GRUPOS = {
    "wikipedia": [
        (WIKI.format(l="en", p=quote("Opinion_polling_for_the_2026_Brazilian_presidential_election")), "wikipedia/pesquisas-2026-en.json"),
        (WIKI.format(l="en", p=quote("Opinion_polling_for_the_2022_Brazilian_presidential_election")), "wikipedia/pesquisas-2022-en.json"),
        (WIKIHTML.format(l="en", p=quote("Opinion_polling_for_the_2026_Brazilian_presidential_election")), "wikipedia/pesquisas-2026-en-html.json"),
        (WIKIHTML.format(l="en", p=quote("Opinion_polling_for_the_2022_Brazilian_presidential_election")), "wikipedia/pesquisas-2022-en-html.json"),
        (WIKI.format(l="en", p=quote("2026_Brazilian_general_election")), "wikipedia/eleicao-2026-en.json"),
        (WIKI.format(l="pt", p=quote("Eleição_presidencial_no_Brasil_em_2026")), "wikipedia/eleicao-presidencial-2026-pt.json"),
    ],
    "economia": [
        (f"{SIDRA}/t/4099/n3/all/v/4099/p/202202,202302,202602", "economia/desocupacao_uf.json"),
        (f"{SIDRA}/t/5436/n3/all/v/5933/p/202202,202302,202602/c2/6794", "economia/rendimento_uf.json"),
        (f"{SIDRA}/t/4099/n1/all/v/4099/p/all", "economia/desocupacao_brasil.json"),
        (f"{SIDRA}/t/5436/n1/all/v/5933/p/all/c2/6794", "economia/rendimento_brasil.json"),
        (f"{SIDRA}/t/7060/n1/all/v/69/p/202201-202609/c315/7169,7170", "economia/ipca_12m_geral_e_alimentos.json"),
        (BCB.format(n=432), "economia/selic_meta.json"),
    ],
    "tse": [
        (f"{CDN}/pesquisa_eleitoral/pesquisa_eleitoral_2026.zip", "tse/pesquisa_eleitoral_2026.zip"),
        (f"{CDN}/perfil_eleitorado/perfil_eleitorado_2022.zip", "tse/perfil_eleitorado_2022.zip"),
        (f"{CDN}/perfil_eleitorado/perfil_eleitorado_2026.zip", "tse/perfil_eleitorado_2026.zip"),
        (f"{CDN}/eleitorado_locais_votacao/eleitorado_local_votacao_2022.zip", "tse/eleitorado_local_votacao_2022.zip"),
        (f"{CDN}/eleitorado_locais_votacao/eleitorado_local_votacao_2026.zip", "tse/eleitorado_local_votacao_2026.zip"),
        (f"{CDN}/votacao_candidato_munzona/votacao_candidato_munzona_2024.zip", "tse/votacao_candidato_munzona_2024.zip"),
        (f"{CDN}/consulta_cand/consulta_cand_2024.zip", "tse/consulta_cand_2024.zip"),
        (f"{CDN}/votacao_candidato_munzona/votacao_candidato_munzona_2022.zip", "tse/votacao_candidato_munzona_2022.zip"),
        (f"{CDN}/votacao_candidato_munzona/votacao_candidato_munzona_2018.zip", "tse/votacao_candidato_munzona_2018.zip"),
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
