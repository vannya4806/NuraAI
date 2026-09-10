import json
import sys

from ocr import extract_text
from matcher import match_drug
from ml_matcher import predict_drug_ml
from analyzer import analyze
from llm_explainer import explain_with_fallback


def identify_drug_ensemble(raw_text: str):
    """
    Gabungkan hasil rule-based (fuzzy matching) dan ML (TF-IDF + SVM).
    Strategi: kalau keduanya sepakat -> confidence tinggi.
    Kalau cuma salah satu yang berhasil -> tetap dipakai (saling menutupi kelemahan).
    Kalau keduanya beda obat -> lebih aman dianggap tidak yakin (butuh foto ulang).
    """
    rule_id, rule_score = match_drug(raw_text)
    ml_id, ml_score = predict_drug_ml(raw_text)

    if rule_id and ml_id:
        if rule_id == ml_id:
            return rule_id, "sepakat (rule-based + ML)"
        else:
            return None, f"tidak sepakat: rule-based={rule_id}, ML={ml_id}"
    elif rule_id:
        return rule_id, "hanya rule-based berhasil"
    elif ml_id:
        return ml_id, "hanya ML berhasil"
    else:
        return None, "keduanya gagal"


def scan_obat(image_path: str, current_drug_ids: list[str]) -> dict:
    print(f"[1/4] Membaca gambar: {image_path}")
    raw_text = extract_text(image_path)
    print(f"[2/4] Teks mentah hasil OCR:\n{raw_text}\n")

    drug_id, keterangan = identify_drug_ensemble(raw_text)
    print(f"[3/4] Hasil identifikasi (ensemble): drug_id={drug_id} ({keterangan})")

    if not drug_id:
        return {
            "success": False,
            "error": "Analisis Gagal. Maaf! Kami gagal mendeteksi gambar yang Anda ambil. "
                     "Silakan ambil gambar kembali.",
        }

    print("[4/4] Menjalankan analisis interaksi...")
    hasil_analisis = analyze(drug_id, current_drug_ids)

    print("[+] Menyusun penjelasan (LLM / fallback template)...")
    penjelasan = explain_with_fallback(hasil_analisis)
    hasil_analisis["penjelasan_lengkap"] = penjelasan["penjelasan_lengkap"]
    hasil_analisis["sumber_penjelasan"] = penjelasan["sumber_penjelasan"]

    return {"success": True, "data": hasil_analisis}


if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else "test_images/abilify_sample.png"
    # Simulasi: user sedang mengonsumsi Ambroxol dan Eclid (sesuai contoh mockup)
    current_drugs = ["ambroxol", "eclid"]

    result = scan_obat(image_path, current_drugs)
    print("\n=== HASIL AKHIR (response yang dikirim ke app) ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))