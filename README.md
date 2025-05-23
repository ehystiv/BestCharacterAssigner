# Sistema Avanzato di Assegnazione Personaggi

Un sistema intelligente per l'assegnazione ottimale di personaggi a persone, utilizzando diverse strategie e algoritmi avanzati per massimizzare la soddisfazione globale.

## 🌟 Caratteristiche Principali

- **Multiple Strategie di Assegnazione**:
  - Hungarian (ottimizzazione matematica)
  - Balanced (bilanciamento popolarità)
  - Priority Fair (priorità equa)
  - Greedy Smart (greedy intelligente)
  - Hybrid (combinazione adattiva)

- **Analisi Avanzata**:
  - Analisi preventiva dei conflitti
  - Bilanciamento automatico della popolarità
  - Espansione intelligente delle preferenze
  - Suggerimenti per migliorare l'input

- **Supporto Formati Dati**:
  - CSV formato "wide" (una riga per persona)
  - CSV formato "long" (una riga per preferenza)

- **Report Dettagliati**:
  - Analisi dei conflitti
  - Statistiche di assegnazione
  - Report testuali completi
  - Valutazione della qualità dell'assegnazione

## 📋 Requisiti

```bash
python >= 3.8
pandas
numpy
scipy (opzionale, per l'algoritmo Hungarian)
```

## 🚀 Installazione

1. Clona il repository:
```bash
git clone [url-repository]
cd CharAssign
```

2. Crea un ambiente virtuale e attivalo:
```bash
python -m venv env
source env/bin/activate  # Per Linux/MacOS
# oppure
.\env\Scripts\activate  # Per Windows
```

3. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

## 💻 Utilizzo

### Da Linea di Comando

```bash
python advanced_assignment_strategies.py file_preferenze.csv [opzioni]

Opzioni:
  --formato {wide,long}    Formato del CSV (default: wide)
  --delimiter CHAR         Carattere separatore CSV (default: ,)
  --strategia STRATEGIA   Strategia da utilizzare (opzionale)
```

### Formato dei Dati

#### Formato "Wide":
```csv
Persona,Pref1,Pref2,Pref3
Alice,Personaggio1,Personaggio2,Personaggio3
Bob,Personaggio2,Personaggio3,
```

#### Formato "Long":
```csv
Persona,Personaggio
Alice,Personaggio1
Alice,Personaggio2
Bob,Personaggio2
```

## 🧪 Test

Il progetto include una suite completa di test. Per eseguire i test:

```bash
pytest -v test_advanced_assignment_strategies.py
```

## 📊 Esempio di Output

```
=== ANALISI CONFLITTI E RISCHI ===

📊 Statistiche generali:
   • Persone: 4
   • Personaggi: 4
   • Media preferenze per persona: 3.0

🔥 Personaggi più richiesti:
   • Personaggio2: 3 persone (75.0%)
   • Personaggio3: 2 persone (50.0%)
...

✨ RISULTATI FINALI:
   • Costo totale: 2
   • Preferenze soddisfatte: 4/4 (100%)
   🎉 Risultato ECCELLENTE!
```

## 🔧 Strategie di Assegnazione

### Hungarian
Utilizza l'algoritmo ungherese (Munkres) per trovare l'assegnazione ottimale minimizzando il costo totale.

### Balanced
Bilancia la popolarità dei personaggi per evitare concentrazioni su pochi personaggi popolari.

### Priority Fair
Dà priorità alle persone con meno opzioni disponibili per garantire un'assegnazione equa.

### Greedy Smart
Versione migliorata dell'algoritmo greedy che considera l'urgenza e la disponibilità.

### Hybrid
Combina diverse strategie e sceglie la migliore basandosi sui risultati.

## 📝 Licenza

MIT License - Vedi il file LICENSE per i dettagli.

## 🤖 Sviluppo con AI

Questo progetto è stato sviluppato con l'assistenza di GitHub Copilot, un sistema di intelligenza artificiale che ha contribuito a:
- Implementazione degli algoritmi di assegnazione
- Ottimizzazione del codice
- Generazione della documentazione
- Creazione della suite di test

La supervisione umana è stata fondamentale per garantire la correttezza degli algoritmi e la qualità del codice.

## 👥 Contribuire

1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Committa i tuoi cambiamenti (`git commit -m 'Add some AmazingFeature'`)
4. Pusha sul branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## ✨ Note di Sviluppo

- L'algoritmo Hungarian richiede scipy
- Le preferenze vengono espanse automaticamente quando necessario
- Il sistema può gestire più copie dello stesso personaggio se necessario
