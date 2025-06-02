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

    assegnatore = advanced_assignment_strategies.AdvancedCharacterAssignment()

    try:
        # Parse arguments
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("preference_file", help="File CSV con le preferenze")
        parser.add_argument(
            "--format",
            choices=["wide", "long"],
            default="wide",
            help="Formato CSV (default: wide)",
        )
        parser.add_argument(
            "--delimiter", default=",", help="Delimitatore CSV (default: ,)"
        )
        parser.add_argument(
            "--strategy",
            choices=[
                "hungarian",
                "balanced",
                "priority_fair",
                "greedy_smart",
                "hybrid",
            ],
            help="Strategia da utilizzare",
        )
        args = parser.parse_args(args_list)

        # Carica i dati
        assegnatore.carica_da_csv(
            args.preference_file, formato=args.format, delimiter=args.delimiter
        )

        # Analizza e mostra i conflitti
        assegnatore.stampa_analisi_conflitti()

        # Se è specificata una strategia, usala direttamente
        if args.strategy:
            risultato = assegnatore.assegna_con_strategia(args.strategy)
            print(f"\n✨ Assignments using {args.strategy.upper()} strategy:")
            for persona, personaggio in risultato.items():
                print(f"   • {persona} -> {personaggio}")
        else:
            # Altrimenti confronta tutte le strategie e usa la migliore
            print("\n🔍 Comparing strategies to find the best one...\n")
            risultati = assegnatore.confronta_strategie()
            migliore = assegnatore.trova_migliore_strategia(risultati)
            print(f"\n✨ Best strategy is: {migliore.upper()}")
            risultato = assegnatore.assegna_con_strategia(migliore)
            print("\nFinal assignments:")
            for persona, personaggio in risultato.items():
                print(f"   • {persona} -> {personaggio}")
    except Exception as e:
        print(f"❌ Error during assignment: {e}")
        exit(1)


def run_evaluate(args_list: list) -> None:
    """Esegue il confronto delle strategie di assegnazione."""
    import advanced_assignment_strategies

    assegnatore = advanced_assignment_strategies.AdvancedCharacterAssignment()

    try:
        assegnatore.carica_da_csv(
            args_list[0], formato=args_list[1], delimiter=args_list[2]
        )
        assegnatore.analizza_conflitti()
        print("\n🔍 Confronto strategie per trovare la migliore...\n")
        risultati = assegnatore.confronta_strategie()
        migliore = assegnatore.trova_migliore_strategia(risultati)
        print(f"\n✨ La strategia migliore è: {migliore.upper()}\n")
    except Exception as e:
        print(f"❌ Errore durante la valutazione: {e}")
        exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="BestCharacterAssigner - Sistema di assegnazione caratteri"
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandi disponibili")

    # Subparser per i test
    test_parser = subparsers.add_parser("test", help="Esegui i test")
    test_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Output verboso"
    )

    # Subparser per l'assegnazione
    assign_parser = subparsers.add_parser(
        "assign", help="Esegui l'assegnazione caratteri"
    )
    assign_parser.add_argument("preference_file", help="File CSV con le preferenze")
    assign_parser.add_argument(
        "--format",
        choices=["wide", "long"],
        default="wide",
        help="Formato CSV (default: wide)",
    )
    assign_parser.add_argument(
        "--delimiter", default=",", help="Delimitatore CSV (default: ,)"
    )
    assign_parser.add_argument("--strategy", help="Strategia da utilizzare (opzionale)")

    # Subparser per la valutazione delle strategie
    evaluate_parser = subparsers.add_parser(
        "evaluate", help="Valuta quale sia la strategia migliore"
    )
    evaluate_parser.add_argument("preference_file", help="File CSV con le preferenze")
    evaluate_parser.add_argument(
        "--format",
        choices=["wide", "long"],
        default="wide",
        help="Formato CSV (default: wide)",
    )
    evaluate_parser.add_argument(
        "--delimiter", default=",", help="Delimitatore CSV (default: ,)"
    )

    args = parser.parse_args()

    if args.command == "test":
        run_tests(args.verbose)
    elif args.command == "assign":
        assign_args = []
        assign_args.append(args.preference_file)
        if args.format != "wide":  # Aggiungi solo se diverso dal default
            assign_args.extend(["--format", args.format])
        if args.delimiter != ",":  # Aggiungi solo se diverso dal default
            assign_args.extend(["--delimiter", args.delimiter])
        if args.strategy:  # Strategy è sempre opzionale
            assign_args.extend(["--strategy", args.strategy])
        run_assigner(assign_args)
    elif args.command == "evaluate":
        evaluate_args = [args.preference_file, args.format, args.delimiter]
        run_evaluate(evaluate_args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
