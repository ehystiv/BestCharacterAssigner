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
    """Fixture che fornisce dati di esempio per i test."""
    return {
        "Alice": ["Personaggio1", "Personaggio2", "Personaggio3"],
        "Bob": ["Personaggio2", "Personaggio3", "Personaggio4"],
        "Charlie": ["Personaggio3", "Personaggio4", "Personaggio1"],
        "David": ["Personaggio4", "Personaggio1", "Personaggio2"],
    }


@pytest.fixture
def empty_assigner() -> AdvancedCharacterAssignment:
    """Fixture che fornisce un'istanza pulita dell'assegnatore."""
    return AdvancedCharacterAssignment()


@pytest.fixture
def populated_assigner(sample_data) -> AdvancedCharacterAssignment:
    """Fixture che fornisce un'istanza dell'assegnatore con dati di esempio."""
    assigner = AdvancedCharacterAssignment()
    assigner.persone_scelte = sample_data
    assigner.tutti_personaggi = list(
        set(char for chars in sample_data.values() for char in chars)
    )
    return assigner


def test_init(empty_assigner):
    """Test dell'inizializzazione della classe."""
    assert empty_assigner.persone_scelte == {}
    assert empty_assigner.tutti_personaggi == []
    assert empty_assigner.analisi_conflitti is None
    assert len(empty_assigner.strategie_disponibili) > 0


def test_analizza_conflitti(populated_assigner):
    """Test dell'analisi dei conflitti."""
    analisi = populated_assigner.analizza_conflitti()

    assert isinstance(analisi, dict)
    assert "n_persone" in analisi
    assert "n_personaggi" in analisi
    assert "personaggi_popolari" in analisi
    assert "suggerimenti" in analisi

    assert analisi["n_persone"] == 4
    assert analisi["n_personaggi"] == 4


def test_carica_da_csv_wide_format():
    """Test del caricamento da CSV in formato wide."""
    assigner = AdvancedCharacterAssignment()

    # Crea un file CSV temporaneo
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("Persona,Pref1,Pref2,Pref3\n")
        f.write("Alice,Personaggio1,Personaggio2,Personaggio3\n")
        f.write("Bob,Personaggio2,Personaggio3,\n")
        temp_path = f.name

    try:
        assigner.carica_da_csv(temp_path, formato="wide")

        assert len(assigner.persone_scelte) == 2
        assert len(assigner.tutti_personaggi) == 3
        assert "Alice" in assigner.persone_scelte
        assert len(assigner.persone_scelte["Alice"]) == 3
        assert len(assigner.persone_scelte["Bob"]) == 2
    finally:
        os.unlink(temp_path)


def test_carica_da_csv_long_format():
    """Test del caricamento da CSV in formato long."""
    assigner = AdvancedCharacterAssignment()

    # Crea un file CSV temporaneo
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("Persona,Personaggio\n")
        f.write("Alice,Personaggio1\n")
        f.write("Alice,Personaggio2\n")
        f.write("Bob,Personaggio2\n")
        temp_path = f.name

    try:
        assigner.carica_da_csv(temp_path, formato="long")

        assert len(assigner.persone_scelte) == 2
        assert len(assigner.tutti_personaggi) == 2
        assert "Alice" in assigner.persone_scelte
        assert len(assigner.persone_scelte["Alice"]) == 2
        assert len(assigner.persone_scelte["Bob"]) == 1
    finally:
        os.unlink(temp_path)


def test_espandi_preferenze_intelligente(populated_assigner):
    """Test dell'espansione intelligente delle preferenze."""
    preferenze_espanse = populated_assigner.espandi_preferenze_intelligente()

    assert len(preferenze_espanse) == len(populated_assigner.persone_scelte)

    # Verifica che tutte le persone abbiano almeno 3 preferenze
    for preferenze in preferenze_espanse.values():
        assert len(preferenze) >= 3

        # Verifica che le preferenze siano valide
        for pref in preferenze:
            assert pref in populated_assigner.tutti_personaggi


def test_assegna_con_strategia(populated_assigner):
    """Test dell'assegnazione con diverse strategie."""
    for strategia in populated_assigner.strategie_disponibili:
        if strategia == "hungarian" and not populated_assigner.SCIPY_AVAILABLE:
            continue

        assegnazione = populated_assigner.assegna_con_strategia(strategia)

        # Verifica che ci sia un'assegnazione per ogni persona
        assert len(assegnazione) == len(populated_assigner.persone_scelte)

        # Verifica che ogni personaggio sia assegnato al massimo una volta
        personaggi_assegnati = list(assegnazione.values())
        assert len(personaggi_assegnati) == len(set(personaggi_assegnati))

        # Verifica che tutti i personaggi assegnati siano validi
        for personaggio in assegnazione.values():
            assert personaggio in populated_assigner.tutti_personaggi


def test_confronta_strategie(populated_assigner):
    """Test del confronto tra strategie."""
    risultati = populated_assigner.confronta_strategie()

    assert isinstance(risultati, dict)
    assert len(risultati) > 0

    for strategia, risultato in risultati.items():
        assert "assegnazione" in risultato
        assert "costo_totale" in risultato
        assert "preferenze_soddisfatte" in risultato
        assert "percentuale_soddisfazione" in risultato


def test_trova_migliore_strategia(populated_assigner):
    """Test della selezione della migliore strategia."""
    risultati = populated_assigner.confronta_strategie()
    migliore = populated_assigner.trova_migliore_strategia(risultati)

    assert migliore is not None
    assert migliore in populated_assigner.strategie_disponibili


def test_genera_report_testuale(populated_assigner):
    """Test della generazione del report testuale."""
    # Prima esegue un'assegnazione
    strategia = "greedy_smart"
    assegnazione = populated_assigner.assegna_con_strategia(strategia)

    # Poi genera il report
    report = populated_assigner.genera_report_testuale(assegnazione, strategia)

    assert isinstance(report, str)
    assert len(report) > 0
    assert "REPORT ASSEGNAZIONE PERSONAGGI" in report
    assert strategia.upper() in report
    assert "STATISTICHE GENERALI" in report
    assert "ASSEGNAZIONI" in report
