import json
import os
from logging_config import setup_logging
import logging

setup_logging(log_file="testing.log", error_log_file="testing_errors.log")

def diagnose_json(filepath):
    logging.info(f"Starting diagnosis for file: {filepath}")
    print("== DIAGNOZA PLIKU JSON ==\n")

    if not os.path.exists(filepath):
        logging.error(f"Error: File '{filepath}' does not exist.")
        print(f"Error: File '{filepath}' does not exist.")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict):
            logging.info("[VALID] Plik JSON zawiera obiekt (słownik).")
            print("[VALID] Plik JSON zawiera obiekt (słownik).")
        elif isinstance(data, list):
            logging.info(f"[VALID] Plik JSON zawiera listę z {len(data)} elementami.")
            print(f"[VALID] Plik JSON zawiera listę z {len(data)} elementami.")
        else:
            logging.info(f"[VALID] Plik JSON zawiera typ danych: {type(data).__name__}.")
            print(f"[VALID] Plik JSON zawiera typ danych: {type(data).__name__}.")
    except json.JSONDecodeError as e:
        logging.error(f"[ERROR] Błąd dekodowania JSON: {e}")
        print(f"[ERROR] Błąd dekodowania JSON: {e}")
    except Exception as e:
        logging.error(f"[ERROR] Wystąpił nieoczekiwany błąd: {e}")
        print(f"[ERROR] Wystąpił nieoczekiwany błąd: {e}")

# Przykład użycia:
diagnose_json("output/2000.json")