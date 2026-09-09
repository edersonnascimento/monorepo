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