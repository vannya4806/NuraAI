import os
import requests

# Groq pakai format yang kompatibel dengan OpenAI Chat Completions API.
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
# Model gratis di Groq yang cukup pintar untuk Bahasa Indonesia.
# Catatan: "llama-3.3-70b-versatile" sudah di-deprecate Groq per 16 Agustus 2026,
# jadi dipakai penggantinya sesuai rekomendasi resmi Groq.
# Cek daftar model terbaru & jadwal deprecation di https://console.groq.com/docs/models
# dan https://console.groq.com/docs/deprecations
MODEL = "openai/gpt-oss-120b"


def _build_prompt(analysis: dict) -> str:
    """Susun prompt terstruktur dari hasil analisis (bukan teks bebas),
    supaya LLM punya konteks lengkap dan tidak mengarang informasi baru."""
    obat = analysis.get("nama_obat", "obat ini")
    status = analysis.get("status_keamanan", "aman")
    overview = analysis.get("overview", "")

    temuan = []
    for item in analysis.get("interaksi_obat", []):
        temuan.append(f"- Interaksi dengan {item['obat']}: status {item['status']}. {item['penjelasan']}")
    for item in analysis.get("interaksi_makanan", []):
        temuan.append(f"- Interaksi dengan {item['item']}: status {item['status']}. {item['penjelasan']}")

    temuan_text = "\n".join(temuan) if temuan else "Tidak ada interaksi tercatat."

    prompt = f"""Kamu adalah asisten edukasi kesehatan di aplikasi NURA. Tugasmu MERANGKAI
(bukan menambah informasi baru) data interaksi obat berikut menjadi 2-3 kalimat
penjelasan yang mudah dipahami orang awam, dalam Bahasa Indonesia, dengan nada
tenang dan tidak menakut-nakuti. Jangan menyarankan dosis atau tindakan medis
spesifik -- cukup jelaskan temuannya dan sarankan konsultasi ke dokter/apoteker
jika statusnya tidak aman atau perlu perhatian.

Obat: {obat}
Status keamanan keseluruhan: {status}
Overview: {overview}

Temuan interaksi:
{temuan_text}

Tulis HANYA penjelasannya, tanpa pembuka/basa-basi."""
    return prompt


def generate_explanation_llm(analysis: dict) -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY tidak ditemukan di environment variable")

    prompt = _build_prompt(analysis)
    response = requests.post(
        GROQ_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def _fallback_template(analysis: dict) -> str:
    """Fallback: gabungkan penjelasan template yang sudah ada di data interaksi."""
    parts = [analysis.get("overview", "")]
    for item in analysis.get("interaksi_obat", []):
        if item["status"] != "aman":
            parts.append(f"{item['obat']}: {item['penjelasan']}")
    for item in analysis.get("interaksi_makanan", []):
        if item["status"] != "aman":
            parts.append(f"{item['item']}: {item['penjelasan']}")
    if len(parts) == 1:
        parts.append("Tidak ditemukan interaksi berisiko yang perlu diwaspadai.")
    return " ".join(parts)


def explain_with_fallback(analysis: dict) -> dict:
    """
    Fungsi utama yang dipanggil dari main.py.
    Selalu berhasil mengembalikan penjelasan -- entah dari LLM atau fallback.
    """
    try:
        llm_text = generate_explanation_llm(analysis)
        return {"penjelasan_lengkap": llm_text, "sumber_penjelasan": "LLM (Groq - GPT-OSS 120B)"}
    except Exception as e:
        return {
            "penjelasan_lengkap": _fallback_template(analysis),
            "sumber_penjelasan": f"Template (fallback, LLM tidak tersedia: {type(e).__name__})",
        }


if __name__ == "__main__":
    from analyzer import analyze
    hasil = analyze("abilify", ["ambroxol", "eclid"])
    penjelasan = explain_with_fallback(hasil)
    print("Sumber:", penjelasan["sumber_penjelasan"])
    print("Penjelasan:\n", penjelasan["penjelasan_lengkap"])