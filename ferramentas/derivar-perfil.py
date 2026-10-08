"""Perfil do eleitorado apto por municipio, 2022 e 2026 (dados abertos do TSE): faixa etaria, escolaridade e sexo.

Saida: dados/derivados/perfil_eleitorado.parquet (ano, uf, mun, aptos_perfil, parcelas por faixa etaria, escolaridade e sexo).
Conferencia (docs/PRE_REGISTRO.md, secao 9): o total por municipio contra o eleitorado apto dos boletins (resultados/val_perfil.csv).
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import BRUTOS, DER  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402

IDADE = {"1600": "i16_17", "1700": "i16_17", "1800": "i18_24", "1900": "i18_24", "2000": "i18_24", "2124": "i18_24",
         "2529": "i25_44", "3034": "i25_44", "3539": "i25_44", "4044": "i25_44", "4549": "i45_59", "5054": "i45_59", "5559": "i45_59",
         "6064": "i60_mais", "6569": "i60_mais", "7074": "i60_mais", "7579": "i60_mais", "8084": "i60_mais", "8589": "i60_mais", "9094": "i60_mais",
         "9599": "i60_mais", "9999": "i60_mais", "-3": None}
ESC = {"1": "e_fund", "2": "e_fund", "3": "e_fund", "4": "e_fund", "5": "e_medio", "6": "e_medio", "7": "e_superior", "8": "e_superior", "9": "e_superior"}


def um(ano: int) -> pd.DataFrame:
    z = zipfile.ZipFile(BRUTOS / "tse" / f"perfil_eleitorado_{ano}.zip")
    partes = []
    for i in z.infolist():
        if not i.filename.endswith(".csv") or "BRASIL" in i.filename.upper():
            continue  # o arquivo nacional repete os estaduais
        for ch in pd.read_csv(z.open(i.filename), sep=";", encoding="latin-1", dtype=str, chunksize=500_000,
                              usecols=["SG_UF", "CD_MUNICIPIO", "CD_GENERO", "CD_FAIXA_ETARIA", "CD_GRAU_ESCOLARIDADE", "QT_ELEITORES"]):
            ch["n"] = pd.to_numeric(ch.QT_ELEITORES, errors="coerce").fillna(0)
            ch["idade"] = ch.CD_FAIXA_ETARIA.map(IDADE)
            ch["esc"] = ch.CD_GRAU_ESCOLARIDADE.map(ESC).fillna("e_fund")  # 1 a 4: analfabeto, le e escreve, fundamental; -3/outros: tratados como fundamental
            ch["sexo"] = ch.CD_GENERO.map({"4": "feminino", "2": "masculino"})  # 2 masculino, 4 feminino
            partes.append(ch)
    d = pd.concat(partes, ignore_index=True)
    d["mun"] = d.CD_MUNICIPIO.astype(int)
    chave = ["SG_UF", "mun"]
    tot = d.groupby(chave).n.sum().rename("aptos_perfil")
    out = tot.to_frame()
    for col in ("idade", "esc", "sexo"):
        t = d.dropna(subset=[col]).pivot_table(index=chave, columns=col, values="n", aggfunc="sum", fill_value=0)
        out = out.join(t.div(t.sum(axis=1), axis=0).add_prefix("p_" if col != "idade" else "p_"))
    out = out.reset_index().rename(columns={"SG_UF": "uf"})
    out["ano"] = ano
    return out


def main() -> None:
    d = pd.concat([um(2022), um(2026)], ignore_index=True)
    DER.mkdir(parents=True, exist_ok=True)
    d.to_parquet(DER / "perfil_eleitorado.parquet", index=False)
    v = pd.read_parquet(DER / "mun_presidente.parquet")
    v = v[(v.turno == 1)][["ano", "uf", "mun", "aptos"]]
    x = d.merge(v, on=["ano", "uf", "mun"], how="inner")
    x["dif"] = x.aptos_perfil - x.aptos
    x["dif_pct"] = 100 * x.dif / x.aptos
    for ano in (2022, 2026):
        y = x[x.ano == ano]
        registrar(f"a1.validacao_perfil.{ano}", {"municipios": len(y), "dif_total": int(y.dif.sum()), "dif_total_pct": float(100 * y.dif.sum() / y.aptos.sum()),
                                                  "municipios_com_dif_acima_5pct": int((y.dif_pct.abs() > 5).sum()), "mediana_dif_pct": float(y.dif_pct.median())})
    tabela("val_perfil", x[x.dif_pct.abs() > 5].sort_values("dif_pct"))
    print(d.groupby("ano")[["aptos_perfil"]].sum())


if __name__ == "__main__":
    main()
