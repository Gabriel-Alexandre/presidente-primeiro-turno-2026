"""Bloco B, emenda 9: o erro de cada instituto em cinco rodadas (1o e 2o turno de 2018 e de 2022, 1o turno de 2026).

Pedido do autor (10/out/2026): avaliar pelo menos as duas eleicoes anteriores e esta, instituto por instituto, para ver se existe um
padrao, se algum instituto erra sempre para o mesmo lado e qual chega mais perto da urna.

Regras (docs/PRE_REGISTRO.md, emenda 9, escrita depois de ver o 1o turno de 2022 e de 2026 por instituto e antes de calcular as cinco
rodadas juntas):
- pesquisa: a ultima de cada instituto com fim de campo de 1 a 8 dias antes da votacao (boca de urna, no dia, nao entra);
  estimulada, nacional, cenario com o candidato do PL (Jair em 2018 e 2022, Flavio em 2026) e o do PT (Haddad em 2018, Lula depois);
- votos validos: 2018, o 'valid_result' do Pindograma (a coluna 'pct' da mesma base e o resultado da URNA, nao da pesquisa, e foi o
  erro da versao de 07/out); 2022, o 'result' de cada candidato sobre a soma dos candidatos do cenario; 2026, o valido da serie, com o
  valor da fonte original quando a conferencia achou diferenca (Futura de 03/out, PDF do instituto);
- erro = margem da pesquisa (PL menos PT) menos margem da urna; negativo = mostrou o candidato do PL mais fraco do que ele foi;
- 'chegou perto' = erro de ate 4 pontos na margem (a margem de erro tipica de 2 pontos por candidato vira ate 4 na diferenca);
- 'puxa sempre para o mesmo lado' = instituto em 3 rodadas ou mais, todas com erro no mesmo sentido, e erro medio de 2 pontos ou mais;
- ranking de precisao: erro absoluto medio, so institutos em 3 rodadas ou mais.
Nada aqui diz por que um instituto errou. Erro e direcao do erro se medem; intencao, nao.
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import CONGRESSO, RES  # noqa: E402
from presidente.saida import ler, registrar, tabela  # noqa: E402

PERTO = 4.0
NOMES = {"Ipec (antigo Ibope)": "Ipec (antigo Ibope)", "Ibope": "Ipec (antigo Ibope)", "DataPoder360": "PoderData", "PoderData": "PoderData",
         "Real Time": "Real Time Big Data", "Real Time Big Data": "Real Time Big Data", "Ideia": "Ideia", "Ideia Big Data": "Ideia",
         "FSB Pesquisa": "FSB", "Paraná Pesquisas": "Paraná Pesquisas", "Veritá": "Veritá"}


def nome(n: str) -> str:
    return NOMES.get(n, n)


def urna() -> dict:
    v = ler("a1.validacao")
    out = {}
    # 1o turno: percentuais validos do bloco A (com o exterior); 2o turno: os dois candidatos sao todo o voto valido
    for chave, pl, pt in (("2018_2", "jair", "haddad"), ("2022_2", "jair", "lula")):
        n = v[chave]["nacional_meu"]
        out[chave.replace("_", "-")] = (100 * n[pl] / (n[pl] + n[pt]), 100 * n[pt] / (n[pl] + n[pt]))
    for ano in (2018, 2022, 2026):
        out[f"{ano}-1"] = (ler(f"a1.pl_pct_{ano}"), ler(f"a1.pt_pct_{ano}"))
    return out


DATAS = {"2018-1": date(2018, 10, 7), "2018-2": date(2018, 10, 28), "2022-1": date(2022, 10, 2), "2022-2": date(2022, 10, 30), "2026-1": date(2026, 10, 4)}


def ultima(df: pd.DataFrame, rodada: str) -> pd.DataFrame:
    e = DATAS[rodada]
    w = df[(df.fim >= pd.Timestamp(e - timedelta(days=8))) & (df.fim < pd.Timestamp(e))].copy()
    w = w.sort_values(["instituto", "fim", "n_cand"]).groupby("instituto").tail(1)
    w["rodada"] = rodada
    return w[["rodada", "instituto", "fim", "pl", "pt"]]


def pindograma(ano: int, turno: int) -> pd.DataFrame:
    if ano == 2018:
        a = pd.read_csv(CONGRESSO / "dados/brutos/capturas/pindograma-late-polls-2012-2018.csv", low_memory=False)
        a = a[(a.year == 2018) & (a.CD_CARGO == 1) & (a.turno == turno) & (a.polled_UE == "BR") & (a.estimulada == 1) & (a.NUMERO_CANDIDATO > 0)].copy()
        a["valido"] = a.valid_result
        pl_n, pt_n = 17, 13
    else:
        a = pd.read_csv(CONGRESSO / "dados/brutos/capturas/pindograma-late-polls-2022.csv", low_memory=False)
        a = a[(a.CD_CARGO == 1) & (a.turno == turno) & (a.polled_UE == "BR") & (a.estimulada == 1) & (a.NUMERO_CANDIDATO > 0)].copy()
        a["valido"] = 100 * a.result / a.groupby(["NR_IDENTIFICACAO_PESQUISA", "scenario_id"]).result.transform("sum")
        pl_n, pt_n = 22, 13
    a["fim"] = pd.to_datetime(a.DT_FIM_PESQUISA)
    a["n_cand"] = a.groupby(["NR_IDENTIFICACAO_PESQUISA", "scenario_id"]).NUMERO_CANDIDATO.transform("nunique")
    a["instituto"] = a.pretty_name.map(nome)
    p = a.pivot_table(index=["NR_IDENTIFICACAO_PESQUISA", "scenario_id", "instituto", "fim", "n_cand"], columns="NUMERO_CANDIDATO", values="valido", aggfunc="first").reset_index()
    p = p.rename(columns={pl_n: "pl", pt_n: "pt"}).dropna(subset=["pl", "pt"])
    return ultima(p, f"{ano}-{turno}")


def serie_2026() -> pd.DataFrame:
    p = pd.read_csv(RES / "b1_pesquisas.csv", parse_dates=["campo_fim"])
    p = p.rename(columns={"campo_fim": "fim", "valido_Flavio": "pl", "valido_Lula": "pt"})
    p["instituto"] = p.instituto.map(nome)
    p["n_cand"] = 0
    u = ultima(p, "2026-1")
    # valores conferidos na fonte original em 11/out/2026 (dados/CAPTURAS_INSTITUTOS.csv); quando a fonte difere da tabela, vale a fonte
    conf = pd.read_csv(Path(__file__).resolve().parent.parent / "dados" / "CAPTURAS_INSTITUTOS.csv")
    for r in conf.itertuples():
        m = (u.instituto == r.instituto) & (u.fim == pd.Timestamp(r.campo_fim))
        if r.valido_flavio == r.valido_flavio and m.any():
            u.loc[m, ["pl", "pt"]] = [r.valido_flavio, r.valido_lula]
    u = u.merge(conf[["instituto", "campo_fim", "conferida"]].assign(fim=lambda d: pd.to_datetime(d.campo_fim)).drop(columns="campo_fim"), on=["instituto", "fim"], how="left")
    u["conferida"] = u.conferida.astype("boolean").fillna(False).astype(bool)
    return u


def contexto_2014() -> None:
    """Contexto, fora das cinco rodadas: 2014, o principal candidato contra o PT (Aecio, PSDB, 45) contra Dilma (PT, 13).
    Urna (TSE): 1o turno Aecio 33,55% e Dilma 41,59% dos validos; 2o turno Aecio 48,36% e Dilma 51,64%."""
    a = pd.read_csv(CONGRESSO / "dados/brutos/capturas/pindograma-late-polls-2012-2018.csv", low_memory=False)
    a = a[(a.year == 2014) & (a.CD_CARGO == 1) & (a.polled_UE == "BR") & (a.estimulada == 1) & (a.NUMERO_CANDIDATO > 0)].copy()
    a["fim"] = pd.to_datetime(a.DT_FIM_PESQUISA)
    out = {}
    for turno, e, psdb, pt in ((1, date(2014, 10, 5), 33.55, 41.59), (2, date(2014, 10, 26), 48.36, 51.64)):
        x = a[(a.turno == turno) & (a.fim >= pd.Timestamp(e - timedelta(days=8))) & (a.fim < pd.Timestamp(e))]
        p = x.pivot_table(index=["NR_IDENTIFICACAO_PESQUISA", "scenario_id", "pretty_name", "fim"], columns="NUMERO_CANDIDATO", values="valid_result", aggfunc="first").reset_index()
        p = p.dropna(subset=[45, 13]).sort_values("fim").groupby("pretty_name").tail(1)
        p["erro"] = (p[45] - p[13]) - (psdb - pt)
        p["erro_oposicao"] = p[45] - psdb
        out[f"2014-{turno}"] = {"institutos": int(len(p)), "erro_mediano": round(float(p.erro.median()), 2),
                                "mostraram_a_oposicao_mais_fraca": int((p.erro < 0).sum()), "erro_oposicao_mediano": round(float(p.erro_oposicao.median()), 2),
                                "por_instituto": {r.pretty_name: round(float(r.erro), 2) for r in p.itertuples()}}
    registrar("b6.contexto_2014", out)


def main() -> None:
    U = urna()
    rod = [pindograma(2018, 1), pindograma(2018, 2), pindograma(2022, 1), pindograma(2022, 2), serie_2026()]
    e = pd.concat(rod, ignore_index=True)
    e["conferida"] = e.conferida.astype("boolean").fillna(True).astype(bool)  # 2018 e 2022: base do Pindograma, conferida contra a imprensa no projeto do Congresso
    e["pl_urna"] = e.rodada.map(lambda r: U[r][0])
    e["pt_urna"] = e.rodada.map(lambda r: U[r][1])
    e["margem_pesquisa"] = e.pl - e.pt
    e["margem_urna"] = e.pl_urna - e.pt_urna
    e["erro"] = e.margem_pesquisa - e.margem_urna
    e["erro_pl"] = e.pl - e.pl_urna  # negativo: a pesquisa deu menos ao candidato do PL do que a urna
    e["erro_pt"] = e.pt - e.pt_urna
    e["perto"] = e.erro.abs() <= PERTO
    e["acertou_quem_ficou_na_frente"] = np.sign(e.margem_pesquisa) == np.sign(e.margem_urna)
    e["fim"] = e.fim.dt.date
    tabela("b6_erro_por_instituto_e_rodada", e.round(2))

    por_rodada = {}
    for r, x in e.groupby("rodada"):
        por_rodada[r] = {"institutos": int(len(x)), "erro_mediano": round(float(x.erro.median()), 2), "erro_medio": round(float(x.erro.mean()), 2),
                         "mostraram_pl_mais_fraco": int((x.erro < 0).sum()), "mostraram_pl_mais_forte": int((x.erro > 0).sum()),
                         "chegaram_perto": int(x.perto.sum()), "acertaram_quem_ficou_na_frente": int(x.acertou_quem_ficou_na_frente.sum()),
                         "margem_urna": round(float(x.margem_urna.iloc[0]), 2),
                         "erro_pl_mediano": round(float(x.erro_pl.median()), 2), "erro_pt_mediano": round(float(x.erro_pt.median()), 2),
                         "so_conferidas_erro_mediano": round(float(x[x.conferida].erro.median()), 2)}
    registrar("b6.por_rodada", por_rodada)

    g = e.groupby("instituto").agg(rodadas=("erro", "size"), erro_medio=("erro", "mean"), erro_absoluto_medio=("erro", lambda s: s.abs().mean()),
                                    pl_mais_fraco=("erro", lambda s: int((s < 0).sum())), pl_mais_forte=("erro", lambda s: int((s > 0).sum())),
                                    chegou_perto=("perto", "sum"), pior_erro=("erro", lambda s: s.loc[s.abs().idxmax()]),
                                    rodadas_lista=("rodada", lambda s: ", ".join(s))).reset_index()

    def direcao(r):
        if r.rodadas < 3:
            return "poucas rodadas"
        if r.pl_mais_fraco == r.rodadas and abs(r.erro_medio) >= 2:
            return "sempre mostrou o PL mais fraco"
        if r.pl_mais_forte == r.rodadas and abs(r.erro_medio) >= 2:
            return "sempre mostrou o PL mais forte"
        return "sem lado fixo"
    g["direcao"] = g.apply(direcao, axis=1)
    g = g.sort_values(["rodadas", "erro_absoluto_medio"], ascending=[False, True])
    tabela("b6_institutos", g.round(2))
    tres = g[g.rodadas >= 3].sort_values("erro_absoluto_medio")
    registrar("b6.institutos_com_3_rodadas_ou_mais", [
        {k: (round(float(v), 2) if isinstance(v, (float, np.floating)) else (int(v) if isinstance(v, (np.integer,)) else v)) for k, v in r.items()}
        for r in tres.to_dict("records")])
    registrar("b6.todas_as_rodadas", {"pesquisas": int(len(e)), "mostraram_pl_mais_fraco": int((e.erro < 0).sum()), "mostraram_pl_mais_forte": int((e.erro > 0).sum()),
                                      "chegaram_perto": int(e.perto.sum())})
    # sinal: rodadas com mediana negativa
    registrar("b6.rodadas_com_mediana_contra_o_pl", int(sum(1 for v in por_rodada.values() if v["erro_mediano"] < 0)))
    contexto_2014()
    with pd.option_context("display.width", 250):
        print(pd.DataFrame(por_rodada).T)
    print(tres[["instituto", "rodadas", "erro_medio", "erro_absoluto_medio", "pl_mais_fraco", "pl_mais_forte", "chegou_perto", "direcao", "rodadas_lista"]].to_string())


if __name__ == "__main__":
    main()
