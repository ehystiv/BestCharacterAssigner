"""
Test suite for the AdvancedCharacterAssignment class.
"""

import pytest
import pandas as pd
import numpy as np
from advanced_assignment_strategies import AdvancedCharacterAssignment
import tempfile
import os
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
    assigner.persone_scelte = sample_data
    assigner.tutti_personaggi = list(
        set(char for chars in sample_data.values() for char in chars)
    )
    return assigner


def test_init(empty_assigner):
    """Test class initialization."""
    assert empty_assigner.persone_scelte == {}
    assert empty_assigner.tutti_personaggi == []
    assert empty_assigner.analisi_conflitti is None
    assert len(empty_assigner.strategie_disponibili) > 0
    assert all(isinstance(s, str) for s in empty_assigner.strategie_disponibili)


def test_analizza_conflitti(populated_assigner):
    """Test conflict analysis."""
    analisi = populated_assigner.analizza_conflitti()

    # Test basic structure
    assert isinstance(analisi, dict)
    assert "n_persone" in analisi
    assert "n_personaggi" in analisi
    assert "personaggi_popolari" in analisi
    assert "personaggi_conflitto" in analisi
    assert "personaggi_critici" in analisi
    assert "persone_rischio" in analisi
    assert "personaggi_non_richiesti" in analisi
    assert "media_preferenze" in analisi
    assert "suggerimenti" in analisi

    # Test values
    assert analisi["n_persone"] == 4
    assert analisi["n_personaggi"] == 4
    assert isinstance(analisi["media_preferenze"], float)
    assert analisi["media_preferenze"] == 3.0  # Each person has exactly 3 preferences

    # Test popular characters
    assert isinstance(analisi["personaggi_popolari"], dict)
    assert "Character2" in analisi["personaggi_popolari"]
    assert analisi["personaggi_popolari"]["Character2"] == 3  # Most requested character

    # Test suggestions
    assert isinstance(analisi["suggerimenti"], list)
    assert len(analisi["suggerimenti"]) > 0
    assert all(isinstance(s, str) for s in analisi["suggerimenti"])


def test_empty_conflict_analysis(empty_assigner):
    """Test conflict analysis with empty data."""
    analysis = empty_assigner.analizza_conflitti()
    assert "errore" in analysis
    assert analysis["errore"] == "Nessun dato caricato"


def test_carica_da_csv_wide_format():
    """Test loading from CSV in wide format."""
    assigner = AdvancedCharacterAssignment()

    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("Person,Pref1,Pref2,Pref3\n")
        f.write("Alice,Character1,Character2,Character3\n")
        f.write("Bob,Character2,Character3,\n")
        f.write("Charlie,,Character1,\n")  # Test empty preferences
        temp_path = f.name

    try:
        assigner.carica_da_csv(temp_path, formato="wide")

        assert len(assigner.persone_scelte) == 3
        assert len(assigner.tutti_personaggi) == 3
        assert "Alice" in assigner.persone_scelte
        assert "Bob" in assigner.persone_scelte
        assert "Charlie" in assigner.persone_scelte
        assert len(assigner.persone_scelte["Alice"]) == 3
        assert len(assigner.persone_scelte["Bob"]) == 2
        assert len(assigner.persone_scelte["Charlie"]) == 1
        assert assigner.persone_scelte["Charlie"] == ["Character1"]
    finally:
        os.unlink(temp_path)


def test_carica_da_csv_long_format():
    """Test loading from CSV in long format."""
    assigner = AdvancedCharacterAssignment()

    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("Person,Character\n")
        f.write("Alice,Character1\n")
        f.write("Alice,Character2\n")
        f.write("Bob,Character2\n")
        f.write("Charlie,\n")  # Test empty preference
        temp_path = f.name

    try:
        assigner.carica_da_csv(temp_path, formato="long")

        assert (
            len(assigner.persone_scelte) == 2
        )  # Charlie should be excluded (no valid preferences)
        assert len(assigner.tutti_personaggi) == 2
        assert "Alice" in assigner.persone_scelte
        assert "Bob" in assigner.persone_scelte
        assert len(assigner.persone_scelte["Alice"]) == 2
        assert len(assigner.persone_scelte["Bob"]) == 1
        assert "Character1" in assigner.persone_scelte["Alice"]
        assert "Character2" in assigner.persone_scelte["Alice"]
        assert "Character2" in assigner.persone_scelte["Bob"]
    finally:
        os.unlink(temp_path)


def test_espandi_preferenze_intelligente(populated_assigner):
    """Test intelligent preference expansion."""
    preferenze_espanse = populated_assigner.espandi_preferenze_intelligente()

    # Test structure
    assert len(preferenze_espanse) == len(populated_assigner.persone_scelte)
    assert all(isinstance(person, str) for person in preferenze_espanse.keys())
    assert all(isinstance(prefs, list) for prefs in preferenze_espanse.values())

    # Test preference length and validity
    for preferenze in preferenze_espanse.values():
        assert len(preferenze) >= 3  # Should have at least 3 preferences
        assert len(preferenze) <= 4  # Should not exceed 4 preferences

        # Test that preferences are valid
        for pref in preferenze:
            assert pref in populated_assigner.tutti_personaggi

        # Test that preferences are unique per person
        assert len(preferenze) == len(set(preferenze))


def test_assegna_con_strategia(populated_assigner):
    """Test assignment with different strategies."""
    for strategia in populated_assigner.strategie_disponibili:
        if strategia == "hungarian" and not populated_assigner.SCIPY_AVAILABLE:
            continue

        assegnazione = populated_assigner.assegna_con_strategia(strategia)

        # Test completeness
        assert len(assegnazione) == len(populated_assigner.persone_scelte)

        # Test uniqueness of assignments
        personaggi_assegnati = list(assegnazione.values())
        assert len(personaggi_assegnati) == len(set(personaggi_assegnati))

        # Test validity of assignments
        for persona, personaggio in assegnazione.items():
            # Test person exists
            assert persona in populated_assigner.persone_scelte
            # Test character exists
            assert personaggio in populated_assigner.tutti_personaggi


def test_confronta_strategie(populated_assigner):
    """Test strategy comparison."""
    risultati = populated_assigner.confronta_strategie()

    # Test structure
    assert isinstance(risultati, dict)
    assert len(risultati) > 0

    # Test each strategy result
    for strategia, risultato in risultati.items():
        assert "assegnazione" in risultato
        assert "costo_totale" in risultato
        assert "preferenze_soddisfatte" in risultato
        assert "percentuale_soddisfazione" in risultato
        assert "dettagli" in risultato

        # Test assignment result
        assegnazione = risultato["assegnazione"]
        assert len(assegnazione) == len(populated_assigner.persone_scelte)
        assert all(
            persona in populated_assigner.persone_scelte for persona in assegnazione
        )
        assert all(
            personaggio in populated_assigner.tutti_personaggi
            for personaggio in assegnazione.values()
        )

        # Test metrics
        assert isinstance(risultato["costo_totale"], (int, float))
        assert isinstance(risultato["preferenze_soddisfatte"], str)
        assert isinstance(risultato["percentuale_soddisfazione"], (int, float))
        assert 0 <= risultato["percentuale_soddisfazione"] <= 100


def test_trova_migliore_strategia(populated_assigner):
    """Test finding the best strategy."""
    risultati = populated_assigner.confronta_strategie()
    migliore = populated_assigner.trova_migliore_strategia(risultati)

    # Test result
    assert migliore is not None
    assert migliore in populated_assigner.strategie_disponibili

    # Test with empty results
    assert populated_assigner.trova_migliore_strategia({}) == "hybrid"


def test_genera_report_testuale(populated_assigner):
    """Test text report generation."""
    # First make an assignment
    strategia = "greedy_smart"
    assegnazione = populated_assigner.assegna_con_strategia(strategia)
    populated_assigner.analizza_conflitti()  # Ensure we have conflict analysis

    # Then generate report
    report = populated_assigner.genera_report_testuale(assegnazione, strategia)

    # Test report structure
    assert isinstance(report, str)
    assert len(report) > 0
    assert "CHARACTER ASSIGNMENT REPORT" in report
    assert strategia.upper() in report
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
    for persona in populated_assigner.persone_scelte:
        assert persona in report
