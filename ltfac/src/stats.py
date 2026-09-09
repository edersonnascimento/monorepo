from __future__ import annotations

from collections import Counter
from itertools import combinations
from typing import Iterable

from .loader import Draw

WEEKDAYS_PT = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo",
}

WEEKDAY_ORDER = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo",
]


def number_frequency(draws: Iterable[Draw]) -> Counter[int]:
    counter: Counter[int] = Counter()
    for draw in draws:
        counter.update(draw.bolas)
    return counter


def combination_frequency(draws: Iterable[Draw], size: int) -> Counter[tuple[int, ...]]:
    counter: Counter[tuple[int, ...]] = Counter()
    for draw in draws:
        counter.update(combinations(draw.bolas, size))
    return counter


def draws_ending_in_zero(draws: Iterable[Draw]) -> list[Draw]:
    return [d for d in draws if d.concurso % 10 == 0]


def group_by_weekday(draws: Iterable[Draw]) -> dict[str, list[Draw]]:
    groups: dict[str, list[Draw]] = {day: [] for day in WEEKDAY_ORDER}
    for draw in draws:
        groups[WEEKDAYS_PT[draw.data.weekday()]].append(draw)
    return groups
