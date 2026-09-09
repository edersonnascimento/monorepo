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
