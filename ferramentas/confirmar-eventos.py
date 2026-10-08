"""Confirma a data de cada evento de dados/eventos.csv com duas reportagens independentes (docs/PRE_REGISTRO.md, secao 5).

Cada fonte e capturada (sha256 no manifesto) e precisa conter as palavras-chave do evento. Evento sem duas fontes que passam sai da
analise de H4 e e contado. Saida: dados/eventos_confirmados.csv e resultados/eventos_resumo.csv.
"""
from __future__ import annotations

import hashlib
import html
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from presidente.comum import BRUTOS, DADOS  # noqa: E402
from presidente.manifesto import baixar  # noqa: E402
from presidente.saida import registrar, tabela  # noqa: E402

# id: (data confirmada, [palavras-chave que a pagina precisa conter, todas], [urls])
CONFIRMA = {
    "V01": ("2025-04-23", ["INSS"], ["https://www.nsctotal.com.br/?p=7489108", "https://www.itatiaia.com.br/brasil/presidente-do-inss-e-afastado-em-operacao-que-apura-fraude-bilionaria-contra-aposentados/"]),
    "V02": ("2025-06-25", ["IOF"], ["https://www.band.com.br/noticias/camara-derruba-decreto-de-aumento-do-iof-202506251932", "https://exame.com/brasil/senado-confirma-derrubada-do-decreto-do-iof-e-congresso-impoe-derrota-historica-ao-governo", "https://diariodonordeste.verdesmares.com.br/negocios/congresso-aprova-derrubada-do-decreto-de-lula-sobre-aumento-do-iof-1.3663739", "https://sbtnews.sbt.com.br/noticia/politica/senado-derruba-alta-do-iof-e-impoe-derrota-ao-governo"]),
    "V03": ("2025-07-30", ["Magnitsky"], ["https://www.mobiletime.com.br/noticias/30/07/2025/trump-tarifa-50-porcento/", "https://sbtnews.sbt.com.br/noticia/politica/sbt-noticias-trump-oficializa-tarifa-de-50-ao-brasil-e-impoe-sancoes-a-alexandre-de-moraes"]),
    "V04": ("2025-09-11", ["Bolsonaro", "27 anos"], ["https://monitormercantil.com.br/primeira-turma-do-stf-mantem-pena-de-27-anos-para-bolsonaro/", "https://diariodonordeste.verdesmares.com.br/pontopoder/primeira-turma-do-stf-aprova-ata-do-julgamento-que-condenou-bolsonaro-1.3693468", "https://www.folhavitoria.com.br/politica/julgamento-de-bolsonaro-quais-os-proximos-passos-quando-a-pena-deve-passar-a-ser-cumprida/", "https://www.metropoles.com/brasil/trama-golpista-stf-condena-bolsonaro-a-27-anos-e-3-meses-de-prisao", "https://mais.opovo.com.br/jornal/politica/2025/09/13/prisao-de-bolsonaro-para-cumprimento-de-pena-tem-estimativa-de-ocorrer-ate-dezembro.html"]),
    "V09": ("2026-09-01", ["Vorcaro", "Moraes"], ["https://www.gazetasp.com.br/politica/flavio-bolsonaro-diz-que-mensagens-de-vorcaro-indicam-protecao-do-proprio-alexandre-de-moraes/", "https://gazetadopovo.com.br/eleicoes/2026/moraes-vota-em-colegio-de-sao-paulo-sob-crise-no-stf-por-relacao-com-vorcaro"]),
    "V12": ("2025-12-12", ["Magnitsky", "Moraes"], ["https://www.poder360.com.br/poder-internacional/eua-retiram-moraes-mulher-e-empresa-da-familia-da-magnitsky/", "https://www.infomoney.com.br/politica/eua-retiram-alexandre-de-moraes-da-lista-de-sancionados-pela-lei-magnitsky/"]),
    "V16": ("2025-12-07", ["Flávio", "preço"], ["https://www.poder360.com.br/poder-eleicoes/preco-para-nao-me-candidatar-e-bolsonaro-livre-nas-urnas-diz-flavio/", "https://www.congressoemfoco.com.br/noticia/114591/flavio-bolsonaro-fala-em-preco-para-desistir-de-disputar-planalto"]),
    "V17": ("2026-05-13", ["Vorcaro", "Flávio"], ["https://www.intercept.com.br/2026/05/13/flavio-bolsonaro-mentiu-banco-master-duas-vezes/", "https://www.opovo.com.br/agencia/bbc/2026/05/13/amp/ligacao-de-flavio-bolsonaro-e-vorcaro-abre-crise-na-campanha-bolsonarista-balde-de-agua-fria.html"]),
    "V19": ("2026-07-30", ["Lulinha"], ["https://www.opovo.com.br/noticias/mundo/2026/08/01/por-que-a-policia-federal-quer-investigar-lulinha.html", "https://www.band.com.br/nacional/por-que-a-policia-federal-quer-investigar-lulinha"]),
    "V21": ("2026-09-23", ["Record", "debate"], ["https://www.poder360.com.br/poder-midia/sem-lula-nem-flavio-record-cancela-debate-do-dia-27/", "https://www.oliberal.com/eleicoes/record-confirma-cancelamento-do-debate-presidencial-marcado-para-domingo-1.1172294"]),
    "V23": ("2026-09-24", ["Aparecida", "Flávio"], ["https://diariodonordeste.verdesmares.com.br/pontopoder/entenda-a-polemica-envolvendo-flavio-bolsonaro-e-nossa-senhora-aparecida-1.3794211", "https://sbtnews.sbt.com.br/noticia/politica/entenda-a-polemica-envolvendo-flavio-e-a-padroeira-do-brasil", "https://investidor10.com.br/noticias/flavio-quer-tirar-de-nossa-senhora-aparecida-o-titulo-de-padroeira-do-brasil-entenda-122845/", "https://ncnews.com.br/?p=52608"]),
    "V26": ("2026-09-30", ["Lula", "Globo", "debate"], ["https://www.bemparana.com.br/eleicoes-2026/lula-confirma-que-nao-vai-participar-do-debate-da-globo-nesta-quinta/", "https://tribunadejundiai.com.br/politica/eleicoes-2026/globo-cancela-ultimo-debate-presidencial-apos-ausencias-de-lula-e-flavio-bolsonaro-e-decisoes-da-justica/"]),
    "V27": ("2026-10-01", ["Globo", "debate"], ["https://www.cnnbrasil.com.br/eleicoes/tv-globo-cancela-debate-presidencial/", "https://www.jornalopcao.com.br/ultimas-noticias/globo-cancela-debate-presidencial-apos-decisoes-do-tse-e-do-stf-874361/"]),
}


MESES = ["janeiro", "fevereiro", "marco", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
ABREV = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def tem_data(t: str, iso: str, janela_dias: int = 3) -> bool:
    """A data (ou um dos dias seguintes, ate 'janela_dias') aparece no texto da pagina em algum formato comum."""
    from datetime import date, timedelta
    y, m, d = map(int, iso.split("-"))
    base = date(y, m, d)
    tn = t.lower().replace("ç", "c")
    for k in range(0, janela_dias + 1):
        x = base + timedelta(days=k)
        dd, mm = x.day, x.month
        pats = [rf"{dd}\s+de\s+{MESES[mm-1]}", rf"{dd:02d}/{mm:02d}", rf"{dd}/{mm}", rf"\({dd}\)", rf"dia\s+{dd}", rf"{dd}\.{ABREV[mm-1]}", rf"{x.isoformat()}"]
        if any(re.search(p, tn) for p in pats):
            return True
    return False


def publicada_perto(h: str, iso: str, janela: int = 3) -> bool:
    """Metadado de publicacao da pagina (article:published_time ou datePublished) a ate 'janela' dias depois do evento."""
    from datetime import date, timedelta
    y, m, d = map(int, iso.split("-"))
    base = date(y, m, d)
    for m_ in re.finditer(r'(?:published_time"\s+content="|"datePublished"\s*:\s*"|<time[^>]*datetime=")(\d{4})-(\d{2})-(\d{2})', h):
        p = date(int(m_.group(1)), int(m_.group(2)), int(m_.group(3)))
        if base <= p <= base + timedelta(days=janela):
            return True
    return False


def texto(h: str) -> str:
    h = re.sub(r"(?s)<(script|style|noscript)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(h))


def main() -> None:
    ev = pd.read_csv(DADOS / "eventos.csv", dtype=str)
    linhas = []
    for r in ev.itertuples():
        info = CONFIRMA.get(r.id)
        ok_fontes, ruins = [], []
        data = None
        if info:
            data, chaves, urls = info
            for u in urls:
                nome = hashlib.sha256(u.encode()).hexdigest()[:16] + ".html"
                try:
                    baixar(u, BRUTOS / "capturas-eventos" / nome, pausa=1.0, tentativas=2, minimo=2000)
                    bruto = (BRUTOS / "capturas-eventos" / nome).read_bytes().decode("utf-8", "ignore")
                    t = texto(bruto)
                    passa = all(k.lower() in t.lower() for k in chaves) and (tem_data(t, data) or publicada_perto(bruto, data))
                    (ok_fontes if passa else ruins).append(u)
                except RuntimeError:
                    ruins.append(u)
        confirmado = len(ok_fontes) >= 2
        linhas.append({"id": r.id, "evento": r.evento, "alvo": r.alvo, "tipo": r.tipo, "data_confirmada": data if confirmado else "", "confirmado": confirmado,
                       "fontes_ok": len(ok_fontes), "fontes_que_falharam": len(ruins), "urls_ok": " | ".join(ok_fontes)})
        print(r.id, "confirmado" if confirmado else "NAO CONFIRMADO", len(ok_fontes), len(ruins), flush=True)
    out = pd.DataFrame(linhas)
    out.to_csv(DADOS / "eventos_confirmados.csv", index=False, encoding="utf-8")
    tabela("eventos_resumo", out[["id", "evento", "alvo", "tipo", "data_confirmada", "confirmado", "fontes_ok"]])
    exp = out[out.tipo == "exposicao"]
    registrar("h4.eventos_na_lista", int(len(out)))
    registrar("h4.exposicoes_na_lista", int(len(exp)))
    registrar("h4.exposicoes_confirmadas", int(exp.confirmado.sum()))
    registrar("h4.exposicoes_removidas_sem_data_confirmada", int((~exp.confirmado).sum()))


if __name__ == "__main__":
    main()
