# ltfac

Programa Python de linha de comando que lê um arquivo CSV com resultados da
Lotofácil e gera um relatório em Markdown com estatísticas sobre os concursos.

## Requisitos

- Python 3.10 ou superior
- Apenas biblioteca padrão (nenhuma dependência externa)

## Estrutura

```
src/
├── __init__.py    # caminhos padrão (entrada/saída)
├── __main__.py    # CLI (argparse) e orquestração
├── loader.py      # leitura do CSV -> lista de Draw
├── stats.py       # cálculo de frequências (números e combinações)
└── report.py      # renderização do relatório em Markdown
```

## Funcionamento

1. **Leitura do CSV** (`loader.py`)
   - Lê o arquivo delimitado por `;` com cabeçalho
     `Concurso;Data Sorteio;Bola1;...;Bola15`.
   - O encoding usado é `utf-8-sig` para descartar o BOM, se presente.
   - Retorna uma lista de `Draw(concurso, data, bolas)`, com `bolas` ordenadas
     em ordem crescente.

2. **Cálculo de estatísticas** (`stats.py`)
   - `number_frequency`: conta quantas vezes cada número (1 a 25) foi sorteado.
   - `combination_frequency(size)`: conta as combinações de `size` números
     (5 ou 7) usando `itertools.combinations`.
   - `draws_ending_in_zero`: filtra concursos cujo número termina em 0
     (múltiplos de 10).
   - `group_by_weekday`: agrupa os concursos pelo dia da semana em português.

3. **Geração do relatório** (`report.py`)
   - Monta o Markdown em memória e grava em disco.
   - As tabelas de "Os 12 números mais sorteados" selecionam o top 12 por
     frequência e os exibem em **ordem numérica crescente**.
   - As tabelas de combinações (de 5 e de 7 números) são ordenadas por
     frequência decrescente; os números dentro de cada combinação aparecem
     em ordem crescente.

4. **Orquestração** (`__main__.py`)
   - Faz o parse dos argumentos, chama o loader, o builder de relatório e o
     writer, e imprime o caminho do arquivo gerado.

## Entrada esperada

CSV delimitado por `;` com as colunas:

```
Concurso;Data Sorteio;Bola1;Bola2;...;Bola15
```

- `Concurso`: inteiro
- `Data Sorteio`: `DD/MM/AAAA`
- `Bola1`..`Bola15`: inteiros de 1 a 25

Local padrão: `../.local/resources/Lotofacil_12_months.csv`
(relativo a esta pasta `src/`).

## Saída

Arquivo Markdown gerado em `../.local/output/estatisticas_lotofacil.md`
contendo:

- Cabeçalho com total de concursos e intervalo de datas
- Os 12 números mais sorteados (ordem crescente)
- As combinações de 5 números mais sorteadas
- As combinações de 7 números mais sorteadas
- Estatísticas equivalentes para concursos terminados em 0 (múltiplos de 10)
- Estatísticas equivalentes agrupadas por dia da semana

## Como executar

A partir da pasta **`ltfac/`** (pai de `src/`):

```bash
python3 -m src
```

Usando caminhos personalizados:

```bash
python3 -m src --input /caminho/do/arquivo.csv --output-dir /caminho/de/saida
```

Opções da CLI:

| Opção          | Descrição                                  | Padrão                                              |
|----------------|--------------------------------------------|-----------------------------------------------------|
| `--input`      | Caminho do CSV de entrada                  | `../.local/resources/Lotofacil_12_months.csv`       |
| `--output-dir` | Diretório onde o Markdown será gravado     | `../.local/output`                                  |

Exemplo de saída no terminal:

```
Relatório salvo em: /home/usuario/ltfac/.local/output/estatisticas_lotofacil.md
```

## Código de retorno

- `0`: execução bem-sucedida
- `1`: arquivo de entrada não encontrado ou CSV vazio
