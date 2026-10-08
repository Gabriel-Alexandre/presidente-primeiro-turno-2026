"""Verificacoes numericas da revisao adversarial (docs/REVISAO_ADVERSARIAL.md). Escreve em resultados/RESUMO.json (chave 'revisao') e em resultados/revisao_*.csv.

1. O movimento de campanha (3/ago a 28/set) depende da correcao de instituto? (serie sem correcao e por instituto)
2. O sinal de religiao e de envelhecimento muda ao controlar pelo voto de Jair em 2022 (efeito teto)?
3. Os erros de 2026 e os episodios aguentam deixar um instituto de fora por vez?
4. A fracao dos 'outros' que fica com o candidato do PL muda se so os 3 maiores institutos forem usados?
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import RES, verificar_fontes  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402


def carregar(nome: str):
    spec = importlib.util.spec_from_file_location(nome.replace("-", "_"), Path(__file__).resolve().parent / f"{nome}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main() -> None:
    verificar_fontes()
    out = {}
    # 1. campanha sem correcao e por instituto
    p = pd.read_csv(RES / "b1_pesquisas.csv", parse_dates=["campo_fim"])
    p["semana"] = p.campo_fim.dt.to_period("W-SUN").dt.start_time
    sem = p.groupby("semana").agg(raw=("margem", "mean"), aj=("margem_aj", "mean"))
    a, b = pd.Timestamp("2026-08-03"), pd.Timestamp("2026-09-28")
    out["campanha_sem_correcao_de_instituto"] = {"3_ago": float(sem.loc[a, "raw"]), "28_set": float(sem.loc[b, "raw"]), "movimento": float(sem.loc[b, "raw"] - sem.loc[a, "raw"])}
    por = []
    for nome, g in p[(p.campo_fim >= "2026-08-01") & (p.campo_fim <= "2026-10-03")].groupby("instituto"):
        g = g.sort_values("campo_fim")
        if len(g) >= 4:
            por.append({"instituto": nome, "pesquisas": len(g), "primeira": g.campo_fim.iloc[0].date(), "ultima": g.campo_fim.iloc[-1].date(), "margem_primeira": g.margem.iloc[0], "margem_ultima": g.margem.iloc[-1], "movimento": g.margem.iloc[-1] - g.margem.iloc[0]})
    t = pd.DataFrame(por)
    tabela("revisao_campanha_por_instituto", t)
    out["campanha_por_instituto"] = {"institutos": int(len(t)), "movimento_minimo": float(t.movimento.min()), "movimento_maximo": float(t.movimento.max()), "institutos_com_movimento_positivo": int((t.movimento > 0).sum())}

    # 2. controle pelo voto de Jair em 2022
    a6 = carregar("analise-6-municipal")
    m = a6.base()
    for c in ("pct_evangelicos", "pct_urbana", "pct_superior", "pct_pretos_pardos", "log_pib_pc", "d_jov", "d_p_i60_mais", "d_p_e_superior", "jair22"):
        m["z_" + c] = a6.z(m[c])
    base8 = ["z_pct_evangelicos", "z_pct_urbana", "z_pct_superior", "z_pct_pretos_pardos", "z_log_pib_pc"]
    r = {}
    for nome, xs, foco in (("religiao_sem_controle", base8, "z_pct_evangelicos"), ("religiao_com_jair22", base8 + ["z_jair22"], "z_pct_evangelicos"),
                           ("idade_sem_controle", ["z_d_jov", "z_d_p_i60_mais", "z_d_p_e_superior", "z_pct_urbana"], "z_d_p_i60_mais"), ("idade_com_jair22", ["z_d_jov", "z_d_p_i60_mais", "z_d_p_e_superior", "z_pct_urbana", "z_jair22"], "z_d_p_i60_mais")):
        f = a6.ajustar(m, "V", xs)
        r[nome] = a6.linha(f, foco)
    out["controle_pelo_voto_de_jair_2022"] = r

    # 3. deixar um instituto de fora por vez
    e = pd.read_csv(RES / "b2_erro_por_instituto.csv")
    e = e[e.verificada & (e.ano == 2026)]
    out["erro_2026_sem_um_instituto"] = {"media_min": float(min(e[e.instituto != i].erro_margem.mean() for i in e.instituto)), "media_max": float(max(e[e.instituto != i].erro_margem.mean() for i in e.instituto)),
                                         "mediana_min": float(min(e[e.instituto != i].erro_margem.median() for i in e.instituto)), "mediana_max": float(max(e[e.instituto != i].erro_margem.median() for i in e.instituto))}
    ev = pd.read_csv(RES / "h4_eventos_por_instituto.csv")
    for ids in ("V17", "V19"):
        x = ev[ev.ids == ids]
        med = [float(x[x.instituto != i].delta.median()) for i in x.instituto]
        out[f"{ids}_sem_um_instituto"] = {"mediana_min": min(med), "mediana_max": max(med), "n": int(len(x)), "sinal_mantido_em_todos": bool(all(np.sign(v) == np.sign(x.delta.median()) for v in med))}

    # 4. fracao dos outros com so os tres institutos de mais rodadas
    b = pd.read_csv(RES / "b2_erro_por_instituto.csv")
    b = b[b.verificada & (b.ano == 2026) & b.instituto.isin(["Datafolha", "Quaest", "PoderData", "MDA", "Real Time"])]
    out["fracao_pl_so_5_institutos_conhecidos"] = {"institutos": b.instituto.tolist(), "fracao_media": float(b.fracao_pl.mean()), "fracao_minima": float(b.fracao_pl.min())}
    registrar("revisao", out)
    import json
    print(json.dumps(out, indent=1, ensure_ascii=False, default=float))


if __name__ == "__main__":
    main()
