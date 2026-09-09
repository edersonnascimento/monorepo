from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from . import registrar
from .base import ModuloEstatistica

if TYPE_CHECKING:
    from ..loader import Draw


@registrar
class TeoriaConjuntos(ModuloEstatistica):
    """Design de experimentos e blocos balanceados."""

    @property
    def nome(self) -> str:
        return "Teoria dos Conjuntos"

    @property
    def descricao(self) -> str:
        return "Distribuição dos números em faixas decimais"

    def compute(self, draws: list[Draw]) -> str:
        faixas: Counter[str] = Counter()
        for draw in draws:
            for bola in draw.bolas:
                if bola <= 5:
                    faixas["01-05"] += 1
                elif bola <= 10:
                    faixas["06-10"] += 1
                elif bola <= 15:
                    faixas["11-15"] += 1
                elif bola <= 20:
                    faixas["16-20"] += 1
                else:
                    faixas["21-25"] += 1

        total = sum(faixas.values())

        linhas = [
            "| Faixa | Quantidade | Percentual |",
            "|---|---:|---:|",
        ]
        for faixa in ["01-05", "06-10", "11-15", "16-20", "21-25"]:
            qtd = faixas.get(faixa, 0)
            linhas.append(f"| {faixa} | {qtd} | {qtd / total:.2%} |")

        return (
            f"## {self.nome}\n\n"
            f"{self.descricao}:\n\n"
            + "\n".join(linhas)
        )
