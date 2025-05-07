import json
import os
import string
from collections import Counter

def save_json(data, name):
    output_dir = "file_analysis"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{name}.json")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved: {filepath}")
    except Exception as e:
        print(f"Error saving JSON file {name}: {e}")

def normalize_text(text):
    # lowercase, remove punctuation
    translator = str.maketrans("", "", string.punctuation)
    return text.lower().translate(translator)

def analyze_file(filename):
    filepath = os.path.join("output", filename)
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return

    # detect file format: JSONL or JSON array
    with open(filepath, "r", encoding="utf-8") as f:
        first_char = f.read(1)
        f.seek(0)
        if first_char == "[":
            try:
                entries = json.load(f)
            except json.JSONDecodeError as e:
                print(f"JSON decode error in {filename}: {e}")
                return
        else:
            entries = []
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"JSON decode error in {filename}, line {i}: {e}")

    total_entries = len(entries)
    total_word_count = 0
    total_char_count = 0
    word_counter = Counter()
    entry_stats = []

    for entry in entries:
        text = entry.get("text", "")
        word_list = normalize_text(text).split()
        word_count = len(word_list)
        char_count = len(text)

        word_counter.update(word_list)

        entry_stats.append({
            "word_count": word_count,
            "char_count": char_count
        })

        total_word_count += word_count
        total_char_count += char_count

    # prepare summary
    #TODO add number formatting for readability
    #TODO add option to hide stopwords ("the", "a", "of", etc.) in top_words
    stats = {
        "filename": filename,
        "total_entries": total_entries,
        "total_word_count": total_word_count,
        "total_char_count": total_char_count,
        "average_words_per_entry": total_word_count / total_entries if total_entries else 0,
        "average_chars_per_entry": total_char_count / total_entries if total_entries else 0,
        "top_words": word_counter.most_common(100),
        "entry_stats": entry_stats  # optionally omit for smaller file
    }

    output_name = filename.replace(".jsonl", "").replace(".json", "") + "_analyzed"
    save_json(stats, output_name)

# przykład użycia:
analyze_file("2000.jsonl")
# analyze_file("2024.jsonl")
