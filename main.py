#!/usr/bin/env python3

import sys
import argparse
import pytest
from pathlib import Path


def run_tests(verbose: bool = False) -> None:
    """Run the project test suite."""
    args = ["-v"] if verbose else []
    pytest.main(args + ["test_advanced_assignment_strategies.py"])


def run_assigner(args_list: list) -> None:
    """Run the character assignment script."""
    import advanced_assignment_strategies

    assigner = advanced_assignment_strategies.AdvancedCharacterAssignment()

    try:
        # Parse arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("preference_file", help="CSV file with preferences")
        parser.add_argument(
            "--format",
            choices=["wide", "long"],
            default="wide",
            help="CSV format (default: wide)",
        )
        parser.add_argument(
            "--delimiter", default=",", help="CSV delimiter (default: ,)"
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
            help="Strategy to use",
        )
        args = parser.parse_args(args_list)

        # Load data
        assigner.load_from_csv(
            args.preference_file, formato=args.format, delimiter=args.delimiter
        )

        # Analyze and print conflicts
        assigner.print_conflict_analysis()

        # If a strategy is specified, use it directly
        if args.strategy:
            result = assigner.assign_with_strategy(args.strategy)
            print(f"\n✨ Assignments using {args.strategy.upper()} strategy:")
            for person, character in result.items():
                print(f"   • {person} -> {character}")
        else:
            # Otherwise compare all strategies and use the best one
            print("\n🔍 Comparing strategies to find the best one...\n")
            results = assigner.compare_strategies()
            best = assigner.find_best_strategy(results)
            print(f"\n✨ Best strategy is: {best.upper()}")
            result = assigner.assign_with_strategy(best)
            print("\nFinal assignments:")
            for person, character in result.items():
                print(f"   • {person} -> {character}")
    except Exception as e:
        print(f"❌ Error during assignment: {e}")
        exit(1)


def run_evaluate(
    preference_file: str, formato: str = "wide", delimiter: str = ","
) -> None:
    """Run strategy comparison for assignment."""
    import advanced_assignment_strategies

    assigner = advanced_assignment_strategies.AdvancedCharacterAssignment()

    try:
        assigner.load_from_csv(preference_file, formato=formato, delimiter=delimiter)
        assigner.analyze_conflicts()
        print("\n🔍 Comparing strategies to find the best one...\n")
        results = assigner.compare_strategies()
        best = assigner.find_best_strategy(results)
        print(f"\n✨ Best strategy is: {best.upper()}\n")
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")
        exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="BestCharacterAssigner - Character assignment system"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for tests
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose output"
    )

    # Subparser for assignment
    assign_parser = subparsers.add_parser(
        "assign", help="Run character assignment"
    )
    assign_parser.add_argument("preference_file", help="CSV file with preferences")
    assign_parser.add_argument(
        "--format",
        choices=["wide", "long"],
        default="wide",
        help="CSV format (default: wide)",
    )
    assign_parser.add_argument(
        "--delimiter", default=",", help="CSV delimiter (default: ,)"
    )
    assign_parser.add_argument("--strategy", help="Strategy to use (optional)")

    # Subparser for strategy evaluation
    evaluate_parser = subparsers.add_parser(
        "evaluate", help="Evaluate which strategy is best"
    )
    evaluate_parser.add_argument("preference_file", help="CSV file with preferences")
    evaluate_parser.add_argument(
        "--format",
        choices=["wide", "long"],
        default="wide",
        help="CSV format (default: wide)",
    )
    evaluate_parser.add_argument(
        "--delimiter", default=",", help="CSV delimiter (default: ,)"
    )

    args = parser.parse_args()

    if args.command == "test":
        run_tests(args.verbose)
    elif args.command == "assign":
        assign_args = []
        assign_args.append(args.preference_file)
        if args.format != "wide":  # Add only if different from default
            assign_args.extend(["--format", args.format])
        if args.delimiter != ",":  # Add only if different from default
            assign_args.extend(["--delimiter", args.delimiter])
        if args.strategy:  # Strategy is always optional
            assign_args.extend(["--strategy", args.strategy])
        run_assigner(assign_args)
    elif args.command == "evaluate":
        run_evaluate(args.preference_file, args.format, args.delimiter)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
