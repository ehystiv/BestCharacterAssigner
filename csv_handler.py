"""
Gestione dei file CSV per il sistema di assegnazione personaggi.

Questo modulo si occupa del caricamento e della gestione dei dati CSV
per il sistema di assegnazione dei personaggi.
"""
import pandas as pd
from typing import Dict, List, Tuple

class CSVHandler:
    """Classe per la gestione dei file CSV nel sistema di assegnazione."""
    
    @staticmethod
    def carica_da_csv(file_path: str, formato: str = 'wide', delimiter: str = ',') -> Tuple[Dict[str, List[str]], List[str]]:
        """
        Carica le preferenze da un file CSV.
        
        Args:
            file_path: Percorso del file CSV
            formato: 'wide' o 'long'. Nel formato 'wide' ogni riga è una persona e le colonne sono le preferenze.
                    Nel formato 'long' ogni riga è una coppia persona-personaggio.
            delimiter: Carattere separatore del CSV (default: virgola)
            
        Returns:
            Tuple[Dict[str, List[str]], List[str]]: Tupla contenente:
                - Dizionario delle preferenze {persona: [preferenze]}
                - Lista di tutti i personaggi unici
        """
        try:
            persone_scelte = {}
            
            if formato == 'wide':
                # Format wide: ogni riga è una persona, le colonne sono le preferenze
                df = pd.read_csv(file_path, delimiter=delimiter)
                
                # La prima colonna è il nome della persona
                persone = df.iloc[:, 0].tolist()
                
                # Le altre colonne sono le preferenze
                for i, persona in enumerate(persone):
                    # Prendi solo le preferenze non nulle
                    preferenze = [p for p in df.iloc[i, 1:].tolist() if pd.notna(p)]
                    if preferenze:  # Aggiungi solo se ha almeno una preferenza
                        persone_scelte[persona] = preferenze
                
            elif formato == 'long':
                # Format long: ogni riga è una coppia persona-personaggio
                df = pd.read_csv(file_path, delimiter=delimiter)
                
                if len(df.columns) < 2:
                    raise ValueError("Il formato 'long' richiede almeno 2 colonne: persona e personaggio")
                
                # Converti il formato long in dizionario
                for persona, gruppo in df.groupby(df.columns[0]):
                    # Prendi la seconda colonna come preferenza
                    preferenze = gruppo.iloc[:, 1].dropna().tolist()
                    if preferenze:  # Aggiungi solo se ha almeno una preferenza
                        persone_scelte[persona] = preferenze
            
            else:
                raise ValueError("Formato non supportato. Usa 'wide' o 'long'")
            
            # Raccogli tutti i personaggi unici
            tutti_personaggi = list(set(
                preferenza 
                for preferenze in persone_scelte.values() 
                for preferenza in preferenze
            ))
            
            print(f"✅ Caricamento completato:")
            print(f"   • {len(persone_scelte)} persone caricate")
            print(f"   • {len(tutti_personaggi)} personaggi unici trovati")
            
            return persone_scelte, tutti_personaggi
            
        except Exception as e:
            print(f"❌ Errore nel caricamento del CSV: {str(e)}")
            raise
    
    @staticmethod
    def salva_su_csv(assegnazioni: Dict[str, str], file_path: str, delimiter: str = ',') -> None:
        """
        Salva le assegnazioni finali su un file CSV.
        
        Args:
            assegnazioni: Dizionario delle assegnazioni {persona: personaggio}
            file_path: Percorso del file CSV da creare
            delimiter: Carattere separatore del CSV (default: virgola)
        """
        try:
            # Crea un DataFrame con le assegnazioni
            df = pd.DataFrame(
                [(persona, personaggio) for persona, personaggio in assegnazioni.items()],
                columns=['Persona', 'Personaggio Assegnato']
            )
            
            # Salva su CSV
            df.to_csv(file_path, index=False, delimiter=delimiter)
            
            print(f"✅ Assegnazioni salvate in: {file_path}")
            
        except Exception as e:
            print(f"❌ Errore nel salvataggio del CSV: {str(e)}")
            raise
