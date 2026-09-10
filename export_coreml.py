import json
from pathlib import Path

import joblib
import numpy as np
import coremltools as ct

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from coremltools.models import datatypes


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "training_data.json"
MODEL_DIR = BASE_DIR / "Model"

MODEL_DIR.mkdir(exist_ok=True)

COREML_PATH = MODEL_DIR / "DrugClassifier.mlmodel"
TFIDF_PATH = MODEL_DIR / "tfidf_config.json"


# ============================================================
# LOAD DATA
# ============================================================

print("[1/7] Membaca training data...")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)

texts = [item[0] for item in dataset]
labels = [item[1] for item in dataset]

print(f"      Jumlah data  : {len(texts)}")
print(f"      Jumlah class : {len(set(labels))}")


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print("[2/7] Membagi dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    texts,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)


# ============================================================
# TF-IDF
# ============================================================

print("[3/7] Membuat TF-IDF...")

vectorizer = TfidfVectorizer(
    analyzer="char_wb",
    ngram_range=(2, 4),
    lowercase=True
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print(f"      Jumlah fitur : {len(vectorizer.vocabulary_)}")


# ============================================================
# TRAIN LINEAR SVM
# ============================================================

print("[4/7] Melatih LinearSVC...")

classifier = LinearSVC()

classifier.fit(X_train_tfidf, y_train)

accuracy = classifier.score(X_test_tfidf, y_test)

print(f"      Akurasi      : {accuracy:.2%}")


# ============================================================
# EXPORT TF-IDF CONFIG
# ============================================================

print("[5/7] Menyimpan konfigurasi TF-IDF...")

vocabulary = vectorizer.vocabulary_
idf = vectorizer.idf_

tfidf_config = {
    "analyzer": "char_wb",
    "ngram_range": [2, 4],
    "lowercase": True,
    "norm": "l2",
    "use_idf": True,
    "smooth_idf": True,

    "vocabulary": vocabulary,

    "idf": idf.tolist(),

    "feature_count": len(vocabulary)
}

with open(TFIDF_PATH, "w", encoding="utf-8") as f:
    json.dump(
        tfidf_config,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"      TF-IDF config: {TFIDF_PATH}")


# ============================================================
# CONVERT LINEAR SVC TO CORE ML
# ============================================================

print("[6/7] Mengubah LinearSVC ke Core ML...")

feature_count = len(vocabulary)

coreml_model = ct.converters.sklearn.convert(
    classifier,
    input_features=[
        ("features", datatypes.Array(feature_count))
    ],
    output_feature_names=[
        "drug_id",
        "scores"
    ]
)

coreml_model.author = "NuraAI"

coreml_model.short_description = (
    "Drug identification using TF-IDF character n-grams "
    "and Linear SVM."
)

coreml_model.version = "1.0"

coreml_model.save(str(COREML_PATH))


# ============================================================
# SAVE ALSO AS JOBLIB
# ============================================================

joblib.dump(
    {
        "vectorizer": vectorizer,
        "classifier": classifier
    },
    MODEL_DIR / "drug_classifier_export.joblib"
)


# ============================================================
# DONE
# ============================================================

print("[7/7] Selesai!")

print()
print("========================================")
print("EXPORT BERHASIL")
print("========================================")
print(f"Core ML    : {COREML_PATH}")
print(f"TF-IDF     : {TFIDF_PATH}")
print(f"Joblib     : {MODEL_DIR / 'drug_classifier_export.joblib'}")
print(f"Features   : {feature_count}")
print("========================================")