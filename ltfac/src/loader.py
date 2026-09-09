from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

BOLA_COLUMNS = [f"Bola{i}" for i in range(1, 16)]


@dataclass(frozen=True)
class Draw:
    concurso: int
    data: date
    bolas: tuple[int, ...]


def load_draws(path: Path) -> list[Draw]:
    draws: list[Draw] = []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh, delimiter=";")
        for row in reader:
            concurso = int(row["Concurso"])
            data = datetime.strptime(row["Data Sorteio"], "%d/%m/%Y").date()
            bolas = tuple(sorted(int(row[col]) for col in BOLA_COLUMNS))
            draws.append(Draw(concurso=concurso, data=data, bolas=bolas))
    return draws
