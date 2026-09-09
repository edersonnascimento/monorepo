from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..loader import Draw


class ModuloEstatistica(ABC):
    """Interface base para módulos de estatística."""

    @property
    @abstractmethod
    def nome(self) -> str:
        """Nome da seção no relatório."""
        ...

    @property
    @abstractmethod
    def descricao(self) -> str:
        """Descrição curta da teoria/método."""
        ...

    @abstractmethod
    def compute(self, draws: list["Draw"]) -> str:
        """Retorna seção Markdown formatada."""
        ...
