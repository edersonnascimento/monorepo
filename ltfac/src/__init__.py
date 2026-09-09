from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESOURCES_DIR = PROJECT_ROOT / ".local" / "resources"
DEFAULT_INPUT = RESOURCES_DIR / "Lotofacil_12_months.csv"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / ".local" / "output"

__all__ = ["PROJECT_ROOT", "RESOURCES_DIR", "DEFAULT_INPUT", "DEFAULT_OUTPUT_DIR"]
