"""
Test suite for the AdvancedCharacterAssignment class.
"""

import os
import tempfile

import pytest

from advanced_assignment_strategies import AdvancedCharacterAssignment
from typing import Dict, List


@pytest.fixture
def sample_data() -> Dict[str, List[str]]:
    """Fixture that provides sample data for testing."""
    return {
        "Alice": ["Character1", "Character2", "Character3"],
        "Bob": ["Character2", "Character3", "Character4"],
        "Charlie": ["Character3", "Character4", "Character1"],
        "David": ["Character4", "Character1", "Character2"],
    }


@pytest.fixture
def empty_assigner() -> AdvancedCharacterAssignment:
    """Fixture that provides a clean instance of the assigner."""
    return AdvancedCharacterAssignment()


@pytest.fixture
def populated_assigner(sample_data) -> AdvancedCharacterAssignment:
    """Fixture that provides an assigner instance with sample data."""
    assigner = AdvancedCharacterAssignment()
    assigner.people_choices = sample_data
    assigner.all_characters = list(
        set(char for chars in sample_data.values() for char in chars)
    )
    return assigner


def test_init(empty_assigner):
    """Test class initialization."""
    assert empty_assigner.people_choices == {}
    assert empty_assigner.all_characters == []
    assert empty_assigner.conflict_analysis is None
    assert len(empty_assigner.available_strategies) > 0
    assert all(isinstance(s, str) for s in empty_assigner.available_strategies)


def test_analyze_conflicts(populated_assigner):
    """Test conflict analysis."""
    analysis = populated_assigner.analyze_conflicts()

    # Test basic structure
    assert isinstance(analysis, dict)
    assert "n_people" in analysis
    assert "n_characters" in analysis
    assert "popular_characters" in analysis
    assert "conflict_characters" in analysis
    assert "critical_characters" in analysis
    assert "at_risk_people" in analysis
    assert "unrequested_characters" in analysis
    assert "avg_preferences" in analysis
    assert "suggestions" in analysis

    # Test values
    assert analysis["n_people"] == 4
    assert analysis["n_characters"] == 4
    assert isinstance(analysis["avg_preferences"], float)
    assert analysis["avg_preferences"] == 3.0  # Each person has exactly 3 preferences

    # Test popular characters
    assert isinstance(analysis["popular_characters"], dict)
    assert "Character2" in analysis["popular_characters"]
    assert analysis["popular_characters"]["Character2"] == 3  # Most requested character

    # Test suggestions
    assert isinstance(analysis["suggestions"], list)
    assert len(analysis["suggestions"]) > 0
    assert all(isinstance(s, str) for s in analysis["suggestions"])


def test_empty_conflict_analysis(empty_assigner):
    """Test conflict analysis with empty data."""
    analysis = empty_assigner.analyze_conflicts()
    assert "error" in analysis
    assert analysis["error"] == "No data loaded"


def test_load_from_csv_wide_format():
    """Test loading from CSV in wide format."""
    assigner = AdvancedCharacterAssignment()

    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("Person,Pref1,Pref2,Pref3\n")
        f.write("Alice,Character1,Character2,Character3\n")
        f.write("Bob,Character2,Character3,\n")
        f.write("Charlie,,Character1,\n")  # Test empty preferences
        temp_path = f.name

    try:
        assigner.load_from_csv(temp_path, formato="wide")

        assert len(assigner.people_choices) == 3
        assert len(assigner.all_characters) == 3
        assert "Alice" in assigner.people_choices
        assert "Bob" in assigner.people_choices
        assert "Charlie" in assigner.people_choices
        assert len(assigner.people_choices["Alice"]) == 3
        assert len(assigner.people_choices["Bob"]) == 2
        assert len(assigner.people_choices["Charlie"]) == 1
        assert assigner.people_choices["Charlie"] == ["Character1"]
    finally:
        os.unlink(temp_path)


def test_load_from_csv_long_format():
    """Test loading from CSV in long format."""
    assigner = AdvancedCharacterAssignment()

    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("Person,Character\n")
        f.write("Alice,Character1\n")
        f.write("Alice,Character2\n")
        f.write("Bob,Character2\n")
        f.write("Charlie,\n")  # Test empty preference
        temp_path = f.name

    try:
        assigner.load_from_csv(temp_path, formato="long")

        assert (
            len(assigner.people_choices) == 2
        )  # Charlie should be excluded (no valid preferences)
        assert len(assigner.all_characters) == 2
        assert "Alice" in assigner.people_choices
        assert "Bob" in assigner.people_choices
        assert len(assigner.people_choices["Alice"]) == 2
        assert len(assigner.people_choices["Bob"]) == 1
        assert "Character1" in assigner.people_choices["Alice"]
        assert "Character2" in assigner.people_choices["Alice"]
        assert "Character2" in assigner.people_choices["Bob"]
    finally:
        os.unlink(temp_path)


def test_load_from_csv_file_not_found():
    """Test that loading a non-existent file raises FileNotFoundError."""
    assigner = AdvancedCharacterAssignment()
    with pytest.raises(FileNotFoundError):
        assigner.load_from_csv("/non/existent/path/file.csv")


def test_load_from_csv_invalid_format():
    """Test that an unsupported format string raises ValueError."""
    assigner = AdvancedCharacterAssignment()
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("Person,Pref1\nAlice,Character1\n")
        temp_path = f.name
    try:
        with pytest.raises(ValueError, match="Unsupported format"):
            assigner.load_from_csv(temp_path, formato="invalid_format")
    finally:
        os.unlink(temp_path)


def test_load_from_csv_long_format_missing_column():
    """Test that a long-format CSV with only one column raises ValueError."""
    assigner = AdvancedCharacterAssignment()
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("Person\nAlice\nBob\n")
        temp_path = f.name
    try:
        with pytest.raises(ValueError, match="at least 2 columns"):
            assigner.load_from_csv(temp_path, formato="long")
    finally:
        os.unlink(temp_path)


def test_expand_preferences(populated_assigner):
    """Test intelligent preference expansion."""
    expanded = populated_assigner.expand_preferences()

    # Test structure
    assert len(expanded) == len(populated_assigner.people_choices)
    assert all(isinstance(person, str) for person in expanded.keys())
    assert all(isinstance(prefs, list) for prefs in expanded.values())

    # Test preference length and validity
    for preferences in expanded.values():
        assert len(preferences) >= 3  # Should have at least 3 preferences
        assert len(preferences) <= 4  # Should not exceed 4 preferences

        # Test that preferences are valid
        for pref in preferences:
            assert pref in populated_assigner.all_characters

        # Test that preferences are unique per person
        assert len(preferences) == len(set(preferences))


@pytest.mark.parametrize(
    "strategy", ["balanced", "priority_fair", "greedy_smart", "hybrid"]
)
def test_assign_with_strategy(populated_assigner, strategy):
    """Test assignment with each strategy individually."""
    assignment = populated_assigner.assign_with_strategy(strategy)

    # Test completeness
    assert len(assignment) == len(populated_assigner.people_choices), (
        f"Strategy '{strategy}' returned {len(assignment)} assignments "
        f"for {len(populated_assigner.people_choices)} people"
    )

    # Test uniqueness of assignments
    assigned_characters = list(assignment.values())
    assert len(assigned_characters) == len(
        set(assigned_characters)
    ), f"Strategy '{strategy}' assigned the same character to multiple people"

    # Test validity of assignments
    for person, character in assignment.items():
        assert (
            person in populated_assigner.people_choices
        ), f"Unknown person: {person}"
        assert (
            character in populated_assigner.all_characters
        ), f"Unknown character '{character}' assigned to '{person}'"


def test_assign_with_strategy_hungarian(populated_assigner):
    """Test Hungarian strategy only if scipy is available."""
    if not populated_assigner.SCIPY_AVAILABLE:
        pytest.skip("scipy not available")

    assignment = populated_assigner.assign_with_strategy("hungarian")

    assert len(assignment) == len(populated_assigner.people_choices)
    assigned_characters = list(assignment.values())
    assert len(assigned_characters) == len(set(assigned_characters))
    for person, character in assignment.items():
        assert person in populated_assigner.people_choices
        assert character in populated_assigner.all_characters


def test_assign_with_strategy_unknown_raises(populated_assigner):
    """Test that requesting an unknown strategy raises ValueError."""
    with pytest.raises(ValueError, match="Unknown strategy"):
        populated_assigner.assign_with_strategy("nonexistent_strategy")


def test_assign_with_strategy_no_data(empty_assigner):
    """Test that assigning with no data loaded raises ValueError."""
    with pytest.raises(ValueError, match="No data loaded"):
        empty_assigner.assign_with_strategy("greedy_smart")


def test_compare_strategies(populated_assigner):
    """Test strategy comparison."""
    results = populated_assigner.compare_strategies()

    # Test structure
    assert isinstance(results, dict)
    assert len(results) > 0

    # Test each strategy result
    for strategy, result in results.items():
        assert "assignment" in result
        assert "total_cost" in result
        assert "satisfied_preferences" in result
        assert "satisfaction_percentage" in result
        assert "details" in result

        # Test assignment result
        assignment = result["assignment"]
        assert len(assignment) == len(populated_assigner.people_choices)
        assert all(
            person in populated_assigner.people_choices for person in assignment
        )
        assert all(
            character in populated_assigner.all_characters
            for character in assignment.values()
        )

        # Test metrics
        assert isinstance(result["total_cost"], (int, float))
        assert isinstance(result["satisfied_preferences"], str)
        assert isinstance(result["satisfaction_percentage"], (int, float))
        assert 0 <= result["satisfaction_percentage"] <= 100


def test_find_best_strategy(populated_assigner):
    """Test finding the best strategy."""
    results = populated_assigner.compare_strategies()
    best = populated_assigner.find_best_strategy(results)

    # Test result
    assert best is not None
    assert best in populated_assigner.available_strategies

    # Test with empty results
    assert populated_assigner.find_best_strategy({}) == "hybrid"


def test_generate_text_report(populated_assigner):
    """Test text report generation."""
    # First make an assignment
    strategy = "greedy_smart"
    assignment = populated_assigner.assign_with_strategy(strategy)
    populated_assigner.analyze_conflicts()  # Ensure we have conflict analysis

    # Then generate report
    report = populated_assigner.generate_text_report(assignment, strategy)

    # Test report structure
    assert isinstance(report, str)
    assert len(report) > 0
    assert "CHARACTER ASSIGNMENT REPORT" in report
    assert strategy.upper() in report
    assert "GENERAL STATISTICS" in report
    assert "ASSIGNMENTS" in report
    assert "FINAL RESULTS" in report

    # Test content
    assert "Number of people" in report
    assert "Number of available characters" in report
    assert "Average preferences per person" in report
    assert "Satisfaction percentage" in report
    assert "Evaluation:" in report

    # Verify all people are mentioned
    for person in populated_assigner.people_choices:
        assert person in report


def test_create_character_pool(populated_assigner):
    """Test the character pool helper creates the correct number of slots."""
    n_people = len(populated_assigner.people_choices)
    pool = populated_assigner._create_character_pool(n_people)

    # Total slots must equal n_people
    assert sum(pool.values()) == n_people

    # All characters in pool must be valid
    for character in pool:
        assert character in populated_assigner.all_characters


def test_create_character_pool_empty_raises(empty_assigner):
    """Test that creating a pool with no characters raises ValueError."""
    with pytest.raises(ValueError, match="No characters available"):
        empty_assigner._create_character_pool(5)
