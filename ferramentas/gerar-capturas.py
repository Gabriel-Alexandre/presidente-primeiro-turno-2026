"""Gera dados/CAPTURAS.csv: cada pagina de imprensa capturada, com URL, sha256, assunto e o trecho copiado (nao parafraseado).

Eventos: o trecho e a frase da pagina que contem a primeira palavra-chave do evento. Pesquisas: a frase que contem 'Lula' e '%'.
Se o trecho nao for encontrado, a linha sai com status 'trecho_nao_encontrado' e a fonte nao pode ser citada no relatorio.
"""
from __future__ import annotations

import csv
import hashlib
import html
import importlib.util
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import BRUTOS, DADOS  # noqa: E402
from presidente.manifesto import carregar  # noqa: E402

spec = importlib.util.spec_from_file_location("ce", Path(__file__).resolve().parent / "confirmar-eventos.py")
ce = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ce)


def texto(h: str) -> str:
    h = re.sub(r"(?s)<(script|style|noscript)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(h))


def trecho(t: str, chaves: list[str]) -> str | None:
    for k in chaves:
        i = t.lower().find(k.lower())
        if i >= 0:
            ini = max(t.rfind(". ", 0, i) + 2, i - 280)
            fim = t.find(". ", i)
            fim = i + 280 if fim < 0 else min(fim + 1, i + 280)
            return t[ini:fim].strip()
    return None


def main() -> None:
    m = carregar()["arquivos"]
    por_url = {}
    for eid, (data, chaves, urls) in ce.CONFIRMA.items():
        for u in urls:
            por_url[hashlib.sha256(u.encode()).hexdigest()[:16] + ".html"] = (u, f"evento {eid}, data {data}", chaves)
    linhas = []
    for rel, ent in sorted(m.items()):
        nome = rel.rsplit("/", 1)[-1]
        if "capturas-eventos" in rel and nome in por_url:
            u, assunto, chaves = por_url[nome]
        elif "capturas-pesquisas" in rel:
            u, assunto, chaves = ent["url"], "pesquisa de presidente citada pela Wikipedia (conferencia de valores)", ["Lula"]
        else:
            continue
        p = DADOS.parent / rel
        t = texto(p.read_bytes().decode("utf-8", "ignore")) if p.exists() else ""
        tr = trecho(t, chaves) if t else None
        linhas.append({"id": nome.replace(".html", ""), "url": u, "capturado_utc": ent["baixado_utc"], "bytes": ent["bytes"], "sha256": ent["sha256"], "status": "ok" if tr else "trecho_nao_encontrado", "assunto": assunto, "trecho": (tr or "")[:300]})
    pd.DataFrame(linhas).to_csv(DADOS / "CAPTURAS.csv", index=False, encoding="utf-8", quoting=csv.QUOTE_MINIMAL)
    ok = sum(1 for l in linhas if l["status"] == "ok")
    print(len(linhas), "capturas,", ok, "com trecho")


if __name__ == "__main__":
    main()
