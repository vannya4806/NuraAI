import json
from pathlib import Path
from rapidfuzz import fuzz, process
from text_utils import get_candidates

DATA_DIR = Path(__file__).parent / "data"

with open(DATA_DIR / "drugs.json", encoding="utf-8") as f:
    DRUGS = json.load(f)

# Bangun index: setiap alias -> drug_id, supaya pencarian lebih akurat
ALIAS_INDEX = {}
for drug_id, info in DRUGS.items():
    for alias in info["alias_ocr"]:
        ALIAS_INDEX[alias.lower()] = drug_id


def match_drug(raw_text: str, threshold: int = 70):
    """
    Cari obat yang paling cocok dari teks OCR.
    Menggunakan WRatio (lebih toleran terhadap kata tambahan / typo ringan
    dibanding token_sort_ratio biasa) dan mencoba tiap kandidat kata/frasa.
    Return: (drug_id, confidence_score) atau (None, 0) jika tidak ketemu.
    """
    candidates = get_candidates(raw_text)
    all_aliases = list(ALIAS_INDEX.keys())

    best_match = None
    best_score = 0

    for candidate in candidates:
        result = process.extractOne(
            candidate.lower(), all_aliases, scorer=fuzz.WRatio
        )
        if result:
            alias, score, _ = result
            if score > best_score:
                best_score = score
                best_match = alias

    if best_match and best_score >= threshold:
        return ALIAS_INDEX[best_match], best_score
    return None, 0


if __name__ == "__main__":
    import sys
    test_text = sys.argv[1] if len(sys.argv) > 1 else "AMBR0X0L HYDR0CHL0RIDE"
    drug_id, score = match_drug(test_text)
    print(f"Input: {test_text}")
    print(f"Hasil: {drug_id} (confidence: {score})")