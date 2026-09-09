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
