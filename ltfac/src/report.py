from __future__ import annotations

from collections import Counter
from pathlib import Path

from .loader import Draw
from .stats import (
    WEEKDAY_ORDER,
    group_by_weekday,
    number_frequency,
)


def build_report(draws: list[Draw]) -> str:
    lines: list[str] = []
    first, last = draws[0], draws[-1]

    lines.append("# Estatísticas Lotofácil — 12 meses")
    lines.append("")
    lines.append(f"- **Total de concursos:** {len(draws)}")
    lines.append(
        f"- **Primeiro concurso:** {first.concurso} "
        f"({first.data.strftime('%d/%m/%Y')})"
    )
    lines.append(
        f"- **Último concurso:** {last.concurso} "
        f"({last.data.strftime('%d/%m/%Y')})"
    )
    lines.append("")

    # Módulos do registry
    from .modulos import get_modulos
    for modulo in get_modulos():
        lines.append(modulo.compute(draws))
        lines.append("")

    # Estatísticas por dia da semana (mantido)
    lines.append("## Estatísticas por Dia da Semana")
    lines.append("")
    groups = group_by_weekday(draws)
    for day in WEEKDAY_ORDER:
        day_draws = groups[day]
        if not day_draws:
            continue
        lines.append(f"### {day} ({len(day_draws)} concursos)")
        lines.append("")

        # Top 12 números do dia
        freq = number_frequency(day_draws)
        top12 = freq.most_common(12)
        linhas = ["| Número | Frequência |", "|---:|---:|"]
        for numero, f in sorted(top12, key=lambda x: x[0]):
            linhas.append(f"| {numero} | {f} |")
        lines.extend(linhas)
        lines.append("")

    return "\n".join(lines)


def write_report(report: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "estatisticas_lotofacil.md"
    out_path.write_text(report, encoding="utf-8")
    return out_path
