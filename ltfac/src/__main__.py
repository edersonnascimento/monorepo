from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import DEFAULT_INPUT, DEFAULT_OUTPUT_DIR
from .loader import load_draws
from .report import build_report, write_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ltfac",
        description="Estatísticas da Lotofácil a partir de um arquivo CSV.",
    )
    parser.add_argument(
        "--input",
        type=str,
        default=str(DEFAULT_INPUT),
        help=f"Caminho do CSV de entrada (padrão: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Diretório de saída (padrão: {DEFAULT_OUTPUT_DIR})",
    )
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    if not input_path.is_file():
        print(f"Arquivo de entrada não encontrado: {input_path}", file=sys.stderr)
        return 1

    draws = load_draws(input_path)
    if not draws:
        print("Nenhum concurso encontrado no CSV.", file=sys.stderr)
        return 1

    report = build_report(draws)
    out_path = write_report(report, output_dir)
    print(f"Relatório salvo em: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
