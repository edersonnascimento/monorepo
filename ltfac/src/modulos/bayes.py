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
