# Design: Sistema de Módulos de Estatísticas

## Objetivo

Implementar um sistema modular que gere uma seção no relatório para cada teoria/método descrito em `docs/estatisticas.md`, facilitando adicionar, alterar e remover módulos com mínimo esforço.

## Escopo

10 teorias/métodos:
1. Hipergeometria
2. Estatística Bayesiana
3. Teoria de Galois e Teoria dos Grupos
4. Otimização Combinatória
5. Análise Estatística de Séries Temporais
6. Teoria da Entropia (Shannon)
7. Teoria de Números e Distribuição de Primos
8. Modelos de Probabilidade Não-uniforme
9. Machine Learning
10. Teoria dos Conjuntos e Design de Experimentos

## Arquitetura

### Estrutura de Diretórios

```
ltfac/
├── pyproject.toml
├── .local/
│   ├── resources/
│   ├── output/
│   └── docs/
│       └── estatisticas.md
└── src/
    ├── __init__.py
    ├── __main__.py
    ├── loader.py
    ├── stats.py
    ├── report.py
    └── modulos/
        ├── __init__.py        # Registry e auto-descoberta
        ├── base.py            # ABC do protocolo
        ├── hipergeometria.py
        ├── bayes.py
        ├── galois.py
        ├── otimizacao.py
        ├── series_temporais.py
        ├── entropia.py
        ├── primos.py
        ├── probabilidade.py
        ├── machine_learning.py
        └── conjuntos.py
```

### Protocolo ABC

**`modulos/base.py`:**

```python
from abc import ABC, abstractmethod
from pathlib import Path

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
    def compute(self, draws: list[Draw]) -> str:
        """Retorna seção Markdown formatada."""
        ...
```

### Registry Auto-descobridor

**`modulos/__init__.py`:**

```python
import importlib
import pkgutil
from pathlib import Path

_registry: list[type[ModuloEstatistica]] = []

def registrar(cls):
    """Decorator: adiciona classe ao registry."""
    _registry.append(cls)
    return cls

def get_modulos() -> list[ModuloEstatistica]:
    """Instancia todos os módulos registrados."""
    package_dir = Path(__file__).parent
    for _, module_name, _ in pkgutil.iter_modules([str(package_dir)]):
        if module_name not in ('base', '__init__'):
            importlib.import_module(f".{module_name}", package=__name__)
    
    return [cls() for cls in _registry]
```

### Exemplo de Módulo

**`modulos/hipergeometria.py`:**

```python
from math import comb
from collections import Counter
from .base import ModuloEstatistica
from . import registrar

@registrar
class Hipergeometria(ModuloEstatistica):
    """Probabilidade de acerto parcial (hipergeometria)."""
    
    nome = "Hipergeometria"
    descricao = "Probabilidade teórica de acertar k de 15 bolas"
    
    def compute(self, draws: list) -> str:
        N, K, n = 25, 15, 15
        
        linhas = ["| Acertos | P(teórica) | P(acumulada) |", "|---:|---:|---:|"]
        prob_acum = 0
        for k in range(10, 16):
            p = comb(K, k) * comb(N-K, n-k) / comb(N, n)
            prob_acum += p
            linhas.append(f"| {k}/15 | {p:.6f} | {prob_acum:.6f} |")
        
        return f"## Hipergeometria\n\nProbabilidade teórica de acerto:\n\n" + "\n".join(linhas)
```

### Integração com o Relatório

**`report.py` atualizado:**

```python
def build_report(draws: list[Draw]) -> str:
    lines = []
    
    # Resumo geral (mantido)
    lines.append("# Estatísticas Lotofácil — 12 meses")
    lines.append(f"- Total: {len(draws)} concursos")
    # ...
    
    # Módulos do registry
    from .modulos import get_modulos
    for modulo in get_modulos():
        lines.append(modulo.compute(draws))
    
    # Dia da semana (mantido)
    # ...
    
    return "\n".join(lines)
```

## Estrutura do Relatório

```markdown
# Estatísticas Lotofácil — 12 meses

- Total de concursos: 293
- Primeiro/Último concurso: ...

## Hipergeometria
... (do módulo)

## Análise Bayesiana
... (do módulo)

## ...demais módulos...

## Estatísticas por Dia da Semana
... (mantido do código atual)
```

## Fluxo de Trabalho

1. **Adicionar módulo:** Criar `modulos/novo_modulo.py` com `@registrar`
2. **Remover módulo:** Deletar o arquivo
3. **Alterar módulo:** Editar o arquivo específico
4. **Executar:** `python3 -m src` (auto-descobre e gera relatório)

## Decisões de Design

| Aspecto | Decisão |
|---------|---------|
| Estrutura | Um arquivo por teoria em `modulos/` |
| Interface | ABC `ModuloEstatistica` |
| Registro | Auto-descoberta via `@registrar` |
| Integração | Registry itera e concatena no relatório |
| Manutenção | Criar/deletar arquivo = adicionar/remover |

## Validação

- [ ] Criar diretório `modulos/`
- [ ] Implementar `base.py` com ABC
- [ ] Implementar `__init__.py` com registry
- [ ] Implementar 10 módulos
- [ ] Atualizar `report.py`
- [ ] Testar geração do relatório
