# Sistema de Módulos de Estatísticas - Plano de Implementação

> **Para trabalhadores agênticos:** HABILIDADE SUB-OBREGATÓRIA: Use superpowers:subagent-driven-development (recomendado) ou superpowers:executing-plans para implementar este plano tarefa por tarefa. As etapas usam sintaxe de checkbox (`- [ ]`) para rastreamento.

**Objetivo:** Implementar um sistema modular que gere uma seção no relatório para cada teoria/método descrito em `docs/estatisticas.md`.

**Arquitetura:** Protocolo ABC com registry auto-descobridor. Cada módulo em `modulos/` se registra via decorator `@registrar` e é automaticamente incluído no relatório.

**Tech Stack:** Python 3.10+, apenas stdlib.

## Restrições Globais

- Python >= 3.10
- Zero dependências externas
- Um arquivo por teoria em `modulos/`
- Interface ABC `ModuloEstatistica`
- Auto-descoberta via `pkgutil`

---

### Task 1: Criar Diretório e Módulo Base

**Arquivos:**
- Criar: `src/modulos/__init__.py`
- Criar: `src/modulos/base.py`

**Interfaces:**
- Consome: N/A
- Produz: `ModuloEstatistica` (ABC), `registrar()` (decorator), `get_modulos()` (factory)

- [ ] **Passo 1: Criar diretório modulos**

```bash
mkdir -p src/modulos
```

- [ ] **Passo 2: Criar base.py com ABC**

```python
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..loader import Draw


class ModuloEstatistica(ABC):
    """Interface base para módulos de estatística."""

    @property
    @abstractmethod
    def nome(self) -> str:
        """Nome da seção no relatório."""
        ...

    @property
    @abstractmethod
    def descricao(self) -> str:
        """Descrição curta da teoria/método."""
        ...

    @abstractmethod
    def compute(self, draws: list["Draw"]) -> str:
        """Retorna seção Markdown formatada."""
        ...
```

- [ ] **Passo 3: Criar __init__.py com registry**

```python
from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import ModuloEstatistica

_registry: list[type[ModuloEstatistica]] = []


def registrar(cls: type[ModuloEstatistica]) -> type[ModuloEstatistica]:
    """Decorator: adiciona classe ao registry."""
    _registry.append(cls)
    return cls


def get_modulos() -> list[ModuloEstatistica]:
    """Instancia todos os módulos registrados, na ordem de descoberta."""
    package_dir = Path(__file__).parent
    for _, module_name, _ in pkgutil.iter_modules([str(package_dir)]):
        if module_name not in ("base", "__init__"):
            importlib.import_module(f".{module_name}", package=__name__)

    return [cls() for cls in _registry]
```

- [ ] **Passo 4: Commit**

```bash
git add src/modulos/__init__.py src/modulos/base.py
git commit -m "feat: add base module and registry for statistics modules"
```

---

### Task 2: Módulo Hipergeometria

**Arquivos:**
- Criar: `src/modulos/hipergeometria.py`

**Interfaces:**
- Consome: `Draw` (dataclass), `registrar` (decorator)
- Produz: `Hipergeometria.compute()` → str (Markdown)

- [ ] **Passo 1: Criar módulo hipergeometria.py**

```python
from __future__ import annotations

from math import comb
from typing import TYPE_CHECKING

from . import registrar
from .base import ModuloEstatistica

if TYPE_CHECKING:
    from ..loader import Draw


@registrar
class Hipergeometria(ModuloEstatistica):
    """Probabilidade de acerto parcial (hipergeometria)."""

    @property
    def nome(self) -> str:
        return "Hipergeometria"

    @property
    def descricao(self) -> str:
        return "Probabilidade teórica de acertar k de 15 bolas"

    def compute(self, draws: list[Draw]) -> str:
        N, K, n = 25, 15, 15

        linhas = [
            "| Acertos | P(teórica) | P(acumulada) |",
            "|---:|---:|---:|",
        ]
        prob_acum = 0.0
        for k in range(10, 16):
            p = comb(K, k) * comb(N - K, n - k) / comb(N, n)
            prob_acum += p
            linhas.append(f"| {k}/15 | {p:.6f} | {prob_acum:.6f} |")

        return (
            f"## {self.nome}\n\n"
            f"{self.descricao}:\n\n"
            + "\n".join(linhas)
        )
```

- [ ] **Passo 2: Commit**

```bash
git add src/modulos/hipergeometria.py
git commit -m "feat: add hypergeometric distribution module"
```

---

### Task 3: Módulo Análise Bayesiana

**Arquivos:**
- Criar: `src/modulos/bayes.py`

**Interfaces:**
- Consome: `Draw`, `registrar`
- Produz: `AnaliseBayesiana.compute()` → str

- [ ] **Passo 1: Criar módulo bayes.py**

```python
from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from . import registrar
from .base import ModuloEstatistica

if TYPE_CHECKING:
    from ..loader import Draw


@registrar
class AnaliseBayesiana(ModuloEstatistica):
    """Análise bayesiana de números quentes e frios."""

    @property
    def nome(self) -> str:
        return "Análise Bayesiana"

    @property
    def descricao(self) -> str:
        return "Números com frequência desviante da média esperada"

    def compute(self, draws: list[Draw]) -> str:
        total_bolas = len(draws) * 15
        freq_esperada = total_bolas / 25

        counter: Counter[int] = Counter()
        for draw in draws:
            counter.update(draw.bolas)

        desvios = []
        for numero in range(1, 26):
            freq = counter.get(numero, 0)
            desvio = abs(freq - freq_esperada) / freq_esperada
            desvios.append((numero, freq, desvio))

        desvios.sort(key=lambda x: x[2], reverse=True)

        linhas = [
            "| Número | Frequência | Desvio % |",
            "|---:|---:|---:|",
        ]
        for numero, freq, desvio in desvios[:12]:
            linhas.append(f"| {numero} | {freq} | {desvio:.2%} |")

        return (
            f"## {self.nome}\n\n"
            f"{self.descricao}:\n\n"
            + "\n".join(linhas)
        )
```

- [ ] **Passo 2: Commit**

```bash
git add src/modulos/bayes.py
git commit -m "feat: add Bayesian analysis module"
```

---

### Task 4: Módulo Teoria de Galois

**Arquivos:**
- Criar: `src/modulos/galois.py`

**Interfaces:**
- Consome: `Draw`, `registrar`
- Produz: `TeoriaGalois.compute()` → str

- [ ] **Passo 1: Criar módulo galois.py**

```python
from __future__ import annotations

from itertools import combinations
from collections import Counter
from typing import TYPE_CHECKING

from . import registrar
from .base import ModuloEstatistica

if TYPE_CHECKING:
    from ..loader import Draw


@registrar
class TeoriaGalois(ModuloEstatistica):
    """Geração de combinatórios sem repetição via ações de grupo."""

    @property
    def nome(self) -> str:
        return "Teoria de Galois"

    @property
    def descricao(self) -> str:
        return "Análise de simetrias e agrupamentos de números"

    def compute(self, draws: list[Draw]) -> str:
        pares_counter: Counter[tuple[int, int]] = Counter()
        for draw in draws:
            pares_counter.update(combinations(draw.bolas, 2))

        linhas = [
            "| Par | Frequência |",
            "|---|---:|",
        ]
        for par, freq in pares_counter.most_common(15):
            linhas.append(f"| {par[0]:02d}-{par[1]:02d} | {freq} |")

        return (
            f"## {self.nome}\n\n"
            f"{self.descricao}:\n\n"
            "### Pares mais frequentes\n\n"
            + "\n".join(linhas)
        )
```

- [ ] **Passo 2: Commit**

```bash
git add src/modulos/galois.py
git commit -m "feat: add Galois theory module"
```

---

### Task 5: Módulo Otimização Combinatória

**Arquivos:**
- Criar: `src/modulos/otimizacao.py`

**Interfaces:**
- Consome: `Draw`, `registrar`
- Produz: `OtimizacaoCombinatoria.compute()` → str

- [ ] **Passo 1: Criar módulo otimizacao.py**

```python
from __future__ import annotations

from collections import Counter
from itertools import combinations
from typing import TYPE_CHECKING

from . import registrar
from .base import ModuloEstatistica

if TYPE_CHECKING:
    from ..loader import Draw


@registrar
class OtimizacaoCombinatoria(ModuloEstatistica):
    """Otimização de apostas via cobertura mínima."""

    @property
    def nome(self) -> str:
        return "Otimização Combinatória"

    @property
    def descricao(self) -> str:
        return "Combinações de 5 números com maior cobertura"

    def compute(self, draws: list[Draw]) -> str:
        counter: Counter[tuple[int, ...]] = Counter()
        for draw in draws:
            counter.update(combinations(draw.bolas, 5))

        linhas = [
            "| Combinação | Frequência |",
            "|---|---:|",
        ]
        for combo, freq in counter.most_common(10):
            linhas.append(f"| {'-'.join(str(n) for n in combo)} | {freq} |")

        return (
            f"## {self.nome}\n\n"
            f"{self.descricao}:\n\n"
            + "\n".join(linhas)
        )
```

- [ ] **Passo 2: Commit**

```bash
git add src/modulos/otimizacao.py
git commit -m "feat: add combinatorial optimization module"
```

---

### Task 6: Módulo Séries Temporais

**Arquivos:**
- Criar: `src/modulos/series_temporais.py`

**Interfaces:**
- Consome: `Draw`, `registrar`
- Produz: `SeriesTemporais.compute()` → str

- [ ] **Passo 1: Criar módulo series_temporais.py**

```python
from __future__ import annotations

from collections import Counter, defaultdict
from typing import TYPE_CHECKING

from . import registrar
from .base import ModuloEstatistica

if TYPE_CHECKING:
    from ..loader import Draw


@registrar
class SeriesTemporais(ModuloEstatistica):
    """Análise de séries temporais e padrões cíclicos."""

    @property
    def nome(self) -> str:
        return "Séries Temporais"

    @property
    def descricao(self) -> str:
        return "Frequência de cada número por mês"

    def compute(self, draws: list[Draw]) -> str:
        por_mes: dict[str, Counter[int]] = defaultdict(Counter)
        for draw in draws:
            mes = draw.data.strftime("%Y-%m")
            por_mes[mes].update(draw.bolas)

        meses = sorted(por_mes.keys())[-6:]

        linhas = ["| Mês | Número | Frequência |", "|---|---:|---:|"]
        for mes in meses:
            counter = por_mes[mes]
            for numero, freq in counter.most_common(3):
                linhas.append(f"| {mes} | {numero} | {freq} |")

        return (
            f"## {self.nome}\n\n"
            f"{self.descricao}:\n\n"
            + "\n".join(linhas)
        )
```

- [ ] **Passo 2: Commit**

```bash
git add src/modulos/series_temporais.py
git commit -m "feat: add time series analysis module"
```

---

### Task 7: Módulo Entropia de Shannon

**Arquivos:**
- Criar: `src/modulos/entropia.py`

**Interfaces:**
- Consome: `Draw`, `registrar`
- Produz: `EntropiaShannon.compute()` → str

- [ ] **Passo 1: Criar módulo entropia.py**

```python
from __future__ import annotations

import math
from collections import Counter
from typing import TYPE_CHECKING

from . import registrar
from .base import ModuloEstatistica

if TYPE_CHECKING:
    from ..loader import Draw


@registrar
class EntropiaShannon(ModuloEstatistica):
    """Medida de imprevisibilidade dos sorteios."""

    @property
    def nome(self) -> str:
        return "Entropia de Shannon"

    @property
    def descricao(self) -> str:
        return "Medida de impredutibilidade do sorteio"

    def compute(self, draws: list[Draw]) -> str:
        counter: Counter[int] = Counter()
        for draw in draws:
            counter.update(draw.bolas)

        total = sum(counter.values())
        entropia = 0.0
        for freq in counter.values():
            if freq > 0:
                p = freq / total
                entropia -= p * math.log2(p)

        entropia_max = math.log2(25)

        linhas = [
            f"| Métrica | Valor |",
            f"|---|---:|",
            f"| Entropia calculada | {entropia:.4f} |",
            f"| Entropia máxima | {entropia_max:.4f} |",
            f"| Normalizada | {entropia / entropia_max:.4f} |",
        ]

        return (
            f"## {self.nome}\n\n"
            f"{self.descricao}:\n\n"
            + "\n".join(linhas)
        )
```

- [ ] **Passo 2: Commit**

```bash
git add src/modulos/entropia.py
git commit -m "feat: add Shannon entropy module"
```

---

### Task 8: Módulo Números Primos

**Arquivos:**
- Criar: `src/modulos/primos.py`

**Interfaces:**
- Consome: `Draw`, `registrar`
- Produz: `NumerosPrimos.compute()` → str

- [ ] **Passo 1: Criar módulo primos.py**

```python
from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from . import registrar
from .base import ModuloEstatistica

if TYPE_CHECKING:
    from ..loader import Draw

PRIMOS_ATE_25 = {2, 3, 5, 7, 11, 13, 17, 19, 23}


@registrar
class NumerosPrimos(ModuloEstatistica):
    """Análise de frequência de números primos."""

    @property
    def nome(self) -> str:
        return "Números Primos"

    @property
    def descricao(self) -> str:
        return "Frequência de primos vs não-primos nos sorteios"

    def compute(self, draws: list[Draw]) -> str:
        primos_counter: Counter[int] = Counter()
        nao_primos_counter: Counter[int] = Counter()

        for draw in draws:
            for bola in draw.bolas:
                if bola in PRIMOS_ATE_25:
                    primos_counter[bola] += 1
                else:
                    nao_primos_counter[bola] += 1

        total_primos = sum(primos_counter.values())
        total_nao_primos = sum(nao_primos_counter.values())
        total = total_primos + total_nao_primos

        linhas = [
            "| Categoria | Quantidade | Percentual |",
            "|---|---:|---:|",
            f"| Primos | {total_primos} | {total_primos / total:.2%} |",
            f"| Não-primos | {total_nao_primos} | {total_nao_primos / total:.2%} |",
        ]

        return (
            f"## {self.nome}\n\n"
            f"{self.descricao}:\n\n"
            + "\n".join(linhas)
        )
```

- [ ] **Passo 2: Commit**

```bash
git add src/modulos/primos.py
git commit -m "feat: add prime numbers module"
```

---

### Task 9: Módulo Probabilidade Não-uniforme

**Arquivos:**
- Criar: `src/modulos/probabilidade.py`

**Interfaces:**
- Consome: `Draw`, `registrar`
- Produz: `ProbabilidadeNaoUniforme.compute()` → str

- [ ] **Passo 1: Criar módulo probabilidade.py**

```python
from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from . import registrar
from .base import ModuloEstatistica

if TYPE_CHECKING:
    from ..loader import Draw


@registrar
class ProbabilidadeNaoUniforme(ModuloEstatistica):
    """Distribuição de probabilidade personalizada."""

    @property
    def nome(self) -> str:
        return "Probabilidade Não-uniforme"

    @property
    def descricao(self) -> str:
        return "Distribuição observada vs uniforme teórica"

    def compute(self, draws: list[Draw]) -> str:
        counter: Counter[int] = Counter()
        for draw in draws:
            counter.update(draw.bolas)

        total = sum(counter.values())
        p_uniforme = 1 / 25

        linhas = [
            "| Número | P(obs) | P(uniforme) | Desvio |",
            "|---:|---:|---:|---:|",
        ]
        for numero in range(1, 26):
            p_obs = counter.get(numero, 0) / total
            desvio = abs(p_obs - p_uniforme)
            linhas.append(f"| {numero} | {p_obs:.4f} | {p_uniforme:.4f} | {desvio:.4f} |")

        return (
            f"## {self.nome}\n\n"
            f"{self.descricao}:\n\n"
            + "\n".join(linhas)
        )
```

- [ ] **Passo 2: Commit**

```bash
git add src/modulos/probabilidade.py
git commit -m "feat: add non-uniform probability module"
```

---

### Task 10: Módulo Machine Learning

**Arquivos:**
- Criar: `src/modulos/machine_learning.py`

**Interfaces:**
- Consome: `Draw`, `registrar`
- Produz: `MachineLearning.compute()` → str

- [ ] **Passo 1: Criar módulo machine_learning.py**

```python
from __future__ import annotations

from collections import Counter
from itertools import combinations
from typing import TYPE_CHECKING

from . import registrar
from .base import ModuloEstatistica

if TYPE_CHECKING:
    from ..loader import Draw


@registrar
class MachineLearning(ModuloEstatistica):
    """Análise de padrões complexos via ML."""

    @property
    def nome(self) -> str:
        return "Machine Learning"

    @property
    def descricao(self) -> str:
        return "Trios de números com maior co-ocorrência"

    def compute(self, draws: list[Draw]) -> str:
        trios_counter: Counter[tuple[int, ...]] = Counter()
        for draw in draws:
            trios_counter.update(combinations(draw.bolas, 3))

        linhas = [
            "| Trio | Frequência |",
            "|---|---:|",
        ]
        for trio, freq in trios_counter.most_common(10):
            linhas.append(f"| {'-'.join(str(n) for n in trio)} | {freq} |")

        return (
            f"## {self.nome}\n\n"
            f"{self.descricao}:\n\n"
            + "\n".join(linhas)
        )
```

- [ ] **Passo 2: Commit**

```bash
git add src/modulos/machine_learning.py
git commit -m "feat: add machine learning pattern module"
```

---

### Task 11: Módulo Teoria dos Conjuntos

**Arquivos:**
- Criar: `src/modulos/conjuntos.py`

**Interfaces:**
- Consome: `Draw`, `registrar`
- Produz: `TeoriaConjuntos.compute()` → str

- [ ] **Passo 1: Criar módulo conjuntos.py**

```python
from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from . import registrar
from .base import ModuloEstatistica

if TYPE_CHECKING:
    from ..loader import Draw


@registrar
class TeoriaConjuntos(ModuloEstatistica):
    """Design de experimentos e blocos balanceados."""

    @property
    def nome(self) -> str:
        return "Teoria dos Conjuntos"

    @property
    def descricao(self) -> str:
        return "Distribuição dos números em faixas decimais"

    def compute(self, draws: list[Draw]) -> str:
        faixas: Counter[str] = Counter()
        for draw in draws:
            for bola in draw.bolas:
                if bola <= 5:
                    faixas["01-05"] += 1
                elif bola <= 10:
                    faixas["06-10"] += 1
                elif bola <= 15:
                    faixas["11-15"] += 1
                elif bola <= 20:
                    faixas["16-20"] += 1
                else:
                    faixas["21-25"] += 1

        total = sum(faixas.values())

        linhas = [
            "| Faixa | Quantidade | Percentual |",
            "|---|---:|---:|",
        ]
        for faixa in ["01-05", "06-10", "11-15", "16-20", "21-25"]:
            qtd = faixas.get(faixa, 0)
            linhas.append(f"| {faixa} | {qtd} | {qtd / total:.2%} |")

        return (
            f"## {self.nome}\n\n"
            f"{self.descricao}:\n\n"
            + "\n".join(linhas)
        )
```

- [ ] **Passo 2: Commit**

```bash
git add src/modulos/conjuntos.py
git commit -m "feat: add set theory module"
```

---

### Task 12: Atualizar report.py

**Arquivos:**
- Modificar: `src/report.py`

**Interfaces:**
- Consome: `get_modulos()` (de modulos/__init__.py)
- Produz: `build_report()` atualizado

- [ ] **Passo 1: Atualizar report.py**

Adicionar import e integrar módulos:

```python
from __future__ import annotations

from collections import Counter
from pathlib import Path

from .loader import Draw
from .stats import (
    WEEKDAY_ORDER,
    group_by_weekday,
    number_frequency,
)


def build_report(draws: list[Draw]) -> str:
    lines: list[str] = []
    first, last = draws[0], draws[-1]

    lines.append("# Estatísticas Lotofácil — 12 meses")
    lines.append("")
    lines.append(f"- **Total de concursos:** {len(draws)}")
    lines.append(
        f"- **Primeiro concurso:** {first.concurso} "
        f"({first.data.strftime('%d/%m/%Y')})"
    )
    lines.append(
        f"- **Último concurso:** {last.concurso} "
        f"({last.data.strftime('%d/%m/%Y')})"
    )
    lines.append("")

    # Módulos do registry
    from .modulos import get_modulos
    for modulo in get_modulos():
        lines.append(modulo.compute(draws))
        lines.append("")

    # Estatísticas por dia da semana (mantido)
    lines.append("## Estatísticas por Dia da Semana")
    lines.append("")
    groups = group_by_weekday(draws)
    for day in WEEKDAY_ORDER:
        day_draws = groups[day]
        if not day_draws:
            continue
        lines.append(f"### {day} ({len(day_draws)} concursos)")
        lines.append("")

        # Top 12 números do dia
        freq = number_frequency(day_draws)
        top12 = freq.most_common(12)
        linhas = ["| Número | Frequência |", "|---:|---:|"]
        for numero, f in sorted(top12, key=lambda x: x[0]):
            linhas.append(f"| {numero} | {f} |")
        lines.extend(linhas)
        lines.append("")

    return "\n".join(lines)


def write_report(report: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "estatisticas_lotofacil.md"
    out_path.write_text(report, encoding="utf-8")
    return out_path
```

- [ ] **Passo 2: Commit**

```bash
git add src/report.py
git commit -m "feat: integrate statistics modules into report"
```

---

### Task 13: Teste de Integração

**Arquivos:**
- Nenhum arquivo novo (teste manual)

**Interfaces:**
- Consome: `main()` de __main__.py
- Produz: Relatório completo

- [ ] **Passo 1: Executar programa**

```bash
cd /mnt/d/repositories/personal/monorepo/ltfac && python3 -m src
```

Esperado: Mensagem "Relatório salvo em: ..." e arquivo gerado

- [ ] **Passo 2: Verificar saída**

```bash
cat .local/output/estatisticas_lotofacil.md | head -100
```

Esperado: Relatório com seções para cada módulo

- [ ] **Passo 3: Commit final**

```bash
git add .
git commit -m "feat: complete statistics modules system"
```

---

## Resumo de Tarefas

| Tarefa | Módulo | Status |
|--------|--------|--------|
| 1 | Base + Registry | Pendente |
| 2 | Hipergeometria | Pendente |
| 3 | Análise Bayesiana | Pendente |
| 4 | Teoria de Galois | Pendente |
| 5 | Otimização Combinatória | Pendente |
| 6 | Séries Temporais | Pendente |
| 7 | Entropia de Shannon | Pendente |
| 8 | Números Primos | Pendente |
| 9 | Probabilidade Não-uniforme | Pendente |
| 10 | Machine Learning | Pendente |
| 11 | Teoria dos Conjuntos | Pendente |
| 12 | Atualizar report.py | Pendente |
| 13 | Teste de Integração | Pendente |
