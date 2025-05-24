#!/usr/bin/env python3

import sys
import argparse
import pytest
from pathlib import Path

def run_tests(verbose: bool = False) -> None:
    """Esegue la suite di test del progetto."""
    args = ["-v"] if verbose else []
    pytest.main(args + ["test_advanced_assignment_strategies.py"])

def run_assigner(args_list: list) -> None:
    """Esegue lo script di assegnazione caratteri."""
    import advanced_assignment_strategies
    sys.argv = ["advanced_assignment_strategies.py"] + args_list
    advanced_assignment_strategies.main()

def main() -> None:
    parser = argparse.ArgumentParser(
        description="BestCharacterAssigner - Sistema di assegnazione caratteri"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comandi disponibili")
    
    # Subparser per i test
    test_parser = subparsers.add_parser("test", help="Esegui i test")
    test_parser.add_argument("-v", "--verbose", action="store_true", help="Output verboso")
    
    # Subparser per l'assegnazione
    assign_parser = subparsers.add_parser("assign", help="Esegui l'assegnazione caratteri")
    assign_parser.add_argument("preference_file", help="File CSV con le preferenze")
    assign_parser.add_argument("--format", choices=["wide", "long"], default="wide",
                             help="Formato CSV (default: wide)")
    assign_parser.add_argument("--delimiter", default=",", help="Delimitatore CSV (default: ,)")
    assign_parser.add_argument("--strategy", help="Strategia da utilizzare (opzionale)")

    args = parser.parse_args()

    if args.command == "test":
        run_tests(args.verbose)
    elif args.command == "assign":
        assign_args = []
        assign_args.append(args.preference_file)
        if args.format:
            assign_args.extend(["--format", args.format])
        if args.delimiter:
            assign_args.extend(["--delimiter", args.delimiter])
        if args.strategy:
            assign_args.extend(["--strategy", args.strategy])
        run_assigner(assign_args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
