import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

with open(DATA_DIR / "drugs.json", encoding="utf-8") as f:
    DRUGS = json.load(f)

with open(DATA_DIR / "interactions_drug.json", encoding="utf-8") as f:
    DRUG_INTERACTIONS = json.load(f)

with open(DATA_DIR / "interactions_food.json", encoding="utf-8") as f:
    FOOD_INTERACTIONS = json.load(f)


def _find_drug_interaction(drug_a: str, drug_b: str):
    for item in DRUG_INTERACTIONS:
        pair = {item["obat_a"], item["obat_b"]}
        if pair == {drug_a, drug_b}:
            return item
    return None


def analyze(new_drug_id: str, current_drug_ids: list[str]) -> dict:
    """
    new_drug_id       : id obat yang baru saja discan
    current_drug_ids  : daftar id obat yang sedang dikonsumsi user (dari profil/riwayat)

    Return dict siap dikirim sebagai response API / ditampilkan di UI.
    """
    if new_drug_id not in DRUGS:
        return {"error": f"Obat '{new_drug_id}' tidak ditemukan di database."}

    # urutan prioritas status: tidak_aman > perlu_perhatian > aman
    STATUS_RANK = {"aman": 0, "perlu_perhatian": 1, "tidak_aman": 2}

    drug_info = DRUGS[new_drug_id]
    drug_interactions_result = []
    overall_status = "aman"

    for other_id in current_drug_ids:
        if other_id == new_drug_id or other_id not in DRUGS:
            continue
        interaction = _find_drug_interaction(new_drug_id, other_id)
        if interaction:
            drug_interactions_result.append({
                "obat": DRUGS[other_id]["nama_generik"],
                "status": interaction["status"],
                "penjelasan": interaction["penjelasan"],
                "sumber": interaction.get("sumber", ""),
            })
            if STATUS_RANK[interaction["status"]] > STATUS_RANK[overall_status]:
                overall_status = interaction["status"]
        else:
            drug_interactions_result.append({
                "obat": DRUGS[other_id]["nama_generik"],
                "status": "aman",
                "penjelasan": "Belum ada data interaksi bermakna yang tercatat.",
                "sumber": "",
            })

    food_interactions_result = FOOD_INTERACTIONS.get(new_drug_id, [])
    for food in food_interactions_result:
        if STATUS_RANK[food["status"]] > STATUS_RANK[overall_status]:
            overall_status = food["status"]

    return {
        "nama_obat": drug_info["nama_generik"],
        "kandungan_aktif": drug_info["kandungan_aktif"],
        "kategori": drug_info["kategori"],
        "overview": drug_info["overview"],
        "status_keamanan": overall_status,
        "interaksi_obat": drug_interactions_result,
        "interaksi_makanan": food_interactions_result,
    }


if __name__ == "__main__":
    # Simulasi: user baru scan Abilify, dan sedang mengonsumsi Ambroxol + Eclid
    hasil = analyze("abilify", ["ambroxol", "eclid"])
    print(json.dumps(hasil, indent=2, ensure_ascii=False))