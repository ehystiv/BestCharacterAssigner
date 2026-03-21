# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest test_advanced_assignment_strategies.py -v
# or via main.py
python main.py test -v

# Format code
black .

# Run character assignment (auto-selects best strategy)
python main.py assign preferences.csv

# Run with specific strategy
python main.py assign preferences.csv --strategy hungarian

# Evaluate which strategy is best without assigning
python main.py evaluate preferences.csv

# Generate test data
python generate_test_data.py
```

## Architecture

The project has three main modules:

**`advanced_assignment_strategies.py`** — Core logic. The `AdvancedCharacterAssignment` class holds all state and implements the assignment pipeline:
- `persone_scelte: Dict[str, List[str]]` — person → ordered preference list
- `tutti_personaggi: List[str]` — all unique characters (derived from preferences at load time)
- `analisi_conflitti: Dict` — cached result of conflict analysis (reset on each CSV load)

The assignment pipeline flows: load CSV → analyze conflicts → expand preferences → run strategy → score result.

**`csv_handler.py`** — `CSVHandler.carica_da_csv()` handles two CSV formats:
- `wide`: one row per person, preference columns (first column = person name)
- `long`: one row per person-character pair (two columns: person, character)

Returns `(persone_scelte, tutti_personaggi)` tuple. Characters not in any preference list won't appear in `tutti_personaggi`.

**`main.py`** — CLI entry point with three subcommands: `assign`, `test`, `evaluate`.

### Assignment strategies

Five strategies are implemented in `AdvancedCharacterAssignment`:

| Strategy | Description | Requires |
|---|---|---|
| `hungarian` | Scipy `linear_sum_assignment` on cost matrix | scipy + numpy |
| `balanced` | Assigns people with rarest preferences first, prioritizing less popular characters | — |
| `priority_fair` | Assigns people with fewest preferences first | — |
| `greedy_smart` | Iterates by urgency (fewest available options first) | — |
| `hybrid` | Runs all sub-strategies, picks the lowest-scoring result | — |

When scipy/numpy are unavailable, `hungarian` falls back to `greedy_smart`. The `hybrid` strategy excludes `hungarian` if scipy is absent.

**Scoring**: lower is better. `score = total_cost × (2 - satisfaction_rate)`. Assignment to a non-preferred character costs `PREFERENCE_PENALTY = 1000`.

**Character pool replication**: `_crea_pool_personaggi()` replicates the character list as many times as needed so there are always enough slots for all people.

**Preference expansion**: before assignment, `espandi_preferenze_intelligente()` pads each person's preference list to at least 3–4 entries using Jaccard similarity against other people's preferences.

## Code conventions

- All code and comments must be in **English**
- Use type hints for function parameters and return types
- Use snake_case naming throughout
- 4-space indentation
