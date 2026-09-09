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
