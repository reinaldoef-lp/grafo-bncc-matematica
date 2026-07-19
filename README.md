# Grafo BNCC — Matemática

Camada de pré-requisitos, progressão e erros característicos
sobre as habilidades da BNCC de Matemática.

## O que é

A BNCC define habilidades, mas **não define progressão formal
entre elas**. Este projeto acrescenta a camada que falta:

- **Componentes finos** — as sub-habilidades sob cada habilidade
- **Pré-requisitos** — qual habilidade precisa vir antes
- **Progressão típica** — a ordem em que se aprende
- **Erros característicos** — o que o aluno erra e por quê

## O que NÃO é

Não é uma extração da BNCC. Essa camada já existe e é livre:
o [bncc.dev](https://bncc.dev) faz isso, e este projeto a consome.

## Escopo atual

Cadeia de números racionais fracionários, 6º ao 9º ano.

## Método

Toda afirmação carrega um campo `evidencia`
(`pratica_docente` · `literatura` · `saeb` · `inferido`).
O critério de cada tipo de aresta está em [METODOLOGIA.md](METODOLOGIA.md).

### Regra de extração — verificação cruzada obrigatória

Vale para esta e para todas as fases seguintes (razão, proporção,
porcentagem e o que vier depois).

O recorte de habilidades é feito **pela unidade temática**, nunca por
busca textual. A busca da API é literal: não normaliza plural nem
flexão, de modo que `fração` e `frações` devolvem conjuntos diferentes
e quase disjuntos. Confiar em um termo perde parte da cadeia em
silêncio — e silêncio é o pior modo de errar aqui.

Toda extração roda em seguida uma **verificação cruzada** por múltiplos
termos e reporta o que aparece **fora** da unidade temática recortada,
em `dados/bruto/fora-do-recorte.json`. Cada item dessa lista é
inspecionado à mão antes de entrar ou ficar de fora do grafo, e a
decisão é registrada.

Nenhum recorte é aceito sem essa conferência.

## Autoria

Reinaldo Elias — professor, Pará, Brasil.
Trabalho independente, desenvolvido com recursos próprios.

## Como citar

ELIAS, Reinaldo. Grafo BNCC — Matemática. 2026.
Disponível em: <URL>

## Licença

- **Dados** (`dados/`, `esquema/`): CC BY-SA 4.0
- **Código** (`scripts/`): AGPL-3.0

O código é AGPL para que quem oferecer este motor como serviço
seja obrigado a abrir as próprias modificações. Os dados são
share-alike pela mesma razão.
