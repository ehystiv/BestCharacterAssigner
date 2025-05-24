import pandas as pd
import random
from datetime import datetime
import itertools
import sys

# Configuration parameters
NUM_PEOPLE = 300  # Number of people to generate
NUM_CHOICES = 4   # Number of choices per person

# Lists of common Italian names and surnames
first_names = [
    "Alessandro", "Sofia", "Lorenzo", "Giulia", "Matteo", "Emma", "Leonardo", "Aurora",
    "Francesco", "Alice", "Giuseppe", "Martina", "Andrea", "Chiara", "Marco", "Sara",
    "Antonio", "Valentina", "Giovanni", "Beatrice", "Gabriele", "Francesca", "Davide",
    "Elena", "Nicola", "Maria", "Paolo", "Anna", "Luca", "Laura"
]

last_names = [
    "Rossi", "Ferrari", "Russo", "Bianchi", "Romano", "Gallo", "Costa", "Fontana",
    "Conti", "Esposito", "Ricci", "Bruno", "De Luca", "Moretti", "Marino", "Greco",
    "Barbieri", "Lombardi", "Giordano", "Colombo", "Mancini", "Longo", "Leone", "Mariani",
    "Martinelli", "Rinaldi", "Vitale", "Serra", "Federici", "Caruso"
]

# Generate all possible combinations of names and surnames
people = []
for first_name, last_name in itertools.product(first_names, last_names):
    people.append(f"{first_name} {last_name}")

# Check if we have enough possible combinations
max_possible_people = len(first_names) * len(last_names)
if NUM_PEOPLE > max_possible_people:
    print(f"⚠️ Error: Requested {NUM_PEOPLE} people, but only {max_possible_people} combinations are possible")
    sys.exit(1)

# Take the specified number of random people
people = random.sample(people, NUM_PEOPLE)

# List of popular Pokemon
pokemon = [
    "Pikachu", "Charizard", "Mewtwo", "Lucario", "Greninja", "Gardevoir", "Rayquaza",
    "Dragonite", "Gengar", "Metagross", "Gyarados", "Typhlosion", "Umbreon", "Sceptile",
    "Blaziken", "Darkrai", "Garchomp", "Zoroark", "Mimikyu", "Sylveon", "Dragapult",
    "Tyranitar", "Snorlax", "Blastoise", "Alakazam", "Arcanine", "Salamence", "Flygon",
    "Absol", "Luxray", "Scizor", "Milotic", "Haxorus", "Volcarona", "Hydreigon",
    "Aegislash", "Noivern", "Decidueye", "Chandelure", "Gallade"
]

# Calculate how many Pokemon we need
needed_pokemon = NUM_PEOPLE * NUM_CHOICES

# Check if we have enough unique Pokemon
if len(pokemon) < NUM_PEOPLE:
    print(f"⚠️ Error: Not enough unique Pokemon ({len(pokemon)}) for the number of people ({NUM_PEOPLE})")
    print("Each person should have at least one unique Pokemon to make the assignment meaningful")
    sys.exit(1)

# Make sure there are enough Pokemon for all choices
while len(pokemon) < needed_pokemon:
    # If there aren't enough Pokemon, duplicate the list adding a progressive number
    extra_pokemon = [f"{p} #{len(pokemon) // len(set(pokemon)) + 1}" for p in pokemon[:needed_pokemon - len(pokemon)]]
    pokemon.extend(extra_pokemon)

# Generate random data
data = []

for person in people:
    # Select the specified number of different random Pokemon for each person
    choices = random.sample(pokemon, NUM_CHOICES)
    data.append([person] + choices)

# Create DataFrame
df = pd.DataFrame(data, columns=['Person', 'Choice1', 'Choice2', 'Choice3', 'Choice4'])

# Generate filename with timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f'test_data_{timestamp}.csv'

# Save the CSV
df.to_csv(output_file, index=False)
print(f"✨ Test file generated: {output_file}")
print(f"📊 Number of people: {len(df)}")
print(f"🎮 Number of unique characters: {len(pokemon)}")
