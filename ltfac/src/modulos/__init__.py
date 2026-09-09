from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import ModuloEstatistica

_registry: list[type[ModuloEstatistica]] = []


def registrar(cls: type[ModuloEstatistica]) -> type[ModuloEstatistica]:
    """Decorator: adiciona classe ao registry."""
    _registry.append(cls)
    return cls


def get_modulos() -> list[ModuloEstatistica]:
    """Instancia todos os módulos registrados, na ordem de descoberta."""
    package_dir = Path(__file__).parent
    for _, module_name, _ in pkgutil.iter_modules([str(package_dir)]):
        if module_name not in ("base", "__init__"):
            importlib.import_module(f".{module_name}", package=__name__)

    return [cls() for cls in _registry]
