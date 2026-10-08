"""Testes do nucleo: identidades exatas, a regressao ecologica em dados sinteticos, o analisador de datas e o casamento de pares."""
from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from presidente import partidos  # noqa: E402
from presidente.ecologica import ajustar  # noqa: E402
from presidente.pesquisas import _datas  # noqa: E402


def modulo(nome: str):
    spec = importlib.util.spec_from_file_location(nome.replace("-", "_"), RAIZ / "ferramentas" / f"{nome}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _municipios(n: int = 60, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    d = []
    for ano in (2022, 2026):
        v = rng.integers(1000, 9000, n)
        pl = (v * rng.uniform(0.3, 0.5, n)).astype(int) + (ano == 2026) * 200
        pt = (v * rng.uniform(0.3, 0.5, n)).astype(int)
        d.append(pd.DataFrame({"ano": ano, "uf": ["A"] * 30 + ["B"] * 30, "pl": pl, "pt": pt, "nominais": v, "regiao": ["R1"] * 30 + ["R2"] * 30, "capital": False, "porte": "x"}))
    x = pd.concat(d, ignore_index=True)
    x["mun"] = list(range(n)) * 2
    return x


def test_deslocamento_soma_exatamente_a_virada():
    a1 = modulo("analise-1-resultado")
    d = _municipios()
    v = a1.margem(d[d.ano == 2026]) - a1.margem(d[d.ano == 2022])
    for col in ("regiao", "uf"):
        t = a1.deslocamento(d, col)
        assert abs(t.contribuicao.sum() - v) < 1e-9
        assert np.allclose(t.dentro + t.composicao, t.contribuicao)


def test_regressao_ecologica_recupera_matriz_conhecida():
    rng = np.random.default_rng(3)
    n = 400
    X = rng.dirichlet([3, 3, 2], n)
    B = np.array([[0.9, 0.1], [0.2, 0.8], [0.5, 0.5]])
    Y = X @ B
    est = ajustar(X, Y, np.ones(n))
    assert np.allclose(est, B, atol=0.02)
    assert np.allclose(est.sum(axis=1), 1, atol=1e-6)


def test_regressao_ecologica_respeita_as_restricoes():
    rng = np.random.default_rng(4)
    X = rng.dirichlet([1, 1, 1], 100)
    Y = rng.dirichlet([1, 1], 100)
    est = ajustar(X, Y, rng.uniform(1, 2, 100))
    assert (est >= -1e-9).all() and np.allclose(est.sum(axis=1), 1, atol=1e-6)


def test_datas_de_pesquisa():
    assert _datas("2–3 Oct", 2026) == (date(2026, 10, 2), date(2026, 10, 3))
    assert _datas("30 Sep–3 Oct", 2026) == (date(2026, 9, 30), date(2026, 10, 3))
    assert _datas("28 Dec–3 Jan", 2026) == (date(2025, 12, 28), date(2026, 1, 3))
    assert _datas("18 Dec", 2025) == (date(2025, 12, 18), date(2025, 12, 18))
    assert _datas("sem data", 2026) == (None, None)


def test_par_de_valores_proximos_no_texto():
    vp = modulo("verificar-pesquisas")
    t = "Lula tem 45% e Flávio, 42% no primeiro turno. " + "x " * 300 + " Outro dado: 10%."
    assert vp.par(t, [45.0], [42.0]) == 0.0
    assert vp.par(t, [45.3], [42.4]) is not None and vp.par(t, [45.3], [42.4]) <= 0.5
    assert vp.par(t, [30.0], [20.0]) is None
    # numeros distantes demais no texto nao formam par
    longe = "Lula 45%. " + "x " * 400 + " Flávio 42%."
    assert vp.par(longe, [45.0], [42.0]) is None


def test_grupos_de_campo_pela_regra_de_tres():
    assert partidos.grupo3("PL") == "direita" and partidos.grupo3("Republicanos") == "direita"
    assert partidos.grupo3("MDB") == "centro" and partidos.grupo3("PSD") == "centro"
    assert partidos.grupo3("PT") == "esquerda" and partidos.grupo3("PSB") == "esquerda"
    assert partidos.grupo3("PSDB") == "centro" and partidos.grupo3("DEM") == "direita"
    assert partidos.grupo3("XYZ") == "sem classificacao"


def test_grupos_de_eventos_a_menos_de_30_dias():
    a4 = modulo("analise-4-eventos-e-candidato")
    ev = pd.DataFrame({"id": ["a", "b", "c"], "data": pd.to_datetime(["2026-05-01", "2026-05-20", "2026-08-01"]), "alvo": ["lula_governo", "lula_governo", "flavio_oposicao"]})
    g = a4.grupos(ev)
    assert [x["ids"] for x in g] == [["a", "b"], ["c"]]
    assert g[0]["direcao"] == 1 and g[1]["direcao"] == -1
    ev2 = ev.assign(alvo=["lula_governo", "flavio_oposicao", "ambos"])
    assert a4.grupos(ev2)[0]["direcao"] is None


def test_conferidor_de_linguagem_acha_o_que_deve():
    cl = modulo("conferir-linguagem")
    f = RAIZ / "tests" / "_tmp_linguagem.md"
    f.write_text("O candidato venceu a eleição — foi uma onda.\n", encoding="utf-8")
    try:
        # o conferidor trabalha com arquivos dentro do repositorio
        achados = cl.conferir(f)
    finally:
        f.unlink()
    assert any("venceu a eleição" in a for a in achados) and any("travessao" in a for a in achados) and any("onda" in a for a in achados)


def test_resumo_tem_as_chaves_centrais():
    import json
    r = json.load(open(RAIZ / "resultados" / "RESUMO.json", encoding="utf-8"))
    for k in ("a1", "a2", "a3", "a4", "b1", "b2", "h1", "h4", "h6", "h7", "h8", "h9", "h13", "placar", "val"):
        assert k in r, k
    assert abs(r["a1"]["virada_2022_2026"] - (r["a1"]["margem_2026"] - r["a1"]["margem_2022"])) < 1e-9
    assert r["val"]["independente"]["falham"] == []
