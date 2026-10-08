"""Passada 3 da revisao: confere palavras proibidas, travessao, 'venceu a eleicao' e adjetivos sem medida em texto publico.

Uso: python ferramentas/conferir-linguagem.py [arquivo ...]   (sem argumento, confere os textos publicos do repositorio)
Sai com codigo 1 se achar algo. A lista vem de .cursor/rules/presidente-fundamentos.mdc e de docs/PRE_REGISTRO.md, secao 11.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PROIBIDAS = ["fraude", "manipulada", "manipulado", "comprada", "encomendada", "tendenciosa", "massacre", "humilhação", "lavada", "varrida", "mentiu", "mentira", "corrupto", "culpado", "deslize", "venceu a eleição", "foi eleito presidente"]
ADJETIVOS = ["histórica", "histórico", "onda", "recorde", "avassalador", "esmagador", "arrasador"]
PUBLICOS = ["README.md", "RELATORIO.md", "RESUMO_SIMPLES.md", "docs/LEITURA_DA_IA.md", "analise-da-ia/DOSSIE.md"]
# a lista de palavras proibidas aparece de proposito nestes arquivos de regra
IGNORAR_PROIBIDAS = {"docs/PRE_REGISTRO.md", ".cursor/rules/presidente-fundamentos.mdc", "analise-da-ia/REGRAS_DO_VEREDITO.md", "CLAUDE.md", "docs/REVISAO_ADVERSARIAL.md"}


def conferir(caminho: Path) -> list[str]:
    rel = str(caminho.relative_to(RAIZ)).replace("\\", "/")
    texto = caminho.read_text(encoding="utf-8")
    achados = []
    for n, linha in enumerate(texto.splitlines(), 1):
        baixa = linha.lower()
        if rel not in IGNORAR_PROIBIDAS:
            for p in PROIBIDAS:
                for m in re.finditer(rf"(?<!\w){re.escape(p)}(?!\w)", baixa):
                    antes = baixa[max(0, m.start() - 14):m.start()]
                    if p in ("venceu a eleição", "foi eleito presidente") and re.search(r"(não|nunca|nem) (ele )?$", antes):
                        continue  # a negacao e permitida: 'ele não venceu a eleição'
                    achados.append(f"{rel}:{n}: palavra proibida '{p}'")
        if "—" in linha or "–" in linha:
            achados.append(f"{rel}:{n}: travessao")
        for a in ADJETIVOS:
            if re.search(rf"(?<!\w){a}(?!\w)", baixa) and "adjetivo" not in baixa:
                achados.append(f"{rel}:{n}: adjetivo sem medida '{a}'")
    return achados


def main() -> int:
    alvos = [RAIZ / a for a in (sys.argv[1:] or PUBLICOS) if (RAIZ / a).exists()]
    tudo = []
    for a in alvos:
        tudo += conferir(a)
    for t in tudo:
        print(t)
    print(f"{len(alvos)} arquivos conferidos, {len(tudo)} achados")
    return 1 if tudo else 0


if __name__ == "__main__":
    sys.exit(main())
