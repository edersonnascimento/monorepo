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
