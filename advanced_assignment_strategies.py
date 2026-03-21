"""
Advanced Assignment System with Multiple Strategies

Implements different strategies to improve character assignment:
1. Preventive conflict analysis
2. Popularity balancing
3. Automatic preference expansion
4. Alternative algorithms with different priorities
5. Input improvement suggestions

Author: AI Assistant
Version: 3.0 - Advanced Strategies
"""

import logging
import random
from collections import Counter
from datetime import datetime
from statistics import mean as statistics_mean
from typing import Dict, List, Set

# Configure module-level logger
logger = logging.getLogger(__name__)

# Thresholds and configuration constants
CONFLICT_THRESHOLD = (
    0.6  # Fraction of people requesting a character to flag it as critical
)
RISK_CONFLICT_RATIO = (
    0.8  # Fraction of a person's preferences in conflict to flag as at-risk
)
SIMILARITY_THRESHOLD = 0.3  # Minimum Jaccard similarity to suggest a character
BALANCED_RANDOM_RATIO = (
    0.7  # Probability of popularity-based choice in balanced expansion
)
PREFERENCE_PENALTY = 1000  # Cost penalty when assigned character is not in preferences

try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from scipy.optimize import linear_sum_assignment

    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


class AdvancedCharacterAssignment:
    """
    Advanced system for optimal assignment with multiple strategies.

    Advanced features:
    - Preventive conflict analysis
    - Automatic popularity balancing
    - Intelligent preference expansion
    - Multiple assignment strategies
    - Input improvement suggestions
    """

    def __init__(self):
        self.people_choices = {}
        self.all_characters = []
        self.conflict_analysis = None
        self.available_strategies = [
            "hungarian",      # Classic Hungarian algorithm
            "balanced",       # Balanced by popularity
            "priority_fair",  # Priority to less fortunate
            "greedy_smart",   # Smart greedy algorithm
            "hybrid",         # Combination of strategies
        ]

    def _create_character_pool(self, n_people: int) -> Counter:
        """
        Create a Counter of available character slots, replicating as needed.

        Args:
            n_people: Number of people to assign characters to

        Returns:
            Counter mapping character name to available slots
        """
        if not self.all_characters:
            raise ValueError("No characters available")
        n_characters = len(self.all_characters)
        copies_needed = (n_people + n_characters - 1) // n_characters
        pool: List[str] = []
        for _ in range(copies_needed):
            pool.extend(self.all_characters)
        return Counter(pool[:n_people])

    def analyze_conflicts(self) -> Dict:
        """
        Preemptively analyzes potential conflicts in preferences.

        Returns:
            dict: Detailed analysis with:
                - popular_characters: most requested characters
                - at_risk_people: people with limited preferences
                - avg_preferences: average preferences per person
                - suggestions: improvement recommendations
        """
        if not self.people_choices:
            return {"error": "No data loaded"}

        # Count popularity of each character
        popularity = Counter()
        preference_lengths = {}

        for person, preferences in self.people_choices.items():
            preference_lengths[person] = len(preferences)
            for character in preferences:
                popularity[character] += 1

        # Identify conflicts
        n_people = len(self.people_choices)
        conflict_characters = {
            c: count for c, count in popularity.items() if count > 1
        }
        critical_characters = {
            c: count
            for c, count in popularity.items()
            if count >= n_people * CONFLICT_THRESHOLD
        }

        # At-risk people (few preferences in high-conflict zones)
        at_risk_people = []
        for person, preferences in self.people_choices.items():
            if len(preferences) <= 2:  # Few preferences
                personal_conflicts = sum(
                    1 for c in preferences if c in conflict_characters
                )
                if personal_conflicts >= len(preferences) * RISK_CONFLICT_RATIO:
                    at_risk_people.append(
                        {
                            "person": person,
                            "preferences": len(preferences),
                            "conflicts": personal_conflicts,
                        }
                    )

        # Underutilized characters
        characters_set = set(self.all_characters)
        unrequested_characters = characters_set - set(popularity.keys())

        # Suggestions
        suggestions = []

        if critical_characters:
            suggestions.append(
                f"⚠️ Highly requested characters: {', '.join(critical_characters.keys())}"
            )

        if at_risk_people:
            names = [p["person"] for p in at_risk_people]
            suggestions.append(
                f"⚠️ People at risk (few preferences): {', '.join(names)}"
            )

        if unrequested_characters:
            suggestions.append(
                f"💡 Never requested characters: {', '.join(unrequested_characters)}"
            )
            suggestions.append("💡 Consider removing or promoting them")

        if len(self.all_characters) - len(self.people_choices) < 2:
            suggestions.append("⚠️ Few backup characters, consider adding more")

        pref_values = list(preference_lengths.values())
        avg_preferences = (
            float(np.mean(pref_values))
            if NUMPY_AVAILABLE
            else float(statistics_mean(pref_values))
        )

        self.conflict_analysis = {
            "n_people": n_people,
            "n_characters": len(self.all_characters),
            "popular_characters": dict(popularity.most_common(5)),
            "conflict_characters": conflict_characters,
            "critical_characters": critical_characters,
            "at_risk_people": at_risk_people,
            "unrequested_characters": list(unrequested_characters),
            "avg_preferences": avg_preferences,
            "suggestions": suggestions,
        }

        return self.conflict_analysis

    def print_conflict_analysis(self):
        """Print conflict analysis in readable format."""
        if not self.conflict_analysis:
            self.analyze_conflicts()

        analysis = self.conflict_analysis

        print("=== CONFLICT AND RISK ANALYSIS ===\n")

        print(f"📊 General statistics:")
        print(f"   • People: {analysis['n_people']}")
        print(f"   • Characters: {analysis['n_characters']}")
        print(f"   • Average preferences per person: {analysis['avg_preferences']:.1f}")
        print()

        if analysis["popular_characters"]:
            print("🔥 Most requested characters:")
            for character, count in analysis["popular_characters"].items():
                percentage = count / analysis["n_people"] * 100
                print(f"   • {character}: {count} people ({percentage:.1f}%)")
            print()

        if analysis["critical_characters"]:
            print("⚠️ CRITICAL CONFLICTS:")
            for character, count in analysis["critical_characters"].items():
                print(f"   • {character}: requested by {count} people!")
            print()

        if analysis["at_risk_people"]:
            print("🚨 People at risk of dissatisfaction:")
            for info in analysis["at_risk_people"]:
                print(
                    f"   • {info['person']}: {info['preferences']} preferences, "
                    f"{info['conflicts']} in conflict"
                )
            print()

        if analysis["unrequested_characters"]:
            print("😴 Never requested characters:")
            print(f"   • {', '.join(analysis['unrequested_characters'])}")
            print()

        if analysis["suggestions"]:
            print("💡 SUGGESTIONS:")
            for suggestion in analysis["suggestions"]:
                print(f"   {suggestion}")
            print()

    def expand_preferences(
        self, method: str = "similarity"
    ) -> Dict[str, List[str]]:
        """
        Automatically expands preferences to reduce conflicts.

        Args:
            method: 'similarity', 'popularity', 'random', 'balanced'

        Returns:
            dict: New expanded preferences for each person
        """
        if not self.conflict_analysis:
            self.analyze_conflicts()

        expanded_preferences = {}
        available_characters = set(self.all_characters)

        for person, original_preferences in self.people_choices.items():
            new_preferences = original_preferences.copy()
            used_characters = set(original_preferences)

            # Add until we have at least 3-4 preferences
            target_preferences = min(4, len(self.all_characters))

            while len(new_preferences) < target_preferences:
                candidates = available_characters - used_characters
                if not candidates:
                    break

                if method == "popularity":
                    # Add less popular characters
                    popularity = self.conflict_analysis["popular_characters"]
                    candidate = min(candidates, key=lambda x: popularity.get(x, 0))

                elif method == "similarity":
                    # Add characters requested by people with similar preferences
                    candidate = self._find_similar_character(person, candidates)

                elif method == "balanced":
                    # Mix of popularity and randomness
                    if random.random() < BALANCED_RANDOM_RATIO:
                        popularity = self.conflict_analysis["popular_characters"]
                        candidate = min(candidates, key=lambda x: popularity.get(x, 0))
                    else:
                        candidate = random.choice(list(candidates))

                else:  # random
                    candidate = random.choice(list(candidates))

                new_preferences.append(candidate)
                used_characters.add(candidate)

            expanded_preferences[person] = new_preferences

        return expanded_preferences

    def _find_similar_character(
        self, target_person: str, candidates: Set[str]
    ) -> str:
        """Find a character based on people with similar preferences."""
        target_preferences = set(self.people_choices[target_person])

        # Find people with similar preferences
        similarity_scores = {}
        for other_person, other_preferences in self.people_choices.items():
            if other_person == target_person:
                continue

            other_pref_set = set(other_preferences)
            intersection = len(target_preferences & other_pref_set)
            union = len(target_preferences | other_pref_set)

            if union > 0:
                similarity = intersection / union  # Jaccard similarity
                similarity_scores[other_person] = similarity

        # Find characters used by similar people
        suggested_characters = Counter()
        for other_person, similarity in similarity_scores.items():
            if similarity > SIMILARITY_THRESHOLD:
                for character in self.people_choices[other_person]:
                    if character in candidates:
                        suggested_characters[character] += similarity

        if suggested_characters:
            return suggested_characters.most_common(1)[0][0]
        else:
            return random.choice(list(candidates))

    def assign_with_strategy(
        self, strategy: str = "hybrid", expand_prefs: bool = True
    ) -> Dict[str, str]:
        """
        Assign characters using the specified strategy.

        Args:
            strategy: Name of the strategy to use
            expand_prefs: Whether to automatically expand preferences

        Returns:
            dict: Assignments {person: character}
        """
        if not self.people_choices:
            raise ValueError("No data loaded")

        # Analyze conflicts if not done
        if not self.conflict_analysis:
            self.analyze_conflicts()

        # Expand preferences if requested
        preferences_to_use = self.people_choices
        if expand_prefs:
            print("🔧 Expanding preferences to reduce conflicts...")
            preferences_to_use = self.expand_preferences("balanced")
            print(f"   Preferences expanded for {len(preferences_to_use)} people")

        # Run chosen strategy
        if strategy == "hungarian":
            return self._assign_hungarian(preferences_to_use)
        elif strategy == "balanced":
            return self._assign_balanced(preferences_to_use)
        elif strategy == "priority_fair":
            return self._assign_priority_fair(preferences_to_use)
        elif strategy == "greedy_smart":
            return self._assign_greedy_smart(preferences_to_use)
        elif strategy == "hybrid":
            return self._assign_hybrid(preferences_to_use)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    def _assign_hungarian(self, preferences: Dict[str, List[str]]) -> Dict[str, str]:
        """Classic Hungarian algorithm."""
        if not SCIPY_AVAILABLE:
            logger.warning("scipy not available, using smart greedy algorithm...")
            print("⚠️ scipy not available, using smart greedy algorithm...")
            return self._assign_greedy_smart(preferences)

        if not NUMPY_AVAILABLE:
            logger.warning("numpy not available, using smart greedy algorithm...")
            print("⚠️ numpy not available, using smart greedy algorithm...")
            return self._assign_greedy_smart(preferences)

        people = list(preferences.keys())
        original_characters = self.all_characters

        # Calculate how many copies of each character are needed
        n_people = len(people)
        n_characters = len(original_characters)
        copies_needed = (n_people + n_characters - 1) // n_characters

        # Replicate characters the necessary number of times
        characters = []
        for _ in range(copies_needed):
            characters.extend(original_characters)
        characters = characters[:n_people]

        # Cost matrix: PREFERENCE_PENALTY for non-preferred assignments
        costs = np.full((n_people, n_people), float(PREFERENCE_PENALTY))

        for i, person in enumerate(people):
            choices = preferences[person]
            for j, character in enumerate(characters):
                if character in choices:
                    costs[i][j] = choices.index(character)

        # Solve
        people_indices, character_indices = linear_sum_assignment(costs)

        return {
            people[i]: characters[j]
            for i, j in zip(people_indices, character_indices)
        }

    def _assign_balanced(self, preferences: Dict[str, List[str]]) -> Dict[str, str]:
        """Strategy that balances character popularity."""
        assignments = {}
        n_people = len(preferences)

        # Count popularity
        popularity = Counter()
        for choices in preferences.values():
            for character in choices:
                popularity[character] += 1

        # Available character pool via Counter (O(1) membership and removal)
        availability = self._create_character_pool(n_people)

        # Sort people: those with rarer preferences first
        def preference_rarity(person):
            choices = preferences[person]
            return (
                sum(popularity[c] for c in choices) / len(choices)
                if choices
                else float("inf")
            )

        sorted_people = sorted(preferences.keys(), key=preference_rarity)

        for person in sorted_people:
            choices = preferences[person]
            assigned = False

            # Search in preferences, prioritizing less popular ones
            sorted_choices = sorted(choices, key=lambda x: popularity[x])

            for character in sorted_choices:
                if availability[character] > 0:
                    assignments[person] = character
                    availability[character] -= 1
                    assigned = True
                    break

            # Emergency assignment from remaining pool
            if not assigned:
                for character, count in availability.items():
                    if count > 0:
                        assignments[person] = character
                        availability[character] -= 1
                        break

        return assignments

    def _assign_priority_fair(
        self, preferences: Dict[str, List[str]]
    ) -> Dict[str, str]:
        """Strategy that gives priority to those with fewer options."""
        assignments = {}
        n_people = len(preferences)

        # Available character pool via Counter
        availability = self._create_character_pool(n_people)

        # Sort by number of preferences (fewer first)
        sorted_people = sorted(preferences.keys(), key=lambda x: len(preferences[x]))

        for person in sorted_people:
            choices = preferences[person]
            assigned = False

            # Try all preferences
            for character in choices:
                if availability[character] > 0:
                    assignments[person] = character
                    availability[character] -= 1
                    assigned = True
                    break

            # Random assignment if necessary
            if not assigned:
                for character, count in availability.items():
                    if count > 0:
                        assignments[person] = character
                        availability[character] -= 1
                        break

        return assignments

    def _assign_greedy_smart(
        self, preferences: Dict[str, List[str]]
    ) -> Dict[str, str]:
        """Improved version of the greedy algorithm."""
        assignments = {}
        n_people = len(preferences)

        # Available character pool via Counter
        availability = self._create_character_pool(n_people)

        # Calculate "urgency" for each person
        def calculate_urgency(person):
            choices = preferences[person]
            available = sum(1 for c in choices if availability[c] > 0)
            return available  # Fewer options = more urgent

        # Process in order of urgency
        remaining_people = set(preferences.keys())
        while remaining_people:
            urgent_person = min(remaining_people, key=calculate_urgency)
            choices = preferences[urgent_person]

            # Assign first available preference
            assigned = False
            for character in choices:
                if availability[character] > 0:
                    assignments[urgent_person] = character
                    availability[character] -= 1
                    assigned = True
                    break

            # If no preferences available, assign the first available character
            if not assigned:
                for character, count in availability.items():
                    if count > 0:
                        assignments[urgent_person] = character
                        availability[character] -= 1
                        break

            remaining_people.discard(urgent_person)

        return assignments

    def _assign_hybrid(self, preferences: Dict[str, List[str]]) -> Dict[str, str]:
        """Hybrid strategy that tests all sub-strategies and picks the best result."""
        # Explicit dispatch table mapping strategy names to their methods
        strategy_map = {
            "hungarian": self._assign_hungarian,
            "balanced": self._assign_balanced,
            "priority_fair": self._assign_priority_fair,
            "greedy_smart": self._assign_greedy_smart,
        }
        results = []

        for strategy, fn in strategy_map.items():
            if strategy == "hungarian" and not SCIPY_AVAILABLE:
                continue

            try:
                assignment = fn(preferences)
                score = self._evaluate_assignment(assignment, preferences)
                results.append((strategy, assignment, score))
            except Exception as e:
                logger.warning(f"Strategy '{strategy}' failed in hybrid: {e}")
                continue

        if not results:
            return self._assign_greedy_smart(preferences)

        # Choose the best (lower score = better)
        best = min(results, key=lambda x: x[2])
        print(
            f"🎯 Hybrid strategy: used '{best[0]}' (score: {best[2]:.2f})"
        )

        return best[1]

    def _evaluate_assignment(
        self, assignments: Dict[str, str], preferences: Dict[str, List[str]]
    ) -> float:
        """Evaluate the quality of an assignment."""
        total_score = 0
        satisfied_count = 0

        for person, character in assignments.items():
            choices = preferences[person]
            if character in choices:
                position = choices.index(character)
                total_score += position  # 0 = better
                satisfied_count += 1
            else:
                total_score += PREFERENCE_PENALTY

        # Bonus for high satisfaction percentage
        satisfaction_rate = satisfied_count / len(assignments)
        total_score *= 2 - satisfaction_rate  # Multiply by 1-2

        return total_score

    def compare_strategies(self) -> Dict:
        """Compare all available strategies."""
        if not self.people_choices:
            raise ValueError("No data loaded")

        comparison_results = {}

        print("🔍 Comparing all strategies...\n")

        for strategy in self.available_strategies:
            if strategy == "hungarian" and not SCIPY_AVAILABLE:
                continue
            if strategy == "hybrid":  # Avoid recursion
                continue

            try:
                assignment = self.assign_with_strategy(
                    strategy, expand_prefs=False
                )

                # Calculate statistics
                total_cost = 0
                satisfied_count = 0
                details = []
                n_people = len(self.people_choices)

                # Verify that there are assignments for all people
                if len(assignment) != n_people:
                    raise ValueError(
                        f"Incomplete assignments: {len(assignment)}/{n_people} people"
                    )

                for person, character in assignment.items():
                    choices = self.people_choices[person]
                    if character in choices:
                        position = choices.index(character)
                        total_cost += position
                        satisfied_count += 1
                        details.append(
                            f"{person}: {character} (pref #{position+1})"
                        )
                    else:
                        total_cost += PREFERENCE_PENALTY
                        details.append(f"{person}: {character} (NOT preferred)")

                percentage = (satisfied_count / n_people) * 100

                comparison_results[strategy] = {
                    "assignment": assignment,
                    "total_cost": total_cost,
                    "satisfied_preferences": f"{satisfied_count}/{len(assignment)}",
                    "satisfaction_percentage": percentage,
                    "details": details,
                }

                print(f"✅ {strategy.upper()}:")
                print(f"   Total cost: {total_cost}")
                print(
                    f"   Satisfaction: {percentage:.1f}% ({satisfied_count}/{len(assignment)})"
                )
                print()

            except Exception as e:
                logger.error(f"Strategy '{strategy}' failed during comparison: {e}")
                print(f"❌ {strategy}: Error - {e}")
                print()

        return comparison_results

    def load_from_csv(
        self, file_path: str, formato: str = "wide", delimiter: str = ","
    ) -> None:
        """
        Load preferences from a CSV file using CSVHandler.

        Args:
            file_path: Path to the CSV file
            formato: 'wide' or 'long'. In 'wide' format each row is a person and columns are preferences.
                    In 'long' format each row is a person-character pair.
            delimiter: CSV separator character (default: comma)
        """
        from csv_handler import CSVHandler

        try:
            self.people_choices, self.all_characters = CSVHandler.load_from_csv(
                file_path, formato, delimiter
            )
            # Reset conflict analysis
            self.conflict_analysis = None

        except Exception as e:
            print(f"❌ Error loading CSV: {str(e)}")
            raise

    def print_advanced_results(self, assignments: Dict[str, str]):
        """Advanced version of result printing."""
        print("=== ADVANCED ASSIGNMENT RESULTS ===\n")

        if self.conflict_analysis:
            at_risk = {
                p["person"] for p in self.conflict_analysis["at_risk_people"]
            }
        else:
            at_risk = set()

        total_cost = 0
        satisfied_count = 0
        results_by_category = {
            "excellent": [],
            "good": [],
            "acceptable": [],
            "problematic": [],
        }

        for person, character in assignments.items():
            choices = self.people_choices[person]
            risk_emoji = "🚨" if person in at_risk else ""

            if character in choices:
                position = choices.index(character)
                total_cost += position
                satisfied_count += 1

                if position == 0:
                    category = "excellent"
                    emoji = "🥇"
                elif position <= 1:
                    category = "good"
                    emoji = "🥈"
                else:
                    category = "acceptable"
                    emoji = "🥉"

                results_by_category[category].append(
                    f"{emoji} {person}: {character} (preference #{position+1}) {risk_emoji}"
                )
            else:
                total_cost += PREFERENCE_PENALTY
                results_by_category["problematic"].append(
                    f"😞 {person}: {character} (NOT in preferences) {risk_emoji}"
                )

        # Print by category
        for category, results in results_by_category.items():
            if results:
                print(f"{category.upper()}:")
                for result in results:
                    print(f"  {result}")
                print()

        # Final statistics
        percentage = satisfied_count / len(assignments) * 100
        print(f"📊 FINAL STATISTICS:")
        print(f"   • Total cost: {total_cost}")
        print(
            f"   • Satisfied preferences: {satisfied_count}/{len(assignments)} ({percentage:.1f}%)"
        )

        if percentage >= 90:
            print("   🎉 EXCELLENT Result!")
        elif percentage >= 75:
            print("   👍 GOOD Result")
        elif percentage >= 50:
            print("   😐 ACCEPTABLE Result")
        else:
            print("   😞 PROBLEMATIC Result - consider revising preferences")

    def find_best_strategy(self, comparison_results: Dict) -> str:
        """Find the best strategy based on comparison results."""
        if not comparison_results:
            return "hybrid"  # Default if no results

        # Find the strategy with the best cost/satisfaction ratio
        best_strategy = None
        best_score = float("inf")

        for strategy, result in comparison_results.items():
            cost = result["total_cost"]
            percentage = result["satisfaction_percentage"]

            # Calculate a weighted score (lower = better)
            # Give more weight to satisfaction percentage
            score = cost * (100 - percentage)

            if score < best_score:
                best_score = score
                best_strategy = strategy

        return best_strategy

    def generate_text_report(
        self, assignments: Dict[str, str], best_strategy: str
    ) -> str:
        """Generate a detailed text report of the assignment."""
        if not self.conflict_analysis:
            self.analyze_conflicts()

        report = []
        report.append("=== CHARACTER ASSIGNMENT REPORT ===")
        report.append(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        report.append(f"Strategy used: {best_strategy.upper()}\n")

        # General statistics
        n_people = len(self.people_choices)
        n_characters = len(self.all_characters)
        report.append("GENERAL STATISTICS:")
        report.append(f"• Number of people: {n_people}")
        report.append(f"• Number of available characters: {n_characters}")
        report.append(
            f"• Average preferences per person: {self.conflict_analysis['avg_preferences']:.1f}\n"
        )

        # Results by person
        report.append("ASSIGNMENTS:")
        sorted_people = sorted(assignments.keys())
        for person in sorted_people:
            character = assignments[person]
            choices = self.people_choices[person]
            if character in choices:
                position = choices.index(character) + 1
                report.append(f"• {person}: {character} (choice #{position})")
            else:
                report.append(f"• {person}: {character} (not in preferences)")

        # Satisfaction statistics
        n_satisfied = sum(
            1 for p, c in assignments.items() if c in self.people_choices[p]
        )
        satisfaction_pct = (n_satisfied / n_people) * 100

        report.append(f"\nFINAL RESULTS:")
        report.append(
            f"• People who received one of their choices: {n_satisfied}/{n_people}"
        )
        report.append(f"• Satisfaction percentage: {satisfaction_pct:.1f}%")

        # Final evaluation
        if satisfaction_pct >= 90:
            report.append("• Evaluation: EXCELLENT")
        elif satisfaction_pct >= 75:
            report.append("• Evaluation: GOOD")
        elif satisfaction_pct >= 50:
            report.append("• Evaluation: ACCEPTABLE")
        else:
            report.append("• Evaluation: PROBLEMATIC")

        return "\n".join(report)
