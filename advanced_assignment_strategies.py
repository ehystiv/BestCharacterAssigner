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
CONFLICT_THRESHOLD = 0.6     # Fraction of people requesting a character to flag it as critical
RISK_CONFLICT_RATIO = 0.8    # Fraction of a person's preferences in conflict to flag as at-risk
SIMILARITY_THRESHOLD = 0.3   # Minimum Jaccard similarity to suggest a character
BALANCED_RANDOM_RATIO = 0.7  # Probability of popularity-based choice in balanced expansion
PREFERENCE_PENALTY = 1000    # Cost penalty when assigned character is not in preferences

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
        self.persone_scelte = {}
        self.tutti_personaggi = []
        self.analisi_conflitti = None
        self.SCIPY_AVAILABLE = SCIPY_AVAILABLE
        self.strategie_disponibili = [
            "hungarian",      # Classic Hungarian algorithm
            "balanced",       # Balanced by popularity
            "priority_fair",  # Priority to less fortunate
            "greedy_smart",   # Smart greedy algorithm
            "hybrid",         # Combination of strategies
        ]

    def _crea_pool_personaggi(self, n_persone: int) -> Counter:
        """
        Create a Counter of available character slots, replicating as needed.

        Args:
            n_persone: Number of people to assign characters to

        Returns:
            Counter mapping character name to available slots
        """
        if not self.tutti_personaggi:
            raise ValueError("No characters available")
        n_personaggi = len(self.tutti_personaggi)
        copie_necessarie = (n_persone + n_personaggi - 1) // n_personaggi
        pool: List[str] = []
        for _ in range(copie_necessarie):
            pool.extend(self.tutti_personaggi)
        return Counter(pool[:n_persone])

    def analizza_conflitti(self) -> Dict:
        """
        Preemptively analyzes potential conflicts in preferences.

        Returns:
            dict: Detailed analysis with:
                - character_conflicts: most requested characters
                - people_at_risk: people with limited preferences
                - preference_coverage: coverage statistics
                - suggestions: improvement recommendations
        """
        if not self.persone_scelte:
            return {"errore": "Nessun dato caricato"}

        # Conta popolarità di ogni personaggio
        popolarita = Counter()
        lunghezze_preferenze = {}

        for persona, preferenze in self.persone_scelte.items():
            lunghezze_preferenze[persona] = len(preferenze)
            for personaggio in preferenze:
                popolarita[personaggio] += 1

        # Identify conflicts
        n_persone = len(self.persone_scelte)
        personaggi_conflitto = {
            p: count for p, count in popolarita.items() if count > 1
        }
        personaggi_critici = {
            p: count
            for p, count in popolarita.items()
            if count >= n_persone * CONFLICT_THRESHOLD
        }

        # Persone a rischio (poche preferenze in zone ad alto conflitto)
        persone_rischio = []
        for persona, preferenze in self.persone_scelte.items():
            if len(preferenze) <= 2:  # Few preferences
                conflitti_personali = sum(
                    1 for p in preferenze if p in personaggi_conflitto
                )
                if conflitti_personali >= len(preferenze) * RISK_CONFLICT_RATIO:
                    persone_rischio.append(
                        {
                            "persona": persona,
                            "preferenze": len(preferenze),
                            "conflitti": conflitti_personali,
                        }
                    )

        # Underutilized characters
        personaggi_set = set(self.tutti_personaggi)
        personaggi_non_richiesti = personaggi_set - set(popolarita.keys())

        # Suggestions
        suggerimenti = []

        if personaggi_critici:
            suggerimenti.append(
                f"⚠️ Highly requested characters: {', '.join(personaggi_critici.keys())}"
            )

        if persone_rischio:
            nomi = [p["persona"] for p in persone_rischio]
            suggerimenti.append(
                f"⚠️ People at risk (few preferences): {', '.join(nomi)}"
            )

        if personaggi_non_richiesti:
            suggerimenti.append(
                f"💡 Never requested characters: {', '.join(personaggi_non_richiesti)}"
            )
            suggerimenti.append("💡 Consider removing or promoting them")

        if len(self.tutti_personaggi) - len(self.persone_scelte) < 2:
            suggerimenti.append("⚠️ Few backup characters, consider adding more")

        pref_values = list(lunghezze_preferenze.values())
        media_preferenze = (
            float(np.mean(pref_values)) if NUMPY_AVAILABLE else float(statistics_mean(pref_values))
        )

        self.analisi_conflitti = {
            "n_persone": n_persone,
            "n_personaggi": len(self.tutti_personaggi),
            "personaggi_popolari": dict(popolarita.most_common(5)),
            "personaggi_conflitto": personaggi_conflitto,
            "personaggi_critici": personaggi_critici,
            "persone_rischio": persone_rischio,
            "personaggi_non_richiesti": list(personaggi_non_richiesti),
            "media_preferenze": media_preferenze,
            "suggerimenti": suggerimenti,
        }

        return self.analisi_conflitti

    def stampa_analisi_conflitti(self):
        """Print conflict analysis in readable format."""
        if not self.analisi_conflitti:
            self.analizza_conflitti()

        analisi = self.analisi_conflitti

        print("=== CONFLICT AND RISK ANALYSIS ===\n")

        print(f"📊 General statistics:")
        print(f"   • People: {analisi['n_persone']}")
        print(f"   • Characters: {analisi['n_personaggi']}")
        print(f"   • Average preferences per person: {analisi['media_preferenze']:.1f}")
        print()

        if analisi["personaggi_popolari"]:
            print("🔥 Most requested characters:")
            for personaggio, count in analisi["personaggi_popolari"].items():
                percentage = count / analisi["n_persone"] * 100
                print(f"   • {personaggio}: {count} people ({percentage:.1f}%)")
            print()

        if analisi["personaggi_critici"]:
            print("⚠️ CRITICAL CONFLICTS:")
            for personaggio, count in analisi["personaggi_critici"].items():
                print(f"   • {personaggio}: requested by {count} people!")
            print()

        if analisi["persone_rischio"]:
            print("🚨 People at risk of dissatisfaction:")
            for info in analisi["persone_rischio"]:
                print(
                    f"   • {info['persona']}: {info['preferenze']} preferences, "
                    f"{info['conflitti']} in conflict"
                )
            print()

        if analisi["personaggi_non_richiesti"]:
            print("😴 Never requested characters:")
            print(f"   • {', '.join(analisi['personaggi_non_richiesti'])}")
            print()

        if analisi["suggerimenti"]:
            print("💡 SUGGESTIONS:")
            for suggerimento in analisi["suggerimenti"]:
                print(f"   {suggerimento}")
            print()

    def espandi_preferenze_intelligente(
        self, metodo="similarità"
    ) -> Dict[str, List[str]]:
        """
        Automatically expands preferences to reduce conflicts.

        Args:
            metodo: 'similarità', 'popolarità', 'casuale', 'bilanciato'

        Returns:
            dict: New expanded preferences for each person
        """
        if not self.analisi_conflitti:
            self.analizza_conflitti()

        preferenze_espanse = {}
        personaggi_disponibili = set(self.tutti_personaggi)

        for persona, preferenze_originali in self.persone_scelte.items():
            nuove_preferenze = preferenze_originali.copy()
            personaggi_usati = set(preferenze_originali)

            # Add until we have at least 3-4 preferences
            target_preferenze = min(4, len(self.tutti_personaggi))

            while len(nuove_preferenze) < target_preferenze:
                candidati = personaggi_disponibili - personaggi_usati
                if not candidati:
                    break

                if metodo == "popolarità":
                    # Add less popular characters
                    popolarita = self.analisi_conflitti["personaggi_popolari"]
                    candidato = min(candidati, key=lambda x: popolarita.get(x, 0))

                elif metodo == "similarità":
                    # Add characters requested by people with similar preferences
                    candidato = self._trova_personaggio_simile(persona, candidati)

                elif metodo == "bilanciato":
                    # Mix of popularity and randomness
                    if random.random() < BALANCED_RANDOM_RATIO:
                        popolarita = self.analisi_conflitti["personaggi_popolari"]
                        candidato = min(candidati, key=lambda x: popolarita.get(x, 0))
                    else:
                        candidato = random.choice(list(candidati))

                else:  # random
                    candidato = random.choice(list(candidati))

                nuove_preferenze.append(candidato)
                personaggi_usati.add(candidato)

            preferenze_espanse[persona] = nuove_preferenze

        return preferenze_espanse

    def _trova_personaggio_simile(
        self, persona_target: str, candidati: Set[str]
    ) -> str:
        """Find a character based on people with similar preferences."""
        preferenze_target = set(self.persone_scelte[persona_target])

        # Find people with similar preferences
        scores_similarita = {}
        for altra_persona, altre_preferenze in self.persone_scelte.items():
            if altra_persona == persona_target:
                continue

            altre_pref_set = set(altre_preferenze)
            intersezione = len(preferenze_target & altre_pref_set)
            unione = len(preferenze_target | altre_pref_set)

            if unione > 0:
                similarita = intersezione / unione  # Jaccard similarity
                scores_similarita[altra_persona] = similarita

        # Find characters used by similar people
        personaggi_suggeriti = Counter()
        for altra_persona, similarita in scores_similarita.items():
            if similarita > SIMILARITY_THRESHOLD:
                for personaggio in self.persone_scelte[altra_persona]:
                    if personaggio in candidati:
                        personaggi_suggeriti[personaggio] += similarita

        if personaggi_suggeriti:
            return personaggi_suggeriti.most_common(1)[0][0]
        else:
            return random.choice(list(candidati))

    def assegna_con_strategia(
        self, strategia: str = "hybrid", espandi_preferenze: bool = True
    ) -> Dict[str, str]:
        """
        Assign characters using the specified strategy.

        Args:
            strategia: Name of the strategy to use
            espandi_preferenze: Whether to automatically expand preferences

        Returns:
            dict: Assignments {person: character}
        """
        if not self.persone_scelte:
            raise ValueError("Nessun dato caricato")

        # Analyze conflicts if not done
        if not self.analisi_conflitti:
            self.analizza_conflitti()

        # Expand preferences if requested
        preferenze_da_usare = self.persone_scelte
        if espandi_preferenze:
            print("🔧 Expanding preferences to reduce conflicts...")
            preferenze_da_usare = self.espandi_preferenze_intelligente("bilanciato")
            print(f"   Preferences expanded for {len(preferenze_da_usare)} people")

        # Esegui strategia scelta
        if strategia == "hungarian":
            return self._assegna_hungarian(preferenze_da_usare)
        elif strategia == "balanced":
            return self._assegna_bilanciato(preferenze_da_usare)
        elif strategia == "priority_fair":
            return self._assegna_priorita_equa(preferenze_da_usare)
        elif strategia == "greedy_smart":
            return self._assegna_greedy_intelligente(preferenze_da_usare)
        elif strategia == "hybrid":
            return self._assegna_hybrid(preferenze_da_usare)
        else:
            raise ValueError(f"Strategia sconosciuta: {strategia}")

    def _assegna_hungarian(self, preferenze: Dict[str, List[str]]) -> Dict[str, str]:
        """Classic Hungarian algorithm."""
        if not SCIPY_AVAILABLE:
            logger.warning("scipy not available, using smart greedy algorithm...")
            print("⚠️ scipy not available, using smart greedy algorithm...")
            return self._assegna_greedy_intelligente(preferenze)

        if not NUMPY_AVAILABLE:
            logger.warning("numpy not available, using smart greedy algorithm...")
            print("⚠️ numpy not available, using smart greedy algorithm...")
            return self._assegna_greedy_intelligente(preferenze)

        persone = list(preferenze.keys())
        personaggi_originali = self.tutti_personaggi

        # Calculate how many copies of each character are needed
        n_persone = len(persone)
        n_personaggi = len(personaggi_originali)
        copie_necessarie = (n_persone + n_personaggi - 1) // n_personaggi

        # Replicate characters the necessary number of times
        personaggi = []
        for _ in range(copie_necessarie):
            personaggi.extend(personaggi_originali)
        personaggi = personaggi[:n_persone]

        # Cost matrix: np.inf means impossible/undesired assignment
        costi = np.full((n_persone, n_persone), np.inf)

        for i, persona in enumerate(persone):
            scelte = preferenze[persona]
            for j, personaggio in enumerate(personaggi):
                if personaggio in scelte:
                    costi[i][j] = scelte.index(personaggio)

        # Risolvi
        indici_persone, indici_personaggi = linear_sum_assignment(costi)

        return {
            persone[i]: personaggi[j] for i, j in zip(indici_persone, indici_personaggi)
        }

    def _assegna_bilanciato(self, preferenze: Dict[str, List[str]]) -> Dict[str, str]:
        """Strategy that balances character popularity."""
        assegnazioni = {}
        n_persone = len(preferenze)

        # Count popularity
        popolarita = Counter()
        for scelte in preferenze.values():
            for personaggio in scelte:
                popolarita[personaggio] += 1

        # Available character pool via Counter (O(1) membership and removal)
        disponibilita = self._crea_pool_personaggi(n_persone)

        # Sort people: those with rarer preferences first
        def rarità_preferenze(persona):
            scelte = preferenze[persona]
            return (
                sum(popolarita[p] for p in scelte) / len(scelte)
                if scelte
                else float("inf")
            )

        persone_ordinate = sorted(preferenze.keys(), key=rarità_preferenze)

        for persona in persone_ordinate:
            scelte = preferenze[persona]
            assegnato = False

            # Search in preferences, prioritizing less popular ones
            scelte_ordinate = sorted(scelte, key=lambda x: popolarita[x])

            for personaggio in scelte_ordinate:
                if disponibilita[personaggio] > 0:
                    assegnazioni[persona] = personaggio
                    disponibilita[personaggio] -= 1
                    assegnato = True
                    break

            # Emergency assignment from remaining pool
            if not assegnato:
                for personaggio, count in disponibilita.items():
                    if count > 0:
                        assegnazioni[persona] = personaggio
                        disponibilita[personaggio] -= 1
                        break

        return assegnazioni

    def _assegna_priorita_equa(
        self, preferenze: Dict[str, List[str]]
    ) -> Dict[str, str]:
        """Strategy that gives priority to those with fewer options."""
        assegnazioni = {}
        n_persone = len(preferenze)

        # Available character pool via Counter
        disponibilita = self._crea_pool_personaggi(n_persone)

        # Sort by number of preferences (fewer first)
        persone_ordinate = sorted(preferenze.keys(), key=lambda x: len(preferenze[x]))

        for persona in persone_ordinate:
            scelte = preferenze[persona]
            assegnato = False

            # Prova tutte le preferenze
            for personaggio in scelte:
                if disponibilita[personaggio] > 0:
                    assegnazioni[persona] = personaggio
                    disponibilita[personaggio] -= 1
                    assegnato = True
                    break

            # Assegnazione casuale se necessario
            if not assegnato:
                for personaggio, count in disponibilita.items():
                    if count > 0:
                        assegnazioni[persona] = personaggio
                        disponibilita[personaggio] -= 1
                        break

        return assegnazioni

    def _assegna_greedy_intelligente(
        self, preferenze: Dict[str, List[str]]
    ) -> Dict[str, str]:
        """Improved version of the greedy algorithm."""
        assegnazioni = {}
        n_persone = len(preferenze)

        # Available character pool via Counter
        disponibilita = self._crea_pool_personaggi(n_persone)

        # Calculate "urgency" for each person
        def calcola_urgenza(persona):
            scelte = preferenze[persona]
            disponibili = sum(1 for p in scelte if disponibilita[p] > 0)
            return disponibili  # Fewer options = more urgent

        # Process in order of urgency
        while len(assegnazioni) < len(preferenze):
            # Find most urgent person
            persone_rimanenti = [p for p in preferenze.keys() if p not in assegnazioni]
            if not persone_rimanenti:
                break

            persona_urgente = min(persone_rimanenti, key=calcola_urgenza)
            scelte = preferenze[persona_urgente]

            # Assegna prima preferenza disponibile
            assegnato = False
            for personaggio in scelte:
                if disponibilita[personaggio] > 0:
                    assegnazioni[persona_urgente] = personaggio
                    disponibilita[personaggio] -= 1
                    assegnato = True
                    break

            # Se non ha preferenze disponibili, assegna il primo personaggio disponibile
            if not assegnato:
                for personaggio, count in disponibilita.items():
                    if count > 0:
                        assegnazioni[persona_urgente] = personaggio
                        disponibilita[personaggio] -= 1
                        break

        return assegnazioni

    def _assegna_hybrid(self, preferenze: Dict[str, List[str]]) -> Dict[str, str]:
        """Hybrid strategy that tests all sub-strategies and picks the best result."""
        # Explicit dispatch table mapping strategy names to their methods
        strategy_map = {
            "hungarian": self._assegna_hungarian,
            "balanced": self._assegna_bilanciato,
            "priority_fair": self._assegna_priorita_equa,
            "greedy_smart": self._assegna_greedy_intelligente,
        }
        risultati = []

        for strategia, fn in strategy_map.items():
            if strategia == "hungarian" and not SCIPY_AVAILABLE:
                continue

            try:
                assegnazione = fn(preferenze)
                punteggio = self._valuta_assegnazione(assegnazione, preferenze)
                risultati.append((strategia, assegnazione, punteggio))
            except Exception as e:
                logger.warning(f"Strategy '{strategia}' failed in hybrid: {e}")
                continue

        if not risultati:
            return self._assegna_greedy_intelligente(preferenze)

        # Scegli la migliore (punteggio più basso = meglio)
        migliore = min(risultati, key=lambda x: x[2])
        print(
            f"🎯 Strategia ibrida: usata '{migliore[0]}' (punteggio: {migliore[2]:.2f})"
        )

        return migliore[1]

    def _valuta_assegnazione(
        self, assegnazioni: Dict[str, str], preferenze: Dict[str, List[str]]
    ) -> float:
        """Evaluate the quality of an assignment."""
        punteggio_totale = 0
        preferenze_soddisfatte = 0

        for persona, personaggio in assegnazioni.items():
            scelte = preferenze[persona]
            if personaggio in scelte:
                posizione = scelte.index(personaggio)
                punteggio_totale += posizione  # 0 = better
                preferenze_soddisfatte += 1
            else:
                punteggio_totale += 10  # Penalty for non-preference

        # Bonus for high satisfaction percentage
        percentuale_soddisfatte = preferenze_soddisfatte / len(assegnazioni)
        punteggio_totale *= 2 - percentuale_soddisfatte  # Multiply by 1-2

        return punteggio_totale

    def confronta_strategie(self) -> Dict:
        """Compare all available strategies."""
        if not self.persone_scelte:
            raise ValueError("No data loaded")

        risultati_confronto = {}

        print("🔍 Comparing all strategies...\n")

        for strategia in self.strategie_disponibili:
            if strategia == "hungarian" and not SCIPY_AVAILABLE:
                continue
            if strategia == "hybrid":  # Evita ricorsione
                continue

            try:
                assegnazione = self.assegna_con_strategia(
                    strategia, espandi_preferenze=False
                )

                # Calculate statistics
                costo_totale = 0
                preferenze_soddisfatte = 0
                dettagli = []
                n_persone = len(self.persone_scelte)

                # Verify that there are assignments for all people
                if len(assegnazione) != n_persone:
                    raise ValueError(
                        f"Incomplete assignments: {len(assegnazione)}/{n_persone} people"
                    )

                for persona, personaggio in assegnazione.items():
                    scelte = self.persone_scelte[persona]
                    if personaggio in scelte:
                        posizione = scelte.index(personaggio)
                        costo_totale += posizione
                        preferenze_soddisfatte += 1
                        dettagli.append(
                            f"{persona}: {personaggio} (pref #{posizione+1})"
                        )
                    else:
                        costo_totale += PREFERENCE_PENALTY
                        dettagli.append(f"{persona}: {personaggio} (NON preferito)")

                percentuale = (preferenze_soddisfatte / n_persone) * 100

                risultati_confronto[strategia] = {
                    "assegnazione": assegnazione,
                    "costo_totale": costo_totale,
                    "preferenze_soddisfatte": f"{preferenze_soddisfatte}/{len(assegnazione)}",
                    "percentuale_soddisfazione": percentuale,
                    "dettagli": dettagli,
                }

                print(f"✅ {strategia.upper()}:")
                print(f"   Costo totale: {costo_totale}")
                print(
                    f"   Soddisfazione: {percentuale:.1f}% ({preferenze_soddisfatte}/{len(assegnazione)})"
                )
                print()

            except Exception as e:
                logger.error(f"Strategy '{strategia}' failed during comparison: {e}")
                print(f"❌ {strategia}: Errore - {e}")
                print()

        return risultati_confronto

    def carica_da_csv(
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
            self.persone_scelte, self.tutti_personaggi = CSVHandler.carica_da_csv(
                file_path, formato, delimiter
            )
            # Reset conflict analysis
            self.analisi_conflitti = None

        except Exception as e:
            print(f"❌ Error loading CSV: {str(e)}")
            raise

    def stampa_risultati_avanzati(self, assegnazioni: Dict[str, str]):
        """Advanced version of result printing."""
        print("=== ADVANCED ASSIGNMENT RESULTS ===\n")

        if self.analisi_conflitti:
            persone_rischio = {
                p["persona"] for p in self.analisi_conflitti["persone_rischio"]
            }
        else:
            persone_rischio = set()

        costo_totale = 0
        preferenze_soddisfatte = 0
        risultati_per_categoria = {
            "excellent": [],
            "good": [],
            "acceptable": [],
            "problematic": [],
        }

        for persona, personaggio in assegnazioni.items():
            scelte = self.persone_scelte[persona]
            emoji_rischio = "🚨" if persona in persone_rischio else ""

            if personaggio in scelte:
                posizione = scelte.index(personaggio)
                costo_totale += posizione
                preferenze_soddisfatte += 1

                if posizione == 0:
                    categoria = "excellent"
                    emoji = "🥇"
                elif posizione <= 1:
                    categoria = "good"
                    emoji = "🥈"
                else:
                    categoria = "acceptable"
                    emoji = "🥉"

                risultati_per_categoria[categoria].append(
                    f"{emoji} {persona}: {personaggio} (preference #{posizione+1}) {emoji_rischio}"
                )
            else:
                costo_totale += PREFERENCE_PENALTY
                risultati_per_categoria["problematic"].append(
                    f"😞 {persona}: {personaggio} (NOT in preferences) {emoji_rischio}"
                )

        # Print by category
        for categoria, risultati in risultati_per_categoria.items():
            if risultati:
                print(f"{categoria.upper()}:")
                for risultato in risultati:
                    print(f"  {risultato}")
                print()

        # Final statistics
        percentuale = preferenze_soddisfatte / len(assegnazioni) * 100
        print(f"📊 FINAL STATISTICS:")
        print(f"   • Total cost: {costo_totale}")
        print(
            f"   • Satisfied preferences: {preferenze_soddisfatte}/{len(assegnazioni)} ({percentuale:.1f}%)"
        )

        if percentuale >= 90:
            print("   🎉 EXCELLENT Result!")
        elif percentuale >= 75:
            print("   👍 GOOD Result")
        elif percentuale >= 50:
            print("   😐 ACCEPTABLE Result")
        else:
            print("   😞 PROBLEMATIC Result - consider revising preferences")

    def trova_migliore_strategia(self, risultati_confronto: Dict) -> str:
        """Find the best strategy based on comparison results."""
        if not risultati_confronto:
            return "hybrid"  # Default if no results

        # Find the strategy with the best cost/satisfaction ratio
        migliore_strategia = None
        miglior_punteggio = float("inf")

        for strategia, risultato in risultati_confronto.items():
            costo = risultato["costo_totale"]
            percentuale = risultato["percentuale_soddisfazione"]

            # Calculate a weighted score (lower = better)
            # Give more weight to satisfaction percentage
            punteggio = costo * (100 - percentuale)

            if punteggio < miglior_punteggio:
                miglior_punteggio = punteggio
                migliore_strategia = strategia

        return migliore_strategia

    def genera_report_testuale(
        self, assegnazioni: Dict[str, str], migliore_strategia: str
    ) -> str:
        """Generate a detailed text report of the assignment."""
        report = []
        report.append("=== CHARACTER ASSIGNMENT REPORT ===")
        report.append(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        report.append(f"Strategy used: {migliore_strategia.upper()}\n")

        # General statistics
        n_persone = len(self.persone_scelte)
        n_personaggi = len(self.tutti_personaggi)
        report.append("GENERAL STATISTICS:")
        report.append(f"• Number of people: {n_persone}")
        report.append(f"• Number of available characters: {n_personaggi}")
        report.append(
            f"• Average preferences per person: {self.analisi_conflitti['media_preferenze']:.1f}\n"
        )

        # Results by person
        report.append("ASSIGNMENTS:")
        persone_ordinate = sorted(assegnazioni.keys())
        for persona in persone_ordinate:
            personaggio = assegnazioni[persona]
            scelte = self.persone_scelte[persona]
            if personaggio in scelte:
                posizione = scelte.index(personaggio) + 1
                report.append(f"• {persona}: {personaggio} (choice #{posizione})")
            else:
                report.append(f"• {persona}: {personaggio} (not in preferences)")

        # Satisfaction statistics
        n_soddisfatti = sum(
            1 for p, c in assegnazioni.items() if c in self.persone_scelte[p]
        )
        perc_soddisfazione = (n_soddisfatti / n_persone) * 100

        report.append(f"\nFINAL RESULTS:")
        report.append(
            f"• People who received one of their choices: {n_soddisfatti}/{n_persone}"
        )
        report.append(f"• Satisfaction percentage: {perc_soddisfazione:.1f}%")

        # Final evaluation
        if perc_soddisfazione >= 90:
            report.append("• Evaluation: EXCELLENT")
        elif perc_soddisfazione >= 75:
            report.append("• Evaluation: GOOD")
        elif perc_soddisfazione >= 50:
            report.append("• Evaluation: ACCEPTABLE")
        else:
            report.append("• Evaluation: PROBLEMATIC")

        return "\n".join(report)
