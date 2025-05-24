"""
Sistema Avanzato di Assegnazione con Strategie Multiple

Implementa diverse strategie per migliorare l'assegnazione di personaggi:
1. Analisi preventiva dei conflitti
2. Bilanciamento della popolarità
3. Espansione automatica delle preferenze
4. Algoritmi alternativi con priorità diverse
5. Suggerimenti per migliorare l'input

Autore: Assistente AI
Versione: 3.0 - Strategie Avanzate
"""

import numpy as np
import pandas as pd
from collections import Counter
import random
from typing import Dict, List, Set
from datetime import datetime

try:
    from scipy.optimize import linear_sum_assignment

    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


class AdvancedCharacterAssignment:
    """
    Sistema avanzato per l'assegnazione ottimale con strategie multiple.

    Features avanzate:
    - Analisi preventiva dei conflitti
    - Bilanciamento automatico della popolarità
    - Espansione intelligente delle preferenze
    - Multiple strategie di assegnazione
    - Suggerimenti per migliorare l'input
    """

    def __init__(self):
        self.persone_scelte = {}
        self.tutti_personaggi = []
        self.analisi_conflitti = None
        try:
            from scipy.optimize import linear_sum_assignment

            self.SCIPY_AVAILABLE = True
        except ImportError:
            self.SCIPY_AVAILABLE = False
        self.strategie_disponibili = [
            "hungarian",  # Algoritmo ungherese classico
            "balanced",  # Bilanciato per popolarità
            "priority_fair",  # Priorità ai meno fortunati
            "greedy_smart",  # Greedy intelligente
            "hybrid",  # Combinazione di strategie
        ]

    def analizza_conflitti(self) -> Dict:
        """
        Analizza preventivamente i potenziali conflitti nelle preferenze.

        Returns:
            dict: Analisi dettagliata con:
                - conflitti_personaggi: personaggi più richiesti
                - persone_rischio: persone con preferenze limitate
                - copertura_preferenze: statistiche di copertura
                - suggerimenti: raccomandazioni per migliorare
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

        # Identifica conflitti
        n_persone = len(self.persone_scelte)
        personaggi_conflitto = {
            p: count for p, count in popolarita.items() if count > 1
        }
        personaggi_critici = {
            p: count for p, count in popolarita.items() if count >= n_persone * 0.6
        }  # >60% lo vuole

        # Persone a rischio (poche preferenze in zone ad alto conflitto)
        persone_rischio = []
        for persona, preferenze in self.persone_scelte.items():
            if len(preferenze) <= 2:  # Poche preferenze
                conflitti_personali = sum(
                    1 for p in preferenze if p in personaggi_conflitto
                )
                if (
                    conflitti_personali >= len(preferenze) * 0.8
                ):  # >80% delle sue preferenze sono in conflitto
                    persone_rischio.append(
                        {
                            "persona": persona,
                            "preferenze": len(preferenze),
                            "conflitti": conflitti_personali,
                        }
                    )

        # Personaggi sottoutilizzati
        personaggi_disponibili = set(self.tutti_personaggi)
        personaggi_non_richiesti = personaggi_disponibili - set(popolarita.keys())

        # Suggerimenti
        suggerimenti = []

        if personaggi_critici:
            suggerimenti.append(
                f"⚠️ Personaggi molto richiesti: {', '.join(personaggi_critici.keys())}"
            )

        if persone_rischio:
            nomi = [p["persona"] for p in persone_rischio]
            suggerimenti.append(
                f"⚠️ Persone a rischio (poche preferenze): {', '.join(nomi)}"
            )

        if personaggi_non_richiesti:
            suggerimenti.append(
                f"💡 Personaggi mai richiesti: {', '.join(personaggi_non_richiesti)}"
            )
            suggerimenti.append("💡 Considera di rimuoverli o promuoverli")

        if len(self.tutti_personaggi) - len(self.persone_scelte) < 2:
            suggerimenti.append(
                "⚠️ Pochi personaggi di riserva, considera di aggiungerne altri"
            )

        self.analisi_conflitti = {
            "n_persone": n_persone,
            "n_personaggi": len(self.tutti_personaggi),
            "personaggi_popolari": dict(popolarita.most_common(5)),
            "personaggi_conflitto": personaggi_conflitto,
            "personaggi_critici": personaggi_critici,
            "persone_rischio": persone_rischio,
            "personaggi_non_richiesti": list(personaggi_non_richiesti),
            "media_preferenze": np.mean(list(lunghezze_preferenze.values())),
            "suggerimenti": suggerimenti,
        }

        return self.analisi_conflitti

    def stampa_analisi_conflitti(self):
        """Stampa l'analisi dei conflitti in formato leggibile."""
        if not self.analisi_conflitti:
            self.analizza_conflitti()

        analisi = self.analisi_conflitti

        print("=== ANALISI CONFLITTI E RISCHI ===\n")

        print(f"📊 Statistiche generali:")
        print(f"   • Persone: {analisi['n_persone']}")
        print(f"   • Personaggi: {analisi['n_personaggi']}")
        print(f"   • Media preferenze per persona: {analisi['media_preferenze']:.1f}")
        print()

        if analisi["personaggi_popolari"]:
            print("🔥 Personaggi più richiesti:")
            for personaggio, count in analisi["personaggi_popolari"].items():
                percentage = count / analisi["n_persone"] * 100
                print(f"   • {personaggio}: {count} persone ({percentage:.1f}%)")
            print()

        if analisi["personaggi_critici"]:
            print("⚠️ CONFLITTI CRITICI:")
            for personaggio, count in analisi["personaggi_critici"].items():
                print(f"   • {personaggio}: richiesto da {count} persone!")
            print()

        if analisi["persone_rischio"]:
            print("🚨 Persone a rischio di insoddisfazione:")
            for info in analisi["persone_rischio"]:
                print(
                    f"   • {info['persona']}: {info['preferenze']} preferenze, "
                    f"{info['conflitti']} in conflitto"
                )
            print()

        if analisi["personaggi_non_richiesti"]:
            print("😴 Personaggi mai richiesti:")
            print(f"   • {', '.join(analisi['personaggi_non_richiesti'])}")
            print()

        if analisi["suggerimenti"]:
            print("💡 SUGGERIMENTI:")
            for suggerimento in analisi["suggerimenti"]:
                print(f"   {suggerimento}")
            print()

    def espandi_preferenze_intelligente(
        self, metodo="similarità"
    ) -> Dict[str, List[str]]:
        """
        Espande automaticamente le preferenze per ridurre i conflitti.

        Args:
            metodo: 'similarità', 'popolarità', 'casuale', 'bilanciato'

        Returns:
            dict: Nuove preferenze espanse per ogni persona
        """
        if not self.analisi_conflitti:
            self.analizza_conflitti()

        preferenze_espanse = {}
        personaggi_disponibili = set(self.tutti_personaggi)

        for persona, preferenze_originali in self.persone_scelte.items():
            nuove_preferenze = preferenze_originali.copy()
            personaggi_usati = set(preferenze_originali)

            # Aggiungi fino a avere almeno 3-4 preferenze
            target_preferenze = min(4, len(self.tutti_personaggi))

            while len(nuove_preferenze) < target_preferenze:
                candidati = personaggi_disponibili - personaggi_usati
                if not candidati:
                    break

                if metodo == "popolarità":
                    # Aggiungi personaggi meno popolari
                    popolarita = self.analisi_conflitti["personaggi_popolari"]
                    candidato = min(candidati, key=lambda x: popolarita.get(x, 0))

                elif metodo == "similarità":
                    # Aggiungi personaggi richiesti da persone con preferenze simili
                    candidato = self._trova_personaggio_simile(persona, candidati)

                elif metodo == "bilanciato":
                    # Mix di popolarità e casualità
                    if random.random() < 0.7:  # 70% basato su popolarità
                        popolarita = self.analisi_conflitti["personaggi_popolari"]
                        candidato = min(candidati, key=lambda x: popolarita.get(x, 0))
                    else:  # 30% casuale
                        candidato = random.choice(list(candidati))

                else:  # casuale
                    candidato = random.choice(list(candidati))

                nuove_preferenze.append(candidato)
                personaggi_usati.add(candidato)

            preferenze_espanse[persona] = nuove_preferenze

        return preferenze_espanse

    def _trova_personaggio_simile(
        self, persona_target: str, candidati: Set[str]
    ) -> str:
        """Trova un personaggio basandosi su persone con preferenze simili."""
        preferenze_target = set(self.persone_scelte[persona_target])

        # Trova persone con preferenze simili
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

        # Trova personaggi usati da persone simili
        personaggi_suggeriti = Counter()
        for altra_persona, similarita in scores_similarita.items():
            if similarita > 0.3:  # Soglia di similarità
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
        Assegna personaggi usando la strategia specificata.

        Args:
            strategia: Nome della strategia da utilizzare
            espandi_preferenze: Se espandere automaticamente le preferenze

        Returns:
            dict: Assegnazioni {persona: personaggio}
        """
        if not self.persone_scelte:
            raise ValueError("Nessun dato caricato")

        # Analizza conflitti se non fatto
        if not self.analisi_conflitti:
            self.analizza_conflitti()

        # Espandi preferenze se richiesto
        preferenze_da_usare = self.persone_scelte
        if espandi_preferenze:
            print("🔧 Espandendo preferenze per ridurre conflitti...")
            preferenze_da_usare = self.espandi_preferenze_intelligente("bilanciato")
            print(f"   Preferenze espanse per {len(preferenze_da_usare)} persone")

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
        """Algoritmo ungherese classico."""
        if not SCIPY_AVAILABLE:
            print("⚠️ scipy non disponibile, uso greedy intelligente...")
            return self._assegna_greedy_intelligente(preferenze)

        import numpy as np

        persone = list(preferenze.keys())
        personaggi_originali = self.tutti_personaggi

        # Calcola quante copie di ogni personaggio servono
        n_persone = len(persone)
        n_personaggi = len(personaggi_originali)
        copie_necessarie = (n_persone + n_personaggi - 1) // n_personaggi

        # Replica i personaggi il numero necessario di volte
        personaggi = []
        for _ in range(copie_necessarie):
            personaggi.extend(personaggi_originali)

        # Taglia l'eccesso
        personaggi = personaggi[:n_persone]

        # Matrice costi
        costi = np.full(
            (n_persone, n_persone), 1000.0
        )  # Usa la stessa dimensione per righe e colonne

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
        """Strategia che bilancia la popolarità dei personaggi."""
        personaggi_originali = self.tutti_personaggi.copy()
        assegnazioni = {}
        popolarita = Counter()
        n_persone = len(preferenze)

        # Calcola quante copie di ogni personaggio servono
        copie_necessarie = (n_persone + len(personaggi_originali) - 1) // len(
            personaggi_originali
        )

        # Crea una lista di tutti i personaggi disponibili con copie
        personaggi_disponibili = []
        for _ in range(copie_necessarie):
            personaggi_disponibili.extend(personaggi_originali)
        personaggi_disponibili = personaggi_disponibili[:n_persone]

        # Conta popolarità
        for scelte in preferenze.values():
            for personaggio in scelte:
                popolarita[personaggio] += 1

        # Ordina persone: prima quelle con preferenze più rare
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

            # Cerca nelle preferenze, privilegiando quelle meno popolari
            scelte_ordinate = sorted(scelte, key=lambda x: popolarita[x])

            for personaggio in scelte_ordinate:
                if personaggio in personaggi_disponibili:
                    assegnazioni[persona] = personaggio
                    personaggi_disponibili.remove(personaggio)
                    assegnato = True
                    break

            # Assegnazione di emergenza
            if not assegnato and personaggi_disponibili:
                personaggio = personaggi_disponibili.pop(0)
                assegnazioni[persona] = personaggio

        return assegnazioni

    def _assegna_priorita_equa(
        self, preferenze: Dict[str, List[str]]
    ) -> Dict[str, str]:
        """Strategia che dà priorità a chi ha meno opzioni."""
        personaggi_originali = self.tutti_personaggi.copy()
        assegnazioni = {}
        n_persone = len(preferenze)

        # Calcola quante copie di ogni personaggio servono
        copie_necessarie = (n_persone + len(personaggi_originali) - 1) // len(
            personaggi_originali
        )

        # Crea pool di personaggi disponibili con copie
        personaggi_disponibili = []
        for _ in range(copie_necessarie):
            personaggi_disponibili.extend(personaggi_originali)
        personaggi_disponibili = personaggi_disponibili[:n_persone]

        # Ordina per numero di preferenze (poche prima)
        persone_ordinate = sorted(preferenze.keys(), key=lambda x: len(preferenze[x]))

        # Conta disponibilità per personaggio
        disponibilita = Counter(personaggi_disponibili)

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
                # Prendi il primo personaggio ancora disponibile
                for personaggio in personaggi_disponibili:
                    if disponibilita[personaggio] > 0:
                        assegnazioni[persona] = personaggio
                        disponibilita[personaggio] -= 1
                        break

        return assegnazioni

    def _assegna_greedy_intelligente(
        self, preferenze: Dict[str, List[str]]
    ) -> Dict[str, str]:
        """Versione migliorata dell'algoritmo greedy."""
        personaggi_originali = self.tutti_personaggi.copy()
        assegnazioni = {}
        n_persone = len(preferenze)

        # Calcola quante copie di ogni personaggio servono
        copie_necessarie = (n_persone + len(personaggi_originali) - 1) // len(
            personaggi_originali
        )

        # Crea pool di personaggi disponibili con copie
        personaggi_disponibili = []
        for _ in range(copie_necessarie):
            personaggi_disponibili.extend(personaggi_originali)
        personaggi_disponibili = personaggi_disponibili[:n_persone]

        # Conta disponibilità per personaggio
        disponibilita = Counter(personaggi_disponibili)

        # Calcola "urgenza" per ogni persona
        def calcola_urgenza(persona):
            scelte = preferenze[persona]
            disponibili = sum(1 for p in scelte if disponibilita[p] > 0)
            return disponibili  # Meno opzioni = più urgente

        # Processa in ordine di urgenza
        while len(assegnazioni) < len(preferenze):
            # Trova persona più urgente
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
                for personaggio in personaggi_disponibili:
                    if disponibilita[personaggio] > 0:
                        assegnazioni[persona_urgente] = personaggio
                        disponibilita[personaggio] -= 1
                        break

        return assegnazioni

    def _assegna_hybrid(self, preferenze: Dict[str, List[str]]) -> Dict[str, str]:
        """Strategia ibrida che combina più approcci."""
        # Prova più strategie e scegli la migliore
        strategie = ["hungarian", "balanced", "priority_fair", "greedy_smart"]
        risultati = []

        for strategia in strategie:
            if strategia == "hungarian" and not SCIPY_AVAILABLE:
                continue

            try:
                assegnazione = getattr(self, f'_assegna_{strategia.replace("_", "_")}')(
                    preferenze
                )
                punteggio = self._valuta_assegnazione(assegnazione, preferenze)
                risultati.append((strategia, assegnazione, punteggio))
            except:
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
        """Valuta la qualità di un'assegnazione."""
        punteggio_totale = 0
        preferenze_soddisfatte = 0

        for persona, personaggio in assegnazioni.items():
            scelte = preferenze[persona]
            if personaggio in scelte:
                posizione = scelte.index(personaggio)
                punteggio_totale += posizione  # 0 = meglio
                preferenze_soddisfatte += 1
            else:
                punteggio_totale += 10  # Penalità per non-preferenza

        # Bonus per alta percentuale di soddisfazione
        percentuale_soddisfatte = preferenze_soddisfatte / len(assegnazioni)
        punteggio_totale *= 2 - percentuale_soddisfatte  # Moltiplica per 1-2

        return punteggio_totale

    def confronta_strategie(self) -> Dict:
        """Confronta tutte le strategie disponibili."""
        if not self.persone_scelte:
            raise ValueError("Nessun dato caricato")

        risultati_confronto = {}

        print("🔍 Confrontando tutte le strategie...\n")

        for strategia in self.strategie_disponibili:
            if strategia == "hungarian" and not SCIPY_AVAILABLE:
                continue
            if strategia == "hybrid":  # Evita ricorsione
                continue

            try:
                assegnazione = self.assegna_con_strategia(
                    strategia, espandi_preferenze=False
                )

                # Calcola statistiche
                costo_totale = 0
                preferenze_soddisfatte = 0
                dettagli = []
                n_persone = len(self.persone_scelte)  # Numero totale di persone

                # Verifica che ci siano assegnazioni per tutte le persone
                if len(assegnazione) != n_persone:
                    raise ValueError(
                        f"Assegnazioni incomplete: {len(assegnazione)}/{n_persone} persone"
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
                        costo_totale += 1000
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
                print(f"❌ {strategia}: Errore - {e}")
                print()

        return risultati_confronto

    def carica_da_csv(
        self, file_path: str, formato: str = "wide", delimiter: str = ","
    ) -> None:
        """
        Carica le preferenze da un file CSV utilizzando CSVHandler.

        Args:
            file_path: Percorso del file CSV
            formato: 'wide' o 'long'. Nel formato 'wide' ogni riga è una persona e le colonne sono le preferenze.
                    Nel formato 'long' ogni riga è una coppia persona-personaggio.
            delimiter: Carattere separatore del CSV (default: virgola)
        """
        from csv_handler import CSVHandler

        try:
            self.persone_scelte, self.tutti_personaggi = CSVHandler.carica_da_csv(
                file_path, formato, delimiter
            )
            # Resetta l'analisi dei conflitti
            self.analisi_conflitti = None

        except Exception as e:
            print(f"❌ Errore nel caricamento del CSV: {str(e)}")
            raise

    def stampa_risultati_avanzati(self, assegnazioni: Dict[str, str]):
        """Versione avanzata della stampa risultati."""
        print("=== RISULTATI ASSEGNAZIONE AVANZATA ===\n")

        if self.analisi_conflitti:
            persone_rischio = {
                p["persona"] for p in self.analisi_conflitti["persone_rischio"]
            }
        else:
            persone_rischio = set()

        costo_totale = 0
        preferenze_soddisfatte = 0
        risultati_per_categoria = {
            "ottimi": [],
            "buoni": [],
            "accettabili": [],
            "problematici": [],
        }

        for persona, personaggio in assegnazioni.items():
            scelte = self.persone_scelte[persona]
            emoji_rischio = "🚨" if persona in persone_rischio else ""

            if personaggio in scelte:
                posizione = scelte.index(personaggio)
                costo_totale += posizione
                preferenze_soddisfatte += 1

                if posizione == 0:
                    categoria = "ottimi"
                    emoji = "🥇"
                elif posizione <= 1:
                    categoria = "buoni"
                    emoji = "🥈"
                else:
                    categoria = "accettabili"
                    emoji = "🥉"

                risultati_per_categoria[categoria].append(
                    f"{emoji} {persona}: {personaggio} (preferenza #{posizione+1}) {emoji_rischio}"
                )
            else:
                costo_totale += 1000
                risultati_per_categoria["problematici"].append(
                    f"😞 {persona}: {personaggio} (NON nelle preferenze) {emoji_rischio}"
                )

        # Stampa per categoria
        for categoria, risultati in risultati_per_categoria.items():
            if risultati:
                print(f"{categoria.upper()}:")
                for risultato in risultati:
                    print(f"  {risultato}")
                print()

        # Statistiche finali
        percentuale = preferenze_soddisfatte / len(assegnazioni) * 100
        print(f"📊 STATISTICHE FINALI:")
        print(f"   • Costo totale: {costo_totale}")
        print(
            f"   • Preferenze soddisfatte: {preferenze_soddisfatte}/{len(assegnazioni)} ({percentuale:.1f}%)"
        )

        if percentuale >= 90:
            print("   🎉 Risultato ECCELLENTE!")
        elif percentuale >= 75:
            print("   👍 Risultato BUONO")
        elif percentuale >= 50:
            print("   😐 Risultato ACCETTABILE")
        else:
            print("   😞 Risultato PROBLEMATICO - considera di rivedere le preferenze")

    def trova_migliore_strategia(self, risultati_confronto: Dict) -> str:
        """Trova la strategia migliore basandosi sui risultati del confronto."""
        if not risultati_confronto:
            return "hybrid"  # Default se non ci sono risultati

        # Trova la strategia con il miglior rapporto costo/soddisfazione
        migliore_strategia = None
        miglior_punteggio = float("inf")

        for strategia, risultato in risultati_confronto.items():
            costo = risultato["costo_totale"]
            percentuale = risultato["percentuale_soddisfazione"]

            # Calcola un punteggio ponderato (più basso = meglio)
            # Da più peso alla percentuale di soddisfazione
            punteggio = costo * (100 - percentuale)

            if punteggio < miglior_punteggio:
                miglior_punteggio = punteggio
                migliore_strategia = strategia

        return migliore_strategia

    def genera_report_testuale(
        self, assegnazioni: Dict[str, str], migliore_strategia: str
    ) -> str:
        """Genera un report testuale dettagliato dell'assegnazione."""
        report = []
        report.append("=== REPORT ASSEGNAZIONE PERSONAGGI ===")
        report.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        report.append(f"Strategia utilizzata: {migliore_strategia.upper()}\n")

        # Statistiche generali
        n_persone = len(self.persone_scelte)
        n_personaggi = len(self.tutti_personaggi)
        report.append("STATISTICHE GENERALI:")
        report.append(f"• Numero di persone: {n_persone}")
        report.append(f"• Numero di personaggi disponibili: {n_personaggi}")
        report.append(
            f"• Media preferenze per persona: {self.analisi_conflitti['media_preferenze']:.1f}\n"
        )

        # Risultati per persona
        report.append("ASSEGNAZIONI:")
        persone_ordinate = sorted(assegnazioni.keys())
        for persona in persone_ordinate:
            personaggio = assegnazioni[persona]
            scelte = self.persone_scelte[persona]
            if personaggio in scelte:
                posizione = scelte.index(personaggio) + 1
                report.append(f"• {persona}: {personaggio} (scelta #{posizione})")
            else:
                report.append(f"• {persona}: {personaggio} (non tra le preferenze)")

        # Statistiche di soddisfazione
        n_soddisfatti = sum(
            1 for p, c in assegnazioni.items() if c in self.persone_scelte[p]
        )
        perc_soddisfazione = (n_soddisfatti / n_persone) * 100

        report.append(f"\nRISULTATI FINALI:")
        report.append(
            f"• Persone che hanno ricevuto una delle loro scelte: {n_soddisfatti}/{n_persone}"
        )
        report.append(f"• Percentuale di soddisfazione: {perc_soddisfazione:.1f}%")

        # Valutazione finale
        if perc_soddisfazione >= 90:
            report.append("• Valutazione: ECCELLENTE")
        elif perc_soddisfazione >= 75:
            report.append("• Valutazione: BUONA")
        elif perc_soddisfazione >= 50:
            report.append("• Valutazione: ACCETTABILE")
        else:
            report.append("• Valutazione: PROBLEMATICA")

        return "\n".join(report)


def main():
    import argparse

    # Configura il parser degli argomenti
    parser = argparse.ArgumentParser(
        description="Sistema avanzato di assegnazione personaggi da file CSV"
    )
    parser.add_argument(
        "file_csv", help="Il file CSV contenente le preferenze (formato: wide o long)"
    )
    parser.add_argument(
        "--formato",
        choices=["wide", "long"],
        default="wide",
        help="Formato del CSV: wide (default) o long",
    )
    parser.add_argument(
        "--delimiter",
        default=",",
        help="Carattere separatore del CSV (default: virgola)",
    )
    parser.add_argument(
        "--strategia",
        choices=["hungarian", "balanced", "priority_fair", "greedy_smart", "hybrid"],
        help="Strategia da utilizzare per l'assegnazione. Se non specificata, verrà scelta la migliore",
    )

    # Parsing degli argomenti
    args = parser.parse_args()

    # Demo del sistema avanzato
    assegnatore = AdvancedCharacterAssignment()

    # Carica dati da CSV
    try:
        assegnatore.carica_da_csv(
            args.file_csv, formato=args.formato, delimiter=args.delimiter
        )
    except Exception as e:
        print(f"❌ Errore nel caricamento del CSV: {e}")
        exit(1)

    # Analisi conflitti
    assegnatore.stampa_analisi_conflitti()

    # Determina la strategia da utilizzare
    strategia_da_usare = args.strategia
    if not strategia_da_usare:
        # Confronta strategie e trova la migliore
        print("\n🔍 Confronto strategie per trovare la migliore...\n")
        risultati = assegnatore.confronta_strategie()
        strategia_da_usare = assegnatore.trova_migliore_strategia(risultati)
        print(f"\n✨ La strategia migliore è: {strategia_da_usare.upper()}\n")
    else:
        print(
            f"\n✨ Utilizzo della strategia specificata: {strategia_da_usare.upper()}\n"
        )

    # Usa la strategia con espansione delle preferenze
    print("🎯 Applicazione della strategia con espansione delle preferenze...\n")
    assegnazione_finale = assegnatore.assegna_con_strategia(
        strategia_da_usare, espandi_preferenze=True
    )
    assegnatore.stampa_risultati_avanzati(assegnazione_finale)

    # Genera e salva il report testuale con timestamp
    report = assegnatore.genera_report_testuale(assegnazione_finale, strategia_da_usare)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"assegnazione_report_{timestamp}.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n✨ Report salvato in: {report_file}")

    return assegnazione_finale


# Esempio di utilizzo avanzato
if __name__ == "__main__":
    main()
