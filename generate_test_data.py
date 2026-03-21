import argparse
import itertools
import random
import sys
from datetime import datetime

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate random test data for BestCharacterAssigner"
    )
    parser.add_argument(
        "--people",
        type=int,
        default=300,
        help="Number of people to generate (default: 300)",
    )
    parser.add_argument(
        "--choices",
        type=int,
        default=4,
        help="Number of choices per person (default: 4)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output CSV filename (default: test_data_<timestamp>.csv)",
    )
    parser.add_argument(
        "--format",
        choices=["wide", "long"],
        default="wide",
        help="CSV output format (default: wide)",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=",",
        help="CSV delimiter (default: ,)",
    )
    return parser.parse_args()


# Lists of common Italian names and surnames
first_names = [
    "Alessandro",
    "Sofia",
    "Lorenzo",
    "Giulia",
    "Matteo",
    "Emma",
    "Leonardo",
    "Aurora",
    "Francesco",
    "Alice",
    "Giuseppe",
    "Martina",
    "Andrea",
    "Chiara",
    "Marco",
    "Sara",
    "Antonio",
    "Valentina",
    "Giovanni",
    "Beatrice",
    "Gabriele",
    "Francesca",
    "Davide",
    "Elena",
    "Nicola",
    "Maria",
    "Paolo",
    "Anna",
    "Luca",
    "Laura",
]

last_names = [
    "Rossi",
    "Ferrari",
    "Russo",
    "Bianchi",
    "Romano",
    "Gallo",
    "Costa",
    "Fontana",
    "Conti",
    "Esposito",
    "Ricci",
    "Bruno",
    "De Luca",
    "Moretti",
    "Marino",
    "Greco",
    "Barbieri",
    "Lombardi",
    "Giordano",
    "Colombo",
    "Mancini",
    "Longo",
    "Leone",
    "Mariani",
    "Martinelli",
    "Rinaldi",
    "Vitale",
    "Serra",
    "Federici",
    "Caruso",
]

# List of popular Pokemon
pokemon = [
    "Pikachu",
    "Charizard",
    "Mewtwo",
    "Lucario",
    "Greninja",
    "Gardevoir",
    "Rayquaza",
    "Dragonite",
    "Gengar",
    "Metagross",
    "Gyarados",
    "Typhlosion",
    "Umbreon",
    "Sceptile",
    "Blaziken",
    "Darkrai",
    "Garchomp",
    "Zoroark",
    "Mimikyu",
    "Sylveon",
    "Dragapult",
    "Tyranitar",
    "Snorlax",
    "Blastoise",
    "Alakazam",
    "Arcanine",
    "Salamence",
    "Flygon",
    "Absol",
    "Luxray",
    "Scizor",
    "Milotic",
    "Haxorus",
    "Volcarona",
    "Hydreigon",
    "Aegislash",
    "Noivern",
    "Decidueye",
    "Chandelure",
    "Gallade",
]


def main():
    args = parse_args()
    num_people = args.people
    num_choices = args.choices

    if num_people <= 0:
        print("⚠️ Error: --people must be greater than 0")
        sys.exit(1)
    if num_choices <= 0:
        print("⚠️ Error: --choices must be greater than 0")
        sys.exit(1)
    if num_choices > len(pokemon):
        print(
            f"⚠️ Error: --choices ({num_choices}) cannot exceed the number of available characters ({len(pokemon)})"
        )
        sys.exit(1)

    # Generate all possible combinations of names and surnames
    all_people = [
        f"{first} {last}" for first, last in itertools.product(first_names, last_names)
    ]

    max_possible_people = len(all_people)
    if num_people > max_possible_people:
        print(
            f"⚠️ Error: Requested {num_people} people, but only {max_possible_people} combinations are possible"
        )
        sys.exit(1)

    people = random.sample(all_people, num_people)

    # Generate random choices for each person; different people can share the same
    # Pokemon — that is intentional, as the assigner is designed to resolve conflicts.
    choice_columns = [f"Choice{i+1}" for i in range(num_choices)]
    data = []
    for person in people:
        choices = random.sample(pokemon, num_choices)
        data.append([person] + choices)

    # Count unique characters actually present in the generated CSV
    used_characters = set(choice for row in data for choice in row[1:])

    # Determine output filename
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"test_data_{timestamp}.csv"

    if args.format == "long":
        long_rows = [[row[0], choice] for row in data for choice in row[1:]]
        df = pd.DataFrame(long_rows, columns=["Person", "Character"])
    else:
        df = pd.DataFrame(data, columns=["Person"] + choice_columns)

    df.to_csv(output_file, index=False, sep=args.delimiter, encoding="utf-8")
    print(f"✨ Test file generated: {output_file}")
    print(f"📊 Number of people: {num_people}")
    print(f"🎮 Number of unique characters used: {len(used_characters)}")
    print(f"🎯 Choices per person: {num_choices}")
    print(f"📋 Format: {args.format}")


if __name__ == "__main__":
    main()
