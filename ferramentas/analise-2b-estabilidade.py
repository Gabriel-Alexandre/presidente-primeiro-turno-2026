"""Recalcula as marcacoes de estabilidade da A4 (tres criterios) a partir de resultados/a4_matriz_transicao.csv, sem refazer os ajustes."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import RES  # noqa: E402
from presidente.ecologica import estabilidade  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402


def main() -> None:
    est = estabilidade(pd.read_csv(RES / "a4_matriz_transicao.csv"))
    tabela("a4_estabilidade", est)
    for r in est.itertuples():
        registrar(f"a4.fluxo.{r.origem}_para_{r.destino}", {"B_amplo": None if pd.isna(r.B_amplo) else r.B_amplo, "B_enxuto": r.B_enxuto, "min_regioes": r.min_regioes, "max_regioes": r.max_regioes,
                                                              "nacional_dentro_das_regioes": r.nacional_dentro_das_regioes, "robusto": bool(r.robusto)})
    print(est.round(3).to_string())


if __name__ == "__main__":
    main()
