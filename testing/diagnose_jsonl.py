import json
import re
import os
from logging_config import setup_logging
import logging

setup_logging(log_file="testing.log", error_log_file="testing_errors.log")

def diagnose_jsonl(filepath):
    total = 0
    valid = 0
    partial = 0
    merged = 0
    unknown = 0
    print("== DIAGNOZA PLIKU ==\n")
    logging.info(f"Starting diagnosis for file: {filepath}")

    if not os.path.exists(filepath):
        logging.error(f"Error: File '{filepath}' does not exist.")
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
                logging.info(f"[PARTIAL] Linia {i}: wygląda na fragment obiektu")
                print(f"[PARTIAL] Linia {i}: wygląda na fragment obiektu")
                partial += 1
                continue

            # Czy złączone rekordy?
            if re.search(r'}\s*{', stripped):
                logging.info(f"[MERGED] Linia {i}: wygląda na złączone JSON-y")
                print(f"[MERGED] Linia {i}: wygląda na złączone JSON-y")
                merged += 1
                continue

            # Inne
            logging.info(f"[UNKNOWN] Linia {i}: nierozpoznana struktura")
            print(f"[UNKNOWN] Linia {i}: nierozpoznana struktura")
            print("   ", stripped[:100])
            unknown += 1

    logging.info(f"Diagnosis results for {filepath}")
    print("\n== PODSUMOWANIE ==")
    logging.info(f"  • Lines total: {total}")
    print(f"  • Łącznie linii:   {total}")
    logging.info(f"  • Valid JSONLs: {valid}")
    print(f"  • Poprawne JSONL-y: {valid}")
    logging.info(f"  • Partial JSONLs: {partial}")
    print(f"  • Fragmenty:       {partial}")
    logging.info(f"  • Merged JSONLs: {merged}")
    print(f"  • Złączone:        {merged}")
    logging.info(f"  • Unknown JSONLs: {unknown}")
    print(f"  • Nieznane:        {unknown}")

# Przykład użycia:
diagnose_jsonl("output/2022.jsonl")

