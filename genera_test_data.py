import pandas as pd
import random
from datetime import datetime
import itertools

# Liste di nomi e cognomi italiani comuni
nomi = [
    "Alessandro", "Sofia", "Lorenzo", "Giulia", "Matteo", "Emma", "Leonardo", "Aurora",
    "Francesco", "Alice", "Giuseppe", "Martina", "Andrea", "Chiara", "Marco", "Sara",
    "Antonio", "Valentina", "Giovanni", "Beatrice", "Gabriele", "Francesca", "Davide",
    "Elena", "Nicola", "Maria", "Paolo", "Anna", "Luca", "Laura"
]

cognomi = [
    "Rossi", "Ferrari", "Russo", "Bianchi", "Romano", "Gallo", "Costa", "Fontana",
    "Conti", "Esposito", "Ricci", "Bruno", "De Luca", "Moretti", "Marino", "Greco",
    "Barbieri", "Lombardi", "Giordano", "Colombo", "Mancini", "Longo", "Leone", "Mariani",
    "Martinelli", "Rinaldi", "Vitale", "Serra", "Federici", "Caruso"
]

# Genera tutte le possibili combinazioni di nomi e cognomi
persone = []
for nome, cognome in itertools.product(nomi, cognomi):
    persone.append(f"{nome} {cognome}")

# Prendiamo 300 persone casuali
persone = random.sample(persone, 300)

# Lista di Pokemon popolari
pokemon = [
    "Pikachu", "Charizard", "Mewtwo", "Lucario", "Greninja", "Gardevoir", "Rayquaza",
    "Dragonite", "Gengar", "Metagross", "Gyarados", "Typhlosion", "Umbreon", "Sceptile",
    "Blaziken", "Darkrai", "Garchomp", "Zoroark", "Mimikyu", "Sylveon", "Dragapult",
    "Tyranitar", "Snorlax", "Blastoise", "Alakazam", "Arcanine", "Salamence", "Flygon",
    "Absol", "Luxray", "Scizor", "Milotic", "Haxorus", "Volcarona", "Hydreigon",
    "Aegislash", "Noivern", "Decidueye", "Chandelure", "Gallade"
]

# Assicurati che ci siano abbastanza Pokemon per tutte le persone
num_pokemon_necessari = len(persone) * 4
while len(pokemon) < num_pokemon_necessari:
    # Se non ci sono abbastanza Pokemon, duplica la lista aggiungendo un numero progressivo
    pokemon_extra = [f"{p} #{len(pokemon) // len(set(pokemon)) + 1}" for p in pokemon[:num_pokemon_necessari - len(pokemon)]]
    pokemon.extend(pokemon_extra)

# Genera dati casuali
data = []

for persona in persone:
    # Seleziona 4 Pokemon casuali diversi per ogni persona
    scelte = random.sample(pokemon, 4)
    data.append([persona] + scelte)

# Crea DataFrame
df = pd.DataFrame(data, columns=['Persona', 'Scelta1', 'Scelta2', 'Scelta3', 'Scelta4'])

# Genera nome file con timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f'test_data_{timestamp}.csv'

# Salva il CSV
df.to_csv(output_file, index=False)
print(f"✨ File di test generato: {output_file}")
print(f"📊 Numero di persone: {len(df)}")
print(f"🎮 Numero di personaggi unici: {len(pokemon)}")
