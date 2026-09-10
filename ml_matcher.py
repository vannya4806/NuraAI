import joblib
from pathlib import Path
from text_utils import get_candidates

MODEL_PATH = Path(__file__).parent / "model" / "drug_classifier.joblib"
_pipeline = joblib.load(MODEL_PATH)


def predict_drug_ml(raw_text: str, threshold: float = 0.35):
    """
    Prediksi obat dari teks OCR memakai model ML terlatih.
    Return: (drug_id, confidence) - drug_id None/"unknown" jika tidak yakin.
    """
    candidates = get_candidates(raw_text)
    best_label, best_prob = None, 0.0

    for candidate in candidates:
        probs = _pipeline.predict_proba([candidate])[0]
        classes = _pipeline.classes_
        idx = probs.argmax()
        label, prob = classes[idx], probs[idx]
        if label != "unknown" and prob > best_prob:
            best_label, best_prob = label, prob

    if best_label and best_prob >= threshold:
        return best_label, round(float(best_prob), 3)
    return None, 0.0


if __name__ == "__main__":
    import sys
    test_text = sys.argv[1] if len(sys.argv) > 1 else "AMBR0X0L HYDR0CHL0RIDE"
    drug_id, score = predict_drug_ml(test_text)
    print(f"Input: {test_text}")
    print(f"Hasil ML: {drug_id} (confidence: {score})")