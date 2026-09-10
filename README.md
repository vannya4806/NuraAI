# NuraAI

Mesin AI di balik fitur "AI Scan" **NURA** scan kemasan obat, langsung tahu apakah aman dikonsumsi bareng obat yang sedang dijalani.

Repo ini adalah prototipe backend/ML yang mensimulasikan endpoint `POST /scan` di masa depan: foto masuk, hasilnya status keamanan + penjelasan berbahasa awam.

## Alur Pipeline

```
foto kemasan obat
        │
        ▼
  1. OCR (ocr.py)              baca teks mentah dari kemasan
        │
        ▼
  2. Identifikasi obat          ensemble rule-based + ML matching
     (matcher.py + ml_matcher.py, digabung di main.py)
        │
        ▼
  3. Analisis interaksi         cek vs obat yang sedang dikonsumsi + makanan
     (analyzer.py)
        │
        ▼
  4. Penjelasan                 LLM merangkai temuan jadi bahasa awam,
     (llm_explainer.py)         fallback ke template kalau LLM tidak tersedia
        │
        ▼
  Response JSON (status keamanan + penjelasan)
```

Jalankan seluruh alur dari awal sampai akhir:

```bash
python3 main.py path/ke/foto.jpg
```

`main.py` mensimulasikan user yang sedang mengonsumsi Ambroxol dan Eclid,
lalu scan kemasan yang diberikan dan mencetak JSON yang nantinya dikirim ke
aplikasi.

## Modul

- **`ocr.py`** — Mengekstrak teks dari foto kemasan pakai Tesseract. Mencoba
  beberapa varian preprocessing (grayscale, thresholding, inversion) dan mode
  PSM, lalu memilih hasil terbaik berdasarkan confidence + keberadaan kata
  kunci khas label obat. Catatan: aplikasi iOS produksi sebaiknya pakai Apple
  Vision framework untuk OCR on-device; Tesseract di sini hanya pengganti
  sementara untuk prototipe.

- **`text_utils.py`** — Fungsi pembersihan teks yang dipakai bersama oleh
  kedua matcher: membuang angka dosis (`500mg`, `10 ml`), dan memperbaiki
  kebiasaan OCR memecah satu kata jadi huruf-huruf terpisah spasi
  (`A M A R Y L` → `AMARYL`).

- **`matcher.py`** — Identifikasi rule-based: fuzzy matching teks OCR ke
  daftar alias obat yang dikenal (`rapidfuzz`, `WRatio`). Cepat,
  deterministik, tidak perlu training.

- **`ml_matcher.py`** — Identifikasi berbasis ML: pipeline TF-IDF (character
  n-gram) + Linear SVM terkalibrasi yang memprediksi obat beserta confidence
  score-nya. Bisa menangani noise OCR yang kadang lolos dari matcher
  rule-based.

- **`main.py`** — `identify_drug_ensemble()` menggabungkan kedua matcher:
  kalau sepakat ⇒ confidence tinggi; kalau cuma satu yang berhasil ⇒ tetap
  dipakai; kalau beda hasil ⇒ dianggap tidak yakin dan user diminta foto
  ulang, daripada asal menebak.

- **`analyzer.py`** — Inti logika keamanan. Berdasarkan obat yang
  teridentifikasi dan daftar obat yang sedang dikonsumsi user, mencari
  interaksi obat-obat dan obat-makanan, lalu mengembalikan status
  keseluruhan: `aman` / `perlu_perhatian` / `tidak_aman`, lengkap dengan
  rincian pendukungnya (pendekatan Explainable AI: setiap keputusan selalu
  disertai alasan).

- **`llm_explainer.py`** — Mengubah temuan terstruktur dari `analyzer.py`
  menjadi 2-3 kalimat penjelasan berbahasa Indonesia yang mengalir, lewat
  Groq API (`gpt-oss-120b`, endpoint kompatibel OpenAI). LLM diinstruksikan
  hanya merangkai ulang temuan yang ada, bukan menambah klaim medis baru.
  Kalau `GROQ_API_KEY` tidak ada atau panggilan API gagal (alasan apa pun),
  sistem otomatis fallback ke template yang disusun dari data yang sama —
  status keamanan tidak pernah tertahan hanya gara-gara LLM sedang
  bermasalah.

## Data & Training

- **`data/drugs.json`** — ~25 obat umum di Indonesia: nama generik,
  kandungan aktif, kategori, merk dagang, alias OCR, overview. Dataset
  kurasi manual (lihat `build_dataset.py`), disusun mengacu pada DDInter 2.0
  & data interaksi FDA — **wajib divalidasi ulang oleh apoteker/dokter
  sebelum dipakai di aplikasi produksi.**
- **`data/interactions_drug.json`** — pasangan interaksi obat-obat beserta
  status dan penjelasannya.
- **`data/interactions_food.json`** — interaksi obat-makanan (mis. warfarin
  vs sayuran tinggi vitamin K, alkohol).
- **`data/training_data.json`** — 847 sampel sintetis gaya-OCR, dihasilkan
  oleh `generate_training_data.py` dari daftar obat (mensimulasikan
  kesalahan OCR umum seperti tertukarnya `0`/`o`, `1`/`l`, karakter hilang,
  dosis yang menempel ke nama obat) plus contoh negatif ("unknown") supaya
  model belajar menolak teks yang bukan nama obat. Ini baseline sintetis —
  ganti/tambahkan dengan hasil scan foto asli begitu tersedia.
- **`train_ml_matcher.py`** — melatih pipeline TF-IDF + Linear SVM dari
  `training_data.json` dan menyimpannya ke `model/drug_classifier.joblib`.
- **`export_coreml.py`** — mengekspor model terlatih ke Core ML
  (`Model/DrugClassifier.mlmodel`) plus vocabulary/bobot IDF dari TF-IDF
  (`Model/tfidf_config.json`) supaya logika matching yang sama bisa jalan
  secara native on-device di aplikasi iOS (TF-IDF direplikasi ulang di
  Swift).

## Setup

```bash
pip install rapidfuzz pytesseract pillow joblib scikit-learn requests
# Binary Tesseract juga harus terpasang di sistem (dengan language data eng + ind)
```

Untuk penjelasan berbasis LLM, siapkan API key (free tier di
[console.groq.com/keys](https://console.groq.com/keys)):

```bash
export GROQ_API_KEY="api-key-kamu"
```

Tanpa key ini, penjelasan otomatis fallback ke template statis — aplikasi
tetap jalan, hanya teksnya kurang natural.

Untuk retrain atau re-export model ML:

```bash
python3 generate_training_data.py   # regenerate data training sintetis
python3 train_ml_matcher.py         # latih + simpan drug_classifier.joblib
python3 export_coreml.py            # ekspor untuk penggunaan on-device di iOS
```

## Catatan Desain

- **Ensemble lebih baik daripada satu metode saja** — fuzzy matching
  rule-based dan model ML gagal pada jenis noise OCR yang berbeda-beda,
  jadi menggabungkan keduanya (dan menganggap "tidak yakin" saat keduanya
  tidak sepakat) lebih tangguh dibanding memakai salah satunya saja.
- **Explainability di atas segalanya** — analyzer tidak pernah cuma
  mengembalikan flag aman/tidak-aman kosongan; setiap keputusan selalu
  didukung interaksi spesifik yang ditemukan, dan lapisan LLM secara
  eksplisit dilarang mengarang informasi medis baru — tugasnya cuma
  merangkai ulang apa yang sudah ditemukan analyzer.
- **Graceful degradation** — fitur yang paling penting (status keamanan)
  tidak pernah bergantung pada ketersediaan LLM. Kalau Groq down atau kena
  rate limit, user tetap dapat penjelasan yang benar, walau kurang mengalir.