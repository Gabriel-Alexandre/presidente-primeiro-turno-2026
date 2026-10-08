"""Caminhos, ponte para os dois repositorios de origem (lidos por hash) e definicoes comuns."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"
BRUTOS = DADOS / "brutos"
DER = DADOS / "derivados"
RES = RAIZ / "resultados"
FIG = RES / "figuras"
FIG_VIDEO = FIG / "video"

SEMENTE = 20261007

UFS = "AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO".split()
REGIAO = {}
for _r, _ufs in {
    "Norte": "AC AM AP PA RO RR TO", "Nordeste": "AL BA CE MA PB PE PI RN SE",
    "Centro-Oeste": "DF GO MS MT", "Sudeste": "ES MG RJ SP", "Sul": "PR RS SC",
}.items():
    for _u in _ufs.split():
        REGIAO[_u] = _r


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _origem(var: str, padrao: str) -> Path:
    return Path(os.environ.get(var, str(RAIZ.parent / padrao))).resolve()


APURACAO = _origem("PRESIDENTE_APURACAO", "apuracao-eleicoes-2026")
CONGRESSO = _origem("PRESIDENTE_CONGRESSO", "congresso-e-governos-eleicoes-2026")


def verificar_fontes() -> dict:
    """Confere os hashes declarados em dados/FONTE_*.json. Levanta erro se algo mudou."""
    ap = json.loads((DADOS / "FONTE_APURACAO.json").read_text(encoding="utf-8"))
    co = json.loads((DADOS / "FONTE_CONGRESSO.json").read_text(encoding="utf-8"))
    achado = sha256(APURACAO / ap["manifesto"])
    if achado != ap["manifesto_sha256"]:
        raise RuntimeError(f"manifesto da apuracao mudou: {achado} != {ap['manifesto_sha256']}")
    for rel, esperado in co["arquivos"].items():
        achado = sha256(CONGRESSO / rel)
        if achado != esperado:
            raise RuntimeError(f"{rel} mudou: {achado} != {esperado}")
    return {"apuracao_manifesto": ap["manifesto_sha256"], "congresso_arquivos": len(co["arquivos"])}


def derivado_apuracao(uf: str, ano: int | None = None, turno: int = 1) -> tuple[Path, Path]:
    """(votos, secoes) de uma UF. ano=None e 2026."""
    base = APURACAO / "dados" / "derivados"
    uf = uf.lower()
    if ano is None:
        return base / "uf" / f"{uf}-votos.parquet", base / "uf" / f"{uf}-secoes.parquet"
    return base / "historico" / f"{ano}-{turno}-{uf}-votos.parquet", base / "historico" / f"{ano}-{turno}-{uf}-secoes.parquet"
