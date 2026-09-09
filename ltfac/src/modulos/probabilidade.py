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
