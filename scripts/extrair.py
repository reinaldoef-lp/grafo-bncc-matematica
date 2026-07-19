#!/usr/bin/env python3
"""Extrai da API do bncc.dev as habilidades de Matemática do 6º ao 9º ano.

Salva dois arquivos em dados/bruto/:

  ma-ef-6-9.json    todas as habilidades de Matemática, 6º ao 9º ano
  numeros-6-9.json  recorte da unidade temática "Números"

A resposta da API é gravada sem alteração. A cadeia de números racionais
fracionários vive dentro de "Números"; a busca textual por "fração"
devolve apenas 3 habilidades e perde o resto da cadeia.

Uso: python3 scripts/extrair.py
"""

import json
import urllib.request
from pathlib import Path

API = "https://api.bncc.dev/v1/habilidades"
ANOS = [6, 7, 8, 9]
UNIDADE = "Números"
DESTINO = Path(__file__).resolve().parent.parent / "dados" / "bruto"


def buscar(ano):
    url = f"{API}?etapa=EF&componente=MA&ano={ano}&limite=100"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


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


if __name__ == "__main__":
    main()
