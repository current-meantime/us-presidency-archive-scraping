import json
import os
import string
import re
from collections import Counter
from nltk.corpus import stopwords

# download stopwords i tokenizer
import nltk
nltk.download("stopwords")
nltk.download("punkt")

from nltk.tokenize import TweetTokenizer

# tokenizer, który radzi sobie ze skrótami, np. don't, he's itp.
tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)

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
    tokens = tokenizer.tokenize(text)
    # usuń tokeny będące czysto interpunkcyjne (np. ",", ".", "!", itp.)
    return [token for token in tokens if re.search(r"\w", token)]

def analyze_file(filename, hide_stopwords=False):
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
        word_list = normalize_text(text)
        word_count = len(word_list)
        char_count = len(text)

        word_counter.update(word_list)

        entry_stats.append({
            "word_count": word_count,
            "char_count": char_count
        })

        total_word_count += word_count
        total_char_count += char_count

    # filter stopwords if the option is enabled
    if hide_stopwords:
        stop_words = set(stopwords.words("english"))
        # get rid of single letters that maybe interpreted as words to count (e.g. "Q" for question in an interview)
        custom_stop_words = set(string.ascii_lowercase)
        stop_words.update(custom_stop_words)
        filtered_word_counter = Counter({word: count for word, count in word_counter.items() if word not in stop_words})
    else:
        filtered_word_counter = word_counter

    # prepare summary
    stats = {
        "filename": filename,
        "total_entries": f"{total_entries:,}",
        "total_word_count": f"{total_word_count:,}",
        "total_char_count": f"{total_char_count:,}",
        "average_words_per_entry": f"{total_word_count / total_entries:,.2f}" if total_entries else "0.00",
        "average_chars_per_entry": f"{total_char_count / total_entries:,.2f}" if total_entries else "0.00",
        "top_words": filtered_word_counter.most_common(100),
        "entry_stats": entry_stats  # optionally omit for smaller file
    }

    output_name = filename.replace(".jsonl", "").replace(".json", "_json") + "_analyzed"
    save_json(stats, output_name)

# przykład użycia:
analyze_file("2024.jsonl", True)
# analyze_file("2024.jsonl")
