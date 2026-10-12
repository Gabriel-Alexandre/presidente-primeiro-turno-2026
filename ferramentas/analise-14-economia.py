"""H3 relida (emenda 10): a economia do bolso, cruzando o numero oficial com fontes que nao sao do governo.

Pedido do autor (10/out/2026): os indicadores de emprego e de inflacao em 12 meses melhoraram, mas a sensacao de quem vive no Brasil e
outra; comparar precos de 2022 e de agora, recuperacao judicial, dividas e o que as pessoas dizem nas pesquisas.

O que este script faz:
- precos: o IPCA (IBGE) ACUMULADO de out/2022 a set/2026 (eleicao a eleicao) e de jan/2020 a set/2026, por item (a taxa em 12 meses
  caindo nao quer dizer preco caindo: quer dizer que ele sobe mais devagar);
- a cesta basica do DIEESE em Sao Paulo (fonte sindical, fora do governo) em ago/2022 e ago/2026, contra o salario minimo;
- emprego: pessoas ocupadas, com carteira e informalidade (PNAD, IBGE);
- dividas: nome sujo (Serasa), parte da renda que vai para pagar divida (Banco Central, serie 29034, desde 2005), Selic;
- empresas: recuperacao judicial (Serasa, nova metodologia de 2026);
- sensacao: o que as pessoas responderam a Genial/Quaest sobre a economia e o preco da comida.

Todo numero digitado aqui vem com o trecho literal que precisa existir no arquivo capturado (dados/brutos/economia-critica/); se o
trecho nao estiver la, o script para. Os arquivos e seus sha256 estao em dados/CAPTURAS_ECONOMIA.csv.
Nada aqui testa voto economico no nivel do eleitor: e descricao, cruzada entre fontes.
"""
from __future__ import annotations

import gzip
import hashlib
import html
import io
import json
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import BRUTOS, DADOS, RES  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402

E = BRUTOS / "economia-critica"


def texto(nome: str) -> str:
    b = (E / nome).read_bytes()
    if b[:2] == b"\x1f\x8b":
        b = gzip.decompress(b)
    if b[:4] == b"%PDF":
        import pypdf
        t = " ".join((p.extract_text() or "") for p in pypdf.PdfReader(io.BytesIO(b)).pages)
    else:
        t = b.decode("utf-8", "ignore")
        t = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script.*?</script>|<style.*?</style>", "", t)))
    return re.sub(r"\s+", " ", t)


CONFERE = [
    # (arquivo, trecho literal, o que prova)
    ("cesta2022.pdf", "maior custo (R$ 749,78)", "cesta de Sao Paulo, ago/2022"),
    ("cesta2022.pdf", "R$ 1.212,00", "salario minimo de 2022"),
    ("cesta2026.pdf", "maior custo (R$ 900,59)", "cesta de Sao Paulo, ago/2026"),
    ("cesta2026.pdf", "R$ 1.621,00", "salario minimo de 2026"),
    ("serasa_rj2025.html", "977 processos de recuperação judicial em 2025, maior volume desde 2016", "processos de 2025"),
    ("serasa_rj2025.html", "2.466 empresas (CNPJs) envolvidas no último ano, alta de 13% e recorde da série", "empresas de 2025"),
    ("serasa_rj2025.html", "Após o salto de 36,2% em 2023, o indicador desacelerou, mas permaneceu em um patamar elevado, registrando altas de 26,4% em 2024 e 12,9% em 2025",
     "crescimento anual das empresas em recuperacao"),
    ("serasa_rj2025.html", "8,7 milhões de CNPJs negativados em janeiro de 2026", "empresas com nome sujo"),
    ("inad2022.html", "66,6 milhões de inadimplentes", "pessoas com nome sujo, mai/2022 (recorde da epoca)"),
    ("inad2026.html", "passando de 83,93 milhões para 83,98 milhões", "pessoas com nome sujo, ago/2026"),
    ("quaest_jun26.html", "44% dos entrevista", "economia piorou, jun/2026"),
    ("quaest_jun26.html", "20% dizem que a economia melhorou", "economia melhorou, jun/2026"),
    ("quaest_jun26.html", "Para 69% dos entrevistados, o preço aumentou nos últimos 12 meses", "preco da comida subiu, jun/2026"),
    ("quaest_jun26.html", "BR-07661/2026", "registro da pesquisa"),
    ("quaest56.html", "piorou nos últimos 12 meses recuou de 56% para 48%", "economia piorou, 2025"),
    ("tse_ns_cnn.html", "com a notícia falsa de que a Santa Nossa Senhora Aparecida pode perder o título de padroeira do Brasil", "o caso de Nossa Senhora Aparecida era noticia falsa (TSE, 30/09)"),
]


def conferir() -> list[dict]:
    linhas = []
    for arq, trecho, prova in CONFERE:
        t = texto(arq)
        if trecho not in t:
            raise RuntimeError(f"trecho nao encontrado em {arq}: {trecho!r}")
        linhas.append({"arquivo": arq, "trecho": trecho, "prova": prova})
    return linhas


def ipca() -> dict:
    d = json.loads((E / "ipca2020.json").read_text(encoding="utf-8"))[1:] + json.loads((E / "ipca7060.json").read_text(encoding="utf-8"))[1:]
    s: dict[str, dict[str, float]] = {}
    for r in d:
        if r["V"] in ("...", "-", "X", ""):
            continue
        s.setdefault(r["D4N"], {})[r["D3C"]] = float(r["V"])
    out = []
    for item, mes in s.items():
        def acum(de: str, ate: str) -> float | None:
            ms = [m for m in sorted(mes) if de <= m <= ate]
            if not ms or ms[0] != de:
                return None
            v = 1.0
            for m in ms:
                v *= 1 + mes[m] / 100
            return round(100 * (v - 1), 1)
        pico = None
        if "202001" in mes:
            idx, base, cam = 1.0, None, {}
            for m in sorted(mes):
                idx *= 1 + mes[m] / 100
                cam[m] = idx
            base = cam["202209"]
            pm = max((m for m in cam if m >= "202210"), key=lambda m: cam[m])
            pico = {"mes": pm, "acima_de_set22": round(100 * (cam[pm] / base - 1), 1)}
        out.append({"item": re.sub(r"^[\d.]+", "", item).strip(), "desde_out22": acum("202210", "202609"), "desde_jan20": acum("202001", "202609"), "pico": pico})
    return {r["item"]: r for r in out}


def bcb() -> dict:
    sel = json.loads((E / "sgs432.json").read_text())
    com = json.loads((E / "sgs29034_full.json").read_text())
    selic_max = max(sel, key=lambda x: float(x["valor"]))
    com_max = max(com, key=lambda x: float(x["valor"]))
    pega = lambda serie, data: next(float(x["valor"]) for x in serie if x["data"] == data)  # noqa: E731
    return {"selic_out22": pega(sel, "03/10/2022"), "selic_max": float(selic_max["valor"]), "selic_max_data": selic_max["data"], "selic_ultima": float(sel[-1]["valor"]),
            "comprometimento_set22": pega(com, "01/09/2022"), "comprometimento_ultimo": float(com[-1]["valor"]), "comprometimento_ultimo_mes": com[-1]["data"],
            "comprometimento_maior_da_serie": com_max["data"] == com[-1]["data"], "comprometimento_serie_desde": com[0]["data"]}


def pnad() -> dict:
    o = json.loads((E / "ocupados.json").read_text(encoding="utf-8"))[1:]
    i = json.loads((E / "informalidade.json").read_text(encoding="utf-8"))[1:]
    v = {(r["D3C"], r["D4N"]): int(r["V"]) for r in o}
    tot = lambda p: v[(p, "Total")]  # noqa: E731
    cart = lambda p: next(val for (pp, n), val in v.items() if pp == p and "com carteira" in n)  # noqa: E731
    inf = {r["D3C"]: float(r["V"]) for r in i}
    return {"ocupados_mil_2t22": tot("202202"), "ocupados_mil_2t26": tot("202602"), "carteira_mil_2t22": cart("202202"), "carteira_mil_2t26": cart("202602"),
            "informalidade_2t22": inf["202202"], "informalidade_2t26": inf["202602"]}


def main() -> None:
    linhas = conferir()
    tabela("e14_conferencia_trechos", pd.DataFrame(linhas))
    p = ipca()
    tabela("e14_precos", pd.DataFrame([{"item": k, "desde_out22_pct": v["desde_out22"], "desde_jan20_pct": v["desde_jan20"],
                                         "pico_mes": (v["pico"] or {}).get("mes"), "pico_acima_de_set22_pct": (v["pico"] or {}).get("acima_de_set22")} for k, v in p.items()]))
    rj_2025 = 2466
    rj = {2025: rj_2025, 2024: round(rj_2025 / 1.129), 2023: round(rj_2025 / 1.129 / 1.264), 2022: round(rj_2025 / 1.129 / 1.264 / 1.362)}
    e = {
        "precos": p,
        "cesta_sp": {"ago22": 749.78, "ago26": 900.59, "alta_pct": round(100 * (900.59 / 749.78 - 1), 1),
                     "salario_minimo_2022": 1212.0, "salario_minimo_2026": 1621.0, "alta_salario_minimo_pct": round(100 * (1621 / 1212 - 1), 1),
                     "horas_de_minimo_para_a_cesta_ago22": round(749.78 / (1212 / 220), 1), "horas_de_minimo_para_a_cesta_ago26": round(900.59 / (1621 / 220), 1)},
        "emprego": pnad(),
        "dividas": {"nome_sujo_mi_mai22": 66.6, "nome_sujo_mi_ago26": 83.98, **bcb()},
        "empresas": {"recuperacao_judicial_empresas": rj, "nota": "2022 a 2024 pela conta das altas anuais que a Serasa publica (36,2%, 26,4%, 12,9%); 2025 e o numero publicado",
                     "recuperacao_judicial_processos_2025": 977, "cnpjs_negativados_jan26_mi": 8.7},
        "sensacao": {"quaest_jun26_piorou": 44, "quaest_jun26_melhorou": 20, "quaest_jun26_comida_subiu": 69, "quaest_2025_piorou_pico": 56, "quaest_jun25_piorou": 48},
    }
    registrar("e14", e)
    print(json.dumps({k: v for k, v in e.items() if k != "precos"}, ensure_ascii=False, indent=1))
    for k in ("Índice geral", "Alimentação no domicílio", "Café moído", "Tomate", "Carnes", "Arroz", "Gasolina", "Energia elétrica residencial", "Plano de saúde"):
        print(k, p.get(k))


if __name__ == "__main__":
    main()
