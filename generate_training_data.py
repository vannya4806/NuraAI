import json
import random
import string
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
random.seed(42)

with open(DATA_DIR / "drugs.json", encoding="utf-8") as f:
    DRUGS = json.load(f)

OCR_CONFUSION = {
    "o": "0", "0": "o", "l": "1", "1": "l", "i": "1",
    "s": "5", "b": "6", "g": "9", "z": "2", "e": "3",
}

DOSAGE_SUFFIXES = [" 500mg", " 10 mg", " 100MG", " (250mg)", " 5mg tablet", ""]

# Kata-kata acak (bukan nama obat) untuk mengajarkan model menolak teks yang tidak dikenal
UNKNOWN_SAMPLES = [
    "NOT FOR SALE", "KEEP OUT OF REACH OF CHILDREN", "EXP DATE 2027",
    "BATCH NO 12345", "MADE IN INDONESIA", "READ INSTRUCTION CAREFULLY",
    "STORE IN COOL DRY PLACE", "PRESCRIPTION ONLY", "REGISTERED TRADEMARK",
    "NOMOR IZIN EDAR", "KOMPOSISI PER TABLET", "CARA PAKAI", "PERHATIAN",
    "kertas kado ulang tahun", "meja kayu jati", "kucing tidur siang",
    "jadwal kereta api", "resep nasi goreng spesial", "cuaca cerah hari ini",
]


def inject_noise(text: str, noise_level: float = 0.15) -> str:
    """Ganti beberapa karakter dengan kemiripan visual (simulasi salah baca OCR)."""
    chars = list(text)
    for i, c in enumerate(chars):
        if c.lower() in OCR_CONFUSION and random.random() < noise_level:
            chars[i] = OCR_CONFUSION[c.lower()]
    return "".join(chars)


def random_case(text: str) -> str:
    choices = [text.upper(), text.lower(), text.title()]
    return random.choice(choices)


def generate_variants(base_name: str, n: int = 12) -> list[str]:
    variants = set()
    for _ in range(n):
        variant = base_name
        variant = random_case(variant)
        if random.random() < 0.5:
            variant = inject_noise(variant)
        if random.random() < 0.4:
            variant += random.choice(DOSAGE_SUFFIXES)
        variants.add(variant)
    return list(variants)


def build_dataset():
    rows = []  # (text, label)
    for drug_id, info in DRUGS.items():
        base_names = [info["nama_generik"]] + info["merk_dagang"]
        for name in base_names:
            for variant in generate_variants(name, n=15):
                rows.append((variant, drug_id))

    for phrase in UNKNOWN_SAMPLES:
        for variant in generate_variants(phrase, n=8):
            rows.append((variant, "unknown"))

    random.shuffle(rows)
    return rows


if __name__ == "__main__":
    dataset = build_dataset()
    print(f"Total data training: {len(dataset)} baris")
    print(f"Jumlah kelas: {len(set(label for _, label in dataset))}")
    print("\nContoh 10 baris pertama:")
    for text, label in dataset[:10]:
        print(f"  [{label:15s}] {text}")

    with open(DATA_DIR / "training_data.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"\nDisimpan ke {DATA_DIR / 'training_data.json'}")