import json
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline

DATA_DIR = Path(__file__).parent / "data"
MODEL_DIR = Path(__file__).parent / "model"
MODEL_DIR.mkdir(exist_ok=True)

with open(DATA_DIR / "training_data.json", encoding="utf-8") as f:
    dataset = json.load(f)

texts = [t for t, _ in dataset]
labels = [l for _, l in dataset]

X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), lowercase=True)),
    ("clf", CalibratedClassifierCV(LinearSVC(), cv=3)),
])

print("Melatih model...")
pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nAkurasi pada data uji: {acc:.2%}\n")
print(classification_report(y_test, y_pred, zero_division=0))

joblib.dump(pipeline, MODEL_DIR / "drug_classifier.joblib")
print(f"Model disimpan ke {MODEL_DIR / 'drug_classifier.joblib'}")