import pytesseract
from PIL import Image, ImageFilter, ImageOps, ImageEnhance


def preprocess_image(image: Image.Image, scale: int = 3) -> Image.Image:
    """
    Preprocessing gambar agar OCR lebih akurat.

    Tahapan:
    1. Grayscale
    2. Upscale
    3. Autocontrast
    4. Sharpen
    5. Contrast enhancement
    """

    # Pastikan RGB
    image = image.convert("RGB")

    # Grayscale
    image = ImageOps.grayscale(image)

    # Upscale supaya teks kecil lebih mudah dibaca Tesseract
    width, height = image.size
    image = image.resize(
        (width * scale, height * scale),
        Image.Resampling.LANCZOS
    )

    # Perbaiki kontras
    image = ImageOps.autocontrast(image)

    # Tingkatkan contrast
    image = ImageEnhance.Contrast(image).enhance(1.5)

    # Sharpen
    image = image.filter(ImageFilter.SHARPEN)
    image = image.filter(ImageFilter.SHARPEN)

    return image


def _create_variants(image: Image.Image):
    """
    Membuat beberapa versi gambar untuk dicoba oleh Tesseract.
    """

    processed = preprocess_image(image)

    variants = []

    # 1. Grayscale + sharpen
    variants.append(("gray", processed))

    # 2. Threshold sederhana
    threshold = processed.point(
        lambda pixel: 255 if pixel > 170 else 0
    )
    variants.append(("threshold", threshold))

    # 3. Threshold lebih rendah
    threshold_dark = processed.point(
        lambda pixel: 255 if pixel > 130 else 0
    )
    variants.append(("threshold_dark", threshold_dark))

    # 4. Inverted threshold
    inverted = ImageOps.invert(threshold)
    variants.append(("inverted", inverted))

    return variants


def _ocr_image(image: Image.Image, psm: int, lang: str) -> tuple[str, float]:
    """
    Jalankan Tesseract dan mengembalikan:
    - teks hasil OCR
    - confidence rata-rata
    """

    config = f"--oem 3 --psm {psm}"

    # image_to_data memberi confidence setiap kata
    data = pytesseract.image_to_data(
        image,
        lang=lang,
        config=config,
        output_type=pytesseract.Output.DICT
    )

    words = []
    confidences = []

    for text, conf in zip(data["text"], data["conf"]):
        text = text.strip()

        if not text:
            continue

        try:
            confidence = float(conf)
        except (ValueError, TypeError):
            continue

        if confidence >= 0:
            words.append(text)
            confidences.append(confidence)

    result = " ".join(words).strip()

    if confidences:
        avg_confidence = sum(confidences) / len(confidences)
    else:
        avg_confidence = 0.0

    return result, avg_confidence


def extract_text(image_path: str, lang: str = "eng+ind") -> str:
    """
    Ambil teks mentah dari gambar kemasan obat.

    Beberapa preprocessing dan konfigurasi Tesseract dicoba,
    kemudian hasil terbaik dipilih.
    """

    image = Image.open(image_path)

    variants = _create_variants(image)

    # PSM 11 cocok untuk gambar yang memiliki banyak blok teks
    # PSM 6 cocok untuk blok teks yang relatif teratur
    # PSM 3 adalah mode otomatis standar
    psm_modes = [11, 6, 3]

    candidates = []

    for variant_name, variant in variants:
        for psm in psm_modes:
            try:
                text, confidence = _ocr_image(
                    variant,
                    psm,
                    lang
                )

                if text:
                    candidates.append({
                        "text": text,
                        "confidence": confidence,
                        "variant": variant_name,
                        "psm": psm
                    })

            except pytesseract.TesseractError:
                continue

    if not candidates:
        return ""

    # Kata penting untuk kemasan obat.
    # Digunakan hanya untuk menentukan hasil OCR terbaik,
    # bukan untuk melakukan identifikasi obat.
    important_words = [
        "paracetamol",
        "500",
        "mg",
        "tablet",
        "caplet",
        "medicine",
        "obat"
    ]

    def score(candidate):
        text_lower = candidate["text"].lower()

        keyword_score = sum(
            1 for word in important_words
            if word in text_lower
        )

        # Confidence tetap menjadi faktor utama,
        # tetapi hasil yang mengandung kata penting diprioritaskan.
        return (
            keyword_score * 100
            + candidate["confidence"]
            + min(len(candidate["text"]), 100) * 0.1
        )

    best = max(candidates, key=score)

    return best["text"].strip()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Pemakaian: python3 ocr.py <path_gambar>")
        sys.exit(1)

    image_path = sys.argv[1]

    print(f"Membaca gambar: {image_path}")

    text = extract_text(image_path)

    print("\n--- Teks hasil OCR ---")
    print(text)