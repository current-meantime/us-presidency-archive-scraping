import json
import re
import os

def diagnose_jsonl(filepath):
    total = 0
    valid = 0
    partial = 0
    merged = 0
    unknown = 0
    print("== DIAGNOZA PLIKU ==\n")

    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' does not exist.")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            total += 1
            stripped = line.strip()
            if not stripped:
                continue

            # Próba normalnego JSON-a
            try:
                obj = json.loads(stripped)
                if isinstance(obj, dict):
                    valid += 1
                    continue
            except json.JSONDecodeError:
                pass

            # Czy linia wygląda jak fragment (np. jedno pole)?
            if re.match(r'^"\w+":', stripped):
                print(f"[PARTIAL] Linia {i}: wygląda na fragment obiektu")
                partial += 1
                continue

            # Czy złączone rekordy?
            if re.search(r'}\s*{', stripped):
                print(f"[MERGED] Linia {i}: wygląda na złączone JSON-y")
                merged += 1
                continue

            # Inne
            print(f"[UNKNOWN] Linia {i}: nierozpoznana struktura")
            print("   ", stripped[:100])
            unknown += 1

    print("\n== PODSUMOWANIE ==")
    print(f"  • Łącznie linii:   {total}")
    print(f"  • Poprawne JSONL-y: {valid}")
    print(f"  • Fragmenty:       {partial}")
    print(f"  • Złączone:        {merged}")
    print(f"  • Nieznane:        {unknown}")

# Przykład użycia:
diagnose_jsonl("output/2022.jsonl")

