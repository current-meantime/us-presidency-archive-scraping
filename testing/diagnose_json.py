import json
import os

def diagnose_json(filepath):
    print("== DIAGNOZA PLIKU JSON ==\n")

    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' does not exist.")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict):
            print("[VALID] Plik JSON zawiera obiekt (słownik).")
        elif isinstance(data, list):
            print(f"[VALID] Plik JSON zawiera listę z {len(data)} elementami.")
        else:
            print(f"[VALID] Plik JSON zawiera typ danych: {type(data).__name__}.")
    except json.JSONDecodeError as e:
        print(f"[ERROR] Błąd dekodowania JSON: {e}")
    except Exception as e:
        print(f"[ERROR] Wystąpił nieoczekiwany błąd: {e}")

# Przykład użycia:
diagnose_json("output/2000.json")