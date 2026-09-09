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
