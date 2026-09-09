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
