"""Manifesto de arquivos baixados: sha256, URL e data. Todo download passa por aqui."""
from __future__ import annotations

import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from .comum import DADOS, RAIZ

MANIFESTO = DADOS / "MANIFESTO.json"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"


def carregar() -> dict:
    return json.loads(MANIFESTO.read_text(encoding="utf-8")) if MANIFESTO.exists() else {"arquivos": {}}


def salvar(m: dict) -> None:
    MANIFESTO.write_text(json.dumps(m, indent=1, ensure_ascii=False, sort_keys=True), encoding="utf-8")


def baixar(url: str, destino: Path, *, forcar: bool = False, pausa: float = 1.0, tentativas: int = 4, minimo: int = 200) -> dict:
    """Baixa com curl (uma requisicao por vez), grava no manifesto. Nao repete URL ja baixada."""
    m = carregar()
    chave = str(destino.relative_to(RAIZ)).replace("\\", "/")
    if chave in m["arquivos"] and destino.exists() and not forcar:
        return m["arquivos"][chave]
    destino.parent.mkdir(parents=True, exist_ok=True)
    for t in range(tentativas):
        r = subprocess.run(["curl", "-sL", "-m", "600", "-A", UA, "-o", str(destino), "-w", "%{http_code}", url], capture_output=True, text=True)
        cod = r.stdout.strip()
        if r.returncode == 0 and cod == "200" and destino.stat().st_size >= minimo:
            break
        time.sleep(3 * (t + 1))
    else:
        raise RuntimeError(f"falhou {url} (http {cod})")
    h = hashlib.sha256()
    with open(destino, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    ent = {"url": url, "bytes": destino.stat().st_size, "sha256": h.hexdigest(), "baixado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    m = carregar()
    m["arquivos"][chave] = ent
    salvar(m)
    time.sleep(pausa)
    return ent
