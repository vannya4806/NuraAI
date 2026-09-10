import re


def strip_dosage(text: str) -> str:
    """Buang angka dosis umum: '500mg', '10 mg', '(10mg)', dst."""
    return re.sub(r"\(?\d+\s?(mg|ml|mcg|g|tablet|kapsul)s?\)?", " ", text, flags=re.I)


def normalize_spaced_letters(text: str) -> str:
    """
    Gabungkan huruf tunggal yang terpisah spasi jadi satu kata.
    Kasus nyata: OCR kadang membaca "AMARYL" sebagai "A M A R Y L" karena
    kerning huruf pada kemasan terlalu lebar. Tanpa perbaikan ini, baik
    fuzzy matching maupun model ML sama-sama gagal karena pola karakter
    per-kata jadi rusak total.
    """
    pattern = r"(?:\b\w\b[ \t]+){2,}\b\w\b"

    def _merge(match: re.Match) -> str:
        return match.group(0).replace(" ", "").replace("\t", "")

    return re.sub(pattern, _merge, text)


def get_candidates(raw_text: str) -> list[str]:
    """
    Pipeline pembersihan lengkap: normalisasi huruf berspasi -> buang dosis
    -> pecah jadi baris & kata individual sebagai kandidat nama obat.
    """
    text = normalize_spaced_letters(raw_text)
    text = strip_dosage(text)

    lines = re.split(r"[\n,()]+", text)
    candidates = set()
    for line in lines:
        line = line.strip()
        if len(line) >= 3:
            candidates.add(line)
            for word in line.split():
                word = word.strip(".:;-")
                if len(word) >= 3:
                    candidates.add(word)
    return list(candidates) or [raw_text]