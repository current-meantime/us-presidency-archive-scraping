import json
import re
import os

def fix_fragmented_jsonl(input_path, output_path, broken_path=None):
    buffer = []
    fixed = 0
    skipped = 0
    line_num = 0  # Zmienna do śledzenia numeru linii w trakcie przetwarzania

    if broken_path is None:
        broken_path = output_path.replace(".jsonl", "_broken.jsonl")

    def try_parse_buffer(buf_lines):
        json_like = "{\n" + "\n".join(buf_lines) + "\n}"
        try:
            obj = json.loads(json_like)
            return obj
        except json.JSONDecodeError as e:
            # Dodajemy więcej informacji o błędzie
            print(f"Line {line_num} - JSON decode error: {e}")
            return None

    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile, \
         open(broken_path, 'w', encoding='utf-8') as brokenfile:

        for i, line in enumerate(infile, 1):
            line_num = i
            stripped = line.strip()
            
            # Logujemy każdą linię
            print(f"Processing Line {line_num}: {stripped[:100]}...")  # Wyświetlamy tylko pierwsze 100 znaków dla przeglądności
            
            # Ignorowanie pustych obiektów []{}
            if stripped == "[]{}" or not stripped:
                skipped += 1
                continue

            # Sprawdzamy, czy linia to fragment, który może być częścią obiektu JSON
            if re.match(r'^"\w+":', stripped):
                buffer.append(stripped)
            elif stripped in ('},', '}'):
                result = try_parse_buffer(buffer)
                if result is not None:
                    json.dump(result, outfile, ensure_ascii=False)
                    outfile.write("\n")
                    fixed += 1
                else:
                    # Jeśli nie udało się naprawić, zapisujemy całość jako błędną
                    brokenfile.write("{\n" + "\n".join(buffer) + "\n}\n---\n")
                    skipped += 1
                buffer = []
            elif stripped.startswith('{'):
                # Zaczynamy nowy obiekt
                buffer = []
            elif not stripped:
                continue
            else:
                # Zapisujemy inne linie, które nie pasują do wzorca
                brokenfile.write(line)
                skipped += 1
                buffer = []

    print("== NAPRAWA ZAKOŃCZONA ==")
    print(f"  • Naprawiono rekordów: {fixed}")
    print(f"  • Zapisano błędy do:   {os.path.basename(broken_path)}")
    print(f"  • Pominięto (błędy):   {skipped}")

# Przykład użycia:
fix_fragmented_jsonl(
    input_path="output/2024.jsonl",
    output_path="output/2024_fixed.jsonl"
)
