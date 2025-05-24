# BestCharacterAssigner

[![Dependencies Status](https://github.com/ehystiv/BestCharacterAssigner/actions/workflows/dependencies.yml/badge.svg)](https://github.com/ehystiv/BestCharacterAssigner/actions/workflows/dependencies.yml)
[![Code Coverage](https://github.com/ehystiv/BestCharacterAssigner/blob/main/coverage.svg)](https://github.com/ehystiv/BestCharacterAssigner/actions/workflows/coverage.yml)

An intelligent system for optimal character assignment to people, using various advanced strategies and algorithms to maximize global satisfaction.

## 🌟 Key Features

- **Multiple Assignment Strategies**:
  - Hungarian (mathematical optimization)
  - Balanced (popularity balancing)
  - Priority Fair (equitable priority)
  - Greedy Smart (intelligent greedy)
  - Hybrid (adaptive combination)

- **Advanced Analysis**:
  - Preventive conflict analysis
  - Automatic popularity balancing
  - Intelligent preference expansion
  - Input improvement suggestions

- **Data Format Support**:
  - "Wide" CSV format (one row per person)
  - "Long" CSV format (one row per preference)

- **Detailed Reports**:
  - Conflict analysis
  - Assignment statistics
  - Complete textual reports
  - Assignment quality evaluation

## 📋 Requirements

```bash
python >= 3.8
pandas
numpy
scipy (optional, for Hungarian algorithm)
```

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/ehystiv/BestCharacterAssigner.git
cd BestCharacterAssigner
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # For Linux/MacOS
# or
.\env\Scripts\activate  # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Command Line Interface

The program offers three main commands:

```bash
python main.py [command] [options]

Available commands:
  assign    Run character assignment
  test      Run tests
  evaluate  Evaluate which strategy is the best

Options for 'assign':
  preference_file        CSV file with preferences
  --format {wide,long}   CSV format (default: wide)
  --delimiter CHAR       CSV delimiter (default: ,)
  --strategy STRATEGY    Strategy to use (optional)

Options for 'test':
  -v, --verbose         Verbose output

Options for 'evaluate':
  preference_file        CSV file with preferences
  --format {wide,long}   CSV format (default: wide)
  --delimiter CHAR       CSV delimiter (default: ,)
```

Usage examples:
```bash
# Run character assignment
python main.py assign preferences.csv --format wide --delimiter ,

# Run tests in verbose mode
python main.py test -v

# Evaluate the best strategy
python main.py evaluate preferences.csv
```

### Data Format

#### "Wide" Format:
```csv
Person,Pref1,Pref2,Pref3
Alice,Character1,Character2,Character3
Bob,Character2,Character3,
```

#### "Long" Format:
```csv
Person,Character
Alice,Character1
Alice,Character2
Bob,Character2
```

## 🧪 Testing

The project includes a comprehensive test suite. To run the tests:

```bash
python main.py test -v
```

## 📊 Output Example

```
=== CONFLICT AND RISK ANALYSIS ===

📊 General Statistics:
   • People: 4
   • Characters: 4
   • Average preferences per person: 3.0

🔥 Most Requested Characters:
   • Character2: 3 people (75.0%)
   • Character3: 2 people (50.0%)
...

✨ FINAL RESULTS:
   • Total cost: 2
   • Preferences satisfied: 4/4 (100%)
   🎉 EXCELLENT Result!
```

## 🔧 Assignment Strategies

### Hungarian
Uses the Hungarian algorithm (Munkres) to find the optimal assignment by minimizing total cost.

### Balanced
Balances character popularity to avoid concentration on a few popular characters.

### Priority Fair
Prioritizes people with fewer available options to ensure fair assignment.

### Greedy Smart
Enhanced version of the greedy algorithm that considers urgency and availability.

### Hybrid
Combines different strategies and chooses the best one based on results.

## 📝 License

MIT License - See LICENSE file for details.

## 🤖 AI Development

This project was developed with the assistance of GitHub Copilot, an artificial intelligence system that contributed to:
- Implementation of assignment algorithms
- Code optimization
- Documentation generation
- Test suite creation

Human supervision was essential to ensure algorithm correctness and code quality.

## 👥 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ✨ Development Notes

- The Hungarian algorithm requires scipy
- Preferences are automatically expanded when needed
- The system can handle multiple copies of the same character if necessary
- Dependencies are automatically checked and updated weekly via GitHub Actions
- Security vulnerabilities in dependencies are automatically detected
