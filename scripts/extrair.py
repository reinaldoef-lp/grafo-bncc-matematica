#!/usr/bin/env python3
"""Extrai da API do bncc.dev as habilidades de Matemática do 6º ao 9º ano.

Salva dois arquivos em dados/bruto/:

  ma-ef-6-9.json    todas as habilidades de Matemática, 6º ao 9º ano
  numeros-6-9.json  recorte da unidade temática "Números"

A resposta da API é gravada sem alteração. A cadeia de números racionais
fracionários vive dentro de "Números", e o recorte é feito pela unidade
temática — não por busca textual.

Motivo, verificado em 19/07/2026: a busca da API é literal, sem stemming.
"fração" devolve EF06MA09, EF07MA09, EF08MA05; "frações" devolve outras
duas (EF06MA07, EF07MA08), sem repetir nenhuma; "fracion" devolve mais
cinco. Confiar em um único termo perde parte da cadeia em silêncio.

Para não trocar um recorte frágil por outro, a extração roda também uma
verificação cruzada: busca vários termos e reporta o que aparece FORA da
unidade temática, para inspeção manual.

Uso: python3 scripts/extrair.py
"""

import json
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.bncc.dev/v1/habilidades"
BUSCA = "https://api.bncc.dev/v1/busca"
ANOS = [6, 7, 8, 9]
UNIDADE = "Números"
TERMOS = ["fração", "frações", "fracion", "racionais", "decimal", "porcentagem"]
DESTINO = Path(__file__).resolve().parent.parent / "dados" / "bruto"


def buscar(ano):
    url = f"{API}?etapa=EF&componente=MA&ano={ano}&limite=100"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def buscar_termo(termo, ano):
    q = urllib.parse.quote(termo)
    url = f"{BUSCA}?q={q}&etapa=EF&componente=MA&ano={ano}&limite=50"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)["itens"]


def unidade_de(item):
    return item.get("organizacao", {}).get("nomes", {}).get("unidadeTematica")


def main():
    DESTINO.mkdir(parents=True, exist_ok=True)

    por_ano = {}
    todas = []
    for ano in ANOS:
        resposta = buscar(ano)
        por_ano[str(ano)] = resposta
        todas.extend(resposta["itens"])
        print(f"{ano}º ano: {resposta['total']} habilidades")

    (DESTINO / "ma-ef-6-9.json").write_text(
        json.dumps(por_ano, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    numeros = [i for i in todas if unidade_de(i) == UNIDADE]
    (DESTINO / "numeros-6-9.json").write_text(
        json.dumps(numeros, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\ntotal: {len(todas)} habilidades")
    print(f'unidade "{UNIDADE}": {len(numeros)}')

    # Verificação cruzada: o que os termos encontram fora da unidade temática
    dentro = {i["codigo"] for i in numeros}
    fora = {}
    for termo in TERMOS:
        for ano in ANOS:
            for item in buscar_termo(termo, ano):
                cod = item["codigo"]
                if cod not in dentro:
                    fora.setdefault(cod, {
                        "codigo": cod,
                        "unidade_tematica": unidade_de(item),
                        "texto": item["texto"],
                        "termos": [],
                    })["termos"].append(termo)

    (DESTINO / "fora-do-recorte.json").write_text(
        json.dumps(sorted(fora.values(), key=lambda x: x["codigo"]),
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\nfora do recorte, encontradas por termo: {len(fora)}")
    for v in sorted(fora.values(), key=lambda x: x["codigo"]):
        print(f'  {v["codigo"]} [{v["unidade_tematica"]}] via {v["termos"]}')


if __name__ == "__main__":
    main()
