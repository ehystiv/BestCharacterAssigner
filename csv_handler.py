"""
CSV file handling for the character assignment system.

This module handles loading and managing CSV data
for the character assignment system.
"""

import logging
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

logger = logging.getLogger(__name__)


class CSVHandler:
    """Class for managing CSV files in the assignment system."""

    @staticmethod
    def load_from_csv(
        file_path: str, formato: str = "wide", delimiter: str = ","
    ) -> Tuple[Dict[str, List[str]], List[str]]:
        """
        Load preferences from a CSV file.

        Args:
            file_path: Path to the CSV file
            formato: 'wide' or 'long'. In 'wide' format each row is a person and columns are preferences.
                    In 'long' format each row is a person-character pair.
            delimiter: CSV separator character (default: comma)

        Returns:
            Tuple[Dict[str, List[str]], List[str]]: Tuple containing:
                - Dictionary of preferences {person: [preferences]}
                - List of all unique characters

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the format is not supported or the file is empty.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        try:
            people_choices = {}

            if formato == "wide":
                # Wide format: each row is a person, columns are preferences
                df = pd.read_csv(file_path, sep=delimiter, encoding="utf-8")

                if df.empty:
                    raise ValueError("CSV file is empty")

                # First column is the person's name
                people = df.iloc[:, 0].tolist()

                # Remaining columns are preferences
                for i, person in enumerate(people):
                    # Keep only non-null preferences
                    preferences = [p for p in df.iloc[i, 1:].tolist() if pd.notna(p)]
                    if preferences:  # Add only if at least one preference exists
                        people_choices[str(person)] = [str(p) for p in preferences]

            elif formato == "long":
                # Long format: each row is a person-character pair
                df = pd.read_csv(file_path, sep=delimiter, encoding="utf-8")

                if df.empty:
                    raise ValueError("CSV file is empty")

                if len(df.columns) < 2:
                    raise ValueError(
                        "The 'long' format requires at least 2 columns: person and character"
                    )

                # Convert long format to dictionary
                for person, group in df.groupby(df.columns[0]):
                    # Take the second column as preference
                    preferences = group.iloc[:, 1].dropna().tolist()
                    if preferences:  # Add only if at least one preference exists
                        people_choices[str(person)] = [str(p) for p in preferences]

            else:
                raise ValueError("Unsupported format. Use 'wide' or 'long'")

            if not people_choices:
                raise ValueError(
                    "No person with valid preferences found in the CSV file"
                )

            # Collect all unique characters (sorted for determinism)
            all_characters = sorted(
                set(
                    preference
                    for preferences in people_choices.values()
                    for preference in preferences
                )
            )

            print(f"✅ Loading complete:")
            print(f"   • {len(people_choices)} people loaded")
            print(f"   • {len(all_characters)} unique characters found")

            return people_choices, all_characters

        except (FileNotFoundError, ValueError):
            raise
        except Exception as e:
            logger.error(f"Error loading CSV '{file_path}': {e}")
            print(f"❌ Error loading CSV: {str(e)}")
            raise

    @staticmethod
    def save_to_csv(
        assignments: Dict[str, str], file_path: str, delimiter: str = ","
    ) -> None:
        """
        Save final assignments to a CSV file.

        Args:
            assignments: Dictionary of assignments {person: character}
            file_path: Path to the CSV file to create
            delimiter: CSV separator character (default: comma)
        """
        try:
            # Create a DataFrame with the assignments
            df = pd.DataFrame(
                [(person, character) for person, character in assignments.items()],
                columns=["Person", "Assigned Character"],
            )

            # Save to CSV with explicit encoding and correct separator
            df.to_csv(file_path, index=False, sep=delimiter, encoding="utf-8")

            print(f"✅ Assignments saved to: {file_path}")

        except Exception as e:
            logger.error(f"Error saving CSV '{file_path}': {e}")
            print(f"❌ Error saving CSV: {str(e)}")
            raise
