import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# ============================================================
# 1. MASTER DATA OBAT (merk dagang Indonesia -> kandungan aktif)
# ============================================================
DRUGS = {
    "paracetamol": {
        "nama_generik": "Paracetamol",
        "kandungan_aktif": "Paracetamol (Acetaminophen)",
        "kategori": "Analgesik & Antipiretik",
        "merk_dagang": ["Panadol", "Sanmol", "Bodrex", "Tempra", "Pamol"],
        "overview": "Digunakan untuk meredakan nyeri ringan-sedang dan menurunkan demam."
    },
    "ibuprofen": {
        "nama_generik": "Ibuprofen",
        "kandungan_aktif": "Ibuprofen",
        "kategori": "NSAID (antiinflamasi nonsteroid)",
        "merk_dagang": ["Proris", "Bufect", "Arfen"],
        "overview": "Meredakan nyeri, peradangan, dan demam."
    },
    "asam_mefenamat": {
        "nama_generik": "Asam Mefenamat",
        "kandungan_aktif": "Mefenamic acid",
        "kategori": "NSAID",
        "merk_dagang": ["Ponstan", "Mefinal"],
        "overview": "Meredakan nyeri sedang seperti nyeri haid dan sakit gigi."
    },
    "aspirin": {
        "nama_generik": "Aspirin",
        "kandungan_aktif": "Acetylsalicylic acid",
        "kategori": "NSAID / Antiplatelet",
        "merk_dagang": ["Aspilets", "Ascardia", "Aspirin"],
        "overview": "Dosis rendah digunakan sebagai pengencer darah pencegah stroke/serangan jantung; dosis tinggi sebagai pereda nyeri."
    },
    "amoxicillin": {
        "nama_generik": "Amoxicillin",
        "kandungan_aktif": "Amoxicillin",
        "kategori": "Antibiotik (Penisilin)",
        "merk_dagang": ["Amoxsan", "Yusimox", "Amoxicillin"],
        "overview": "Antibiotik untuk infeksi bakteri saluran pernapasan, telinga, dan saluran kemih."
    },
    "cetirizine": {
        "nama_generik": "Cetirizine",
        "kandungan_aktif": "Cetirizine HCl",
        "kategori": "Antihistamin (generasi 2)",
        "merk_dagang": ["Cerini", "Estin"],
        "overview": "Meredakan alergi seperti gatal, bersin, dan hidung meler; efek mengantuk lebih ringan dibanding antihistamin generasi 1."
    },
    "loratadine": {
        "nama_generik": "Loratadine",
        "kandungan_aktif": "Loratadine",
        "kategori": "Antihistamin (generasi 2)",
        "merk_dagang": ["Clarityne", "Alloris"],
        "overview": "Meredakan gejala alergi tanpa efek mengantuk signifikan."
    },
    "ctm": {
        "nama_generik": "Chlorpheniramine Maleate (CTM)",
        "kandungan_aktif": "Chlorpheniramine maleate",
        "kategori": "Antihistamin (generasi 1, sedatif)",
        "merk_dagang": ["CTM", "Alerhis"],
        "overview": "Antihistamin lama, efektif meredakan alergi namun menyebabkan kantuk kuat."
    },
    "dextromethorphan": {
        "nama_generik": "Dextromethorphan",
        "kandungan_aktif": "Dextromethorphan HBr",
        "kategori": "Antitusif (pereda batuk kering)",
        "merk_dagang": ["Vicks Formula 44", "Woods"],
        "overview": "Meredakan batuk kering/tidak berdahak dengan menekan refleks batuk di otak."
    },
    "ambroxol": {
        "nama_generik": "Ambroxol",
        "kandungan_aktif": "Ambroxol Hydrochloride",
        "kategori": "Mukolitik (pengencer dahak)",
        "merk_dagang": ["Mucera", "Mucosolvan", "RhelixMED"],
        "overview": "Mengencerkan dahak untuk batuk berdahak agar lebih mudah dikeluarkan."
    },
    "omeprazole": {
        "nama_generik": "Omeprazole",
        "kandungan_aktif": "Omeprazole",
        "kategori": "PPI (penghambat pompa proton)",
        "merk_dagang": ["Pumpitor", "Losec", "Omepros"],
        "overview": "Menurunkan produksi asam lambung untuk mengatasi maag dan GERD."
    },
    "antasida": {
        "nama_generik": "Antasida",
        "kandungan_aktif": "Aluminium hidroksida & Magnesium hidroksida",
        "kategori": "Antasida",
        "merk_dagang": ["Promag", "Mylanta", "Polysilane"],
        "overview": "Menetralkan asam lambung secara cepat untuk meredakan maag."
    },
    "metformin": {
        "nama_generik": "Metformin",
        "kandungan_aktif": "Metformin HCl",
        "kategori": "Antidiabetes (Biguanide)",
        "merk_dagang": ["Glucophage", "Glumin"],
        "overview": "Obat lini pertama diabetes tipe 2, menurunkan produksi gula di hati."
    },
    "eclid": {
        "nama_generik": "Ipragliflozin",
        "kandungan_aktif": "Ipragliflozin L-Proline",
        "kategori": "Antidiabetes (SGLT2 inhibitor)",
        "merk_dagang": ["Eclid"],
        "overview": "Menurunkan gula darah dengan meningkatkan pembuangan glukosa lewat urin."
    },
    "glimepiride": {
        "nama_generik": "Glimepiride",
        "kandungan_aktif": "Glimepiride",
        "kategori": "Antidiabetes (Sulfonilurea)",
        "merk_dagang": ["Amaryl"],
        "overview": "Merangsang pankreas melepaskan lebih banyak insulin untuk menurunkan gula darah."
    },
    "amlodipine": {
        "nama_generik": "Amlodipine",
        "kandungan_aktif": "Amlodipine besylate",
        "kategori": "Antihipertensi (CCB)",
        "merk_dagang": ["Norvask", "Tensivask"],
        "overview": "Menurunkan tekanan darah dengan melebarkan pembuluh darah."
    },
    "captopril": {
        "nama_generik": "Captopril",
        "kandungan_aktif": "Captopril",
        "kategori": "Antihipertensi (ACE inhibitor)",
        "merk_dagang": ["Captopril", "Tensicap"],
        "overview": "Menurunkan tekanan darah dengan menghambat enzim pengubah angiotensin."
    },
    "bisoprolol": {
        "nama_generik": "Bisoprolol",
        "kandungan_aktif": "Bisoprolol fumarate",
        "kategori": "Antihipertensi (Beta blocker)",
        "merk_dagang": ["Concor"],
        "overview": "Menurunkan tekanan darah dan detak jantung."
    },
    "simvastatin": {
        "nama_generik": "Simvastatin",
        "kandungan_aktif": "Simvastatin",
        "kategori": "Antikolesterol (Statin)",
        "merk_dagang": ["Zocor", "Simvastatin"],
        "overview": "Menurunkan kadar kolesterol LDL dalam darah."
    },
    "warfarin": {
        "nama_generik": "Warfarin",
        "kandungan_aktif": "Warfarin sodium",
        "kategori": "Antikoagulan",
        "merk_dagang": ["Simarc"],
        "overview": "Mengencerkan darah untuk mencegah pembekuan darah pada pasien risiko stroke/trombosis."
    },
    "abilify": {
        "nama_generik": "Aripiprazole",
        "kandungan_aktif": "Aripiprazole",
        "kategori": "Antipsikotik",
        "merk_dagang": ["Abilify"],
        "overview": "Mengatasi gangguan mental seperti skizofrenia dan gangguan bipolar dengan menyeimbangkan dopamin dan serotonin."
    },
    "fluoxetine": {
        "nama_generik": "Fluoxetine",
        "kandungan_aktif": "Fluoxetine HCl",
        "kategori": "Antidepresan (SSRI)",
        "merk_dagang": ["Prozac", "Andep"],
        "overview": "Mengatasi depresi dan gangguan kecemasan dengan meningkatkan kadar serotonin."
    },
    "alprazolam": {
        "nama_generik": "Alprazolam",
        "kandungan_aktif": "Alprazolam",
        "kategori": "Ansiolitik (Benzodiazepine)",
        "merk_dagang": ["Xanax", "Alganax"],
        "overview": "Meredakan kecemasan dan panik dengan menenangkan sistem saraf pusat."
    },
    "loperamide": {
        "nama_generik": "Loperamide",
        "kandungan_aktif": "Loperamide HCl",
        "kategori": "Antidiare",
        "merk_dagang": ["Imodium", "Lodia"],
        "overview": "Memperlambat gerakan usus untuk mengatasi diare."
    },
    "domperidone": {
        "nama_generik": "Domperidone",
        "kandungan_aktif": "Domperidone",
        "kategori": "Antiemetik & Prokinetik",
        "merk_dagang": ["Vometa", "Vosea"],
        "overview": "Meredakan mual, muntah, dan rasa begah dengan mempercepat pengosongan lambung."
    },
}

# Bangun alias_ocr otomatis: nama generik + semua merk dagang (lowercase)
for drug_id, info in DRUGS.items():
    aliases = {info["nama_generik"].lower(), drug_id.replace("_", " ")}
    aliases.update(m.lower() for m in info["merk_dagang"])
    aliases.add(info["kandungan_aktif"].split(" ")[0].lower())
    info["alias_ocr"] = sorted(aliases)

with open(DATA_DIR / "drugs.json", "w", encoding="utf-8") as f:
    json.dump(DRUGS, f, indent=2, ensure_ascii=False)

# ============================================================
# 2. INTERAKSI OBAT-OBAT (drug-drug interaction)
# status: aman | perlu_perhatian | tidak_aman
# ============================================================
DRUG_INTERACTIONS = [
    {"obat_a": "warfarin", "obat_b": "aspirin", "status": "tidak_aman",
     "penjelasan": "Kombinasi dua zat pengencer darah meningkatkan risiko pendarahan serius.",
     "sumber": "Interaksi mayor, konsisten dengan DDInter & FDA Drug Interactions"},
    {"obat_a": "warfarin", "obat_b": "ibuprofen", "status": "tidak_aman",
     "penjelasan": "NSAID dapat meningkatkan risiko pendarahan saluran cerna saat dikombinasi dengan warfarin.",
     "sumber": "Interaksi mayor, konsisten dengan DDInter & FDA Drug Interactions"},
    {"obat_a": "warfarin", "obat_b": "asam_mefenamat", "status": "tidak_aman",
     "penjelasan": "NSAID meningkatkan risiko pendarahan pada pasien yang mengonsumsi warfarin.",
     "sumber": "Interaksi mayor golongan NSAID-antikoagulan"},
    {"obat_a": "warfarin", "obat_b": "amoxicillin", "status": "perlu_perhatian",
     "penjelasan": "Antibiotik dapat mengganggu flora usus penghasil vitamin K sehingga meningkatkan efek warfarin; perlu pemantauan INR.",
     "sumber": "Interaksi moderat, umum pada pemakaian antibiotik + antikoagulan"},
    {"obat_a": "warfarin", "obat_b": "paracetamol", "status": "perlu_perhatian",
     "penjelasan": "Penggunaan paracetamol dosis tinggi/jangka panjang bersama warfarin dapat meningkatkan efek pengenceran darah.",
     "sumber": "Interaksi moderat pada penggunaan jangka panjang"},
    {"obat_a": "captopril", "obat_b": "ibuprofen", "status": "perlu_perhatian",
     "penjelasan": "NSAID dapat menurunkan efektivitas obat penurun tekanan darah dan membebani fungsi ginjal.",
     "sumber": "Interaksi moderat golongan ACE inhibitor-NSAID"},
    {"obat_a": "aspirin", "obat_b": "ibuprofen", "status": "tidak_aman",
     "penjelasan": "Ibuprofen dapat menurunkan efek perlindungan jantung dari aspirin dosis rendah serta menambah risiko iritasi lambung.",
     "sumber": "Interaksi mayor, dikenal luas dalam farmakologi klinis"},
    {"obat_a": "eclid", "obat_b": "metformin", "status": "aman",
     "penjelasan": "Kombinasi umum terapi diabetes tipe 2 dan sering diresepkan bersamaan oleh dokter.",
     "sumber": "Kombinasi terapi standar diabetes"},
    {"obat_a": "eclid", "obat_b": "abilify", "status": "tidak_aman",
     "penjelasan": "Abilify (antipsikotik atipikal) dapat memengaruhi kadar gula darah, berlawanan dengan efek Eclid; berisiko membuat gula darah tidak stabil.",
     "sumber": "Efek metabolik antipsikotik atipikal terhadap kontrol glikemik"},
    {"obat_a": "alprazolam", "obat_b": "ctm", "status": "tidak_aman",
     "penjelasan": "Kombinasi dua obat penekan sistem saraf pusat dapat menyebabkan kantuk berlebihan hingga gangguan pernapasan.",
     "sumber": "Interaksi mayor golongan sedatif-benzodiazepine"},
    {"obat_a": "alprazolam", "obat_b": "cetirizine", "status": "perlu_perhatian",
     "penjelasan": "Efek mengantuk dapat menumpuk meski Cetirizine tergolong antihistamin generasi baru yang lebih ringan.",
     "sumber": "Interaksi moderat golongan sedatif ringan"},
    {"obat_a": "alprazolam", "obat_b": "loperamide", "status": "perlu_perhatian",
     "penjelasan": "Kombinasi dapat meningkatkan efek penekanan sistem saraf pusat.",
     "sumber": "Interaksi moderat"},
    {"obat_a": "fluoxetine", "obat_b": "aspirin", "status": "perlu_perhatian",
     "penjelasan": "SSRI dapat meningkatkan risiko pendarahan bila dikombinasikan dengan obat pengencer darah/NSAID.",
     "sumber": "Interaksi moderat golongan SSRI-antiplatelet"},
    {"obat_a": "fluoxetine", "obat_b": "ibuprofen", "status": "perlu_perhatian",
     "penjelasan": "Risiko pendarahan saluran cerna meningkat pada kombinasi SSRI dengan NSAID.",
     "sumber": "Interaksi moderat golongan SSRI-NSAID"},
    {"obat_a": "fluoxetine", "obat_b": "domperidone", "status": "tidak_aman",
     "penjelasan": "Keduanya berpotensi memperpanjang interval QT jantung sehingga meningkatkan risiko gangguan irama jantung.",
     "sumber": "Interaksi mayor terkait risiko perpanjangan QT"},
    {"obat_a": "simvastatin", "obat_b": "amlodipine", "status": "perlu_perhatian",
     "penjelasan": "Amlodipine dapat meningkatkan kadar simvastatin dalam darah sehingga menambah risiko gangguan otot (miopati) pada dosis tinggi.",
     "sumber": "Interaksi moderat, umum dicatat pada label FDA simvastatin"},
    {"obat_a": "omeprazole", "obat_b": "simvastatin", "status": "aman",
     "penjelasan": "Tidak ditemukan interaksi bermakna antara keduanya pada penggunaan dosis normal.",
     "sumber": "Tidak ada laporan interaksi signifikan"},
    {"obat_a": "ambroxol", "obat_b": "amoxicillin", "status": "aman",
     "penjelasan": "Kombinasi ini justru umum diresepkan bersamaan untuk infeksi saluran napas disertai dahak.",
     "sumber": "Kombinasi terapi umum"},
    {"obat_a": "ambroxol", "obat_b": "dextromethorphan", "status": "perlu_perhatian",
     "penjelasan": "Ambroxol untuk batuk berdahak dan dextromethorphan untuk batuk kering bekerja berlawanan arah; kombinasi umumnya tidak dianjurkan tanpa anjuran dokter.",
     "sumber": "Prinsip farmakologi: mukolitik vs antitusif"},
    {"obat_a": "glimepiride", "obat_b": "aspirin", "status": "perlu_perhatian",
     "penjelasan": "Aspirin dosis tinggi dapat memperkuat efek penurunan gula darah dari Glimepiride, berisiko hipoglikemia.",
     "sumber": "Interaksi moderat golongan sulfonilurea-salisilat"},
    {"obat_a": "bisoprolol", "obat_b": "captopril", "status": "aman",
     "penjelasan": "Kombinasi umum pada terapi hipertensi/gagal jantung dan sering diresepkan bersamaan dengan pemantauan dokter.",
     "sumber": "Kombinasi terapi standar kardiovaskular"},
    {"obat_a": "abilify", "obat_b": "ambroxol", "status": "aman",
     "penjelasan": "Belum ada laporan interaksi signifikan antara Abilify dan Ambroxol pada penggunaan dosis normal.",
     "sumber": "Tidak ada laporan interaksi signifikan"},
    {"obat_a": "abilify", "obat_b": "paracetamol", "status": "aman",
     "penjelasan": "Abilify dan Paracetamol umumnya aman dikonsumsi bersamaan sesuai anjuran dokter.",
     "sumber": "Tidak ada laporan interaksi signifikan"},
    {"obat_a": "ambroxol", "obat_b": "eclid", "status": "aman",
     "penjelasan": "Tidak ditemukan interaksi bermakna antara Ambroxol dan Eclid.",
     "sumber": "Tidak ada laporan interaksi signifikan"},
    {"obat_a": "ambroxol", "obat_b": "paracetamol", "status": "aman",
     "penjelasan": "Ambroxol dan Paracetamol dapat dikonsumsi bersamaan dan sering diresepkan dalam kombinasi obat flu.",
     "sumber": "Kombinasi terapi umum"},
    {"obat_a": "eclid", "obat_b": "paracetamol", "status": "aman",
     "penjelasan": "Tidak ditemukan interaksi bermakna antara Eclid dan Paracetamol pada dosis normal.",
     "sumber": "Tidak ada laporan interaksi signifikan"},
]

with open(DATA_DIR / "interactions_drug.json", "w", encoding="utf-8") as f:
    json.dump(DRUG_INTERACTIONS, f, indent=2, ensure_ascii=False)

# ============================================================
# 3. INTERAKSI OBAT-MAKANAN (drug-food interaction)
# ============================================================
FOOD_INTERACTIONS = {
    "warfarin": [
        {"item": "sayuran hijau tinggi vitamin K (bayam, brokoli, kale)", "status": "perlu_perhatian",
         "penjelasan": "Vitamin K dapat menurunkan efektivitas warfarin; konsumsi sebaiknya konsisten jumlahnya, bukan dihindari total.",
         "sumber": "Interaksi klasik warfarin-vitamin K"},
        {"item": "alkohol", "status": "tidak_aman",
         "penjelasan": "Alkohol dapat meningkatkan efek pengenceran darah warfarin secara tidak terduga.",
         "sumber": "Interaksi mayor"},
    ],
    "simvastatin": [
        {"item": "grapefruit / jeruk bali", "status": "tidak_aman",
         "penjelasan": "Grapefruit menghambat enzim yang memetabolisme simvastatin sehingga kadarnya di darah meningkat drastis, menambah risiko kerusakan otot.",
         "sumber": "Interaksi mayor, tercantum pada label FDA simvastatin"},
    ],
    "amlodipine": [
        {"item": "grapefruit / jeruk bali", "status": "perlu_perhatian",
         "penjelasan": "Grapefruit dapat meningkatkan kadar amlodipine dalam darah sehingga efek penurunan tekanan darah lebih kuat dari seharusnya.",
         "sumber": "Interaksi moderat golongan CCB-grapefruit"},
    ],
    "metformin": [
        {"item": "alkohol", "status": "tidak_aman",
         "penjelasan": "Alkohol meningkatkan risiko asidosis laktat, efek samping serius dari Metformin.",
         "sumber": "Interaksi mayor, tercantum pada label Metformin"},
    ],
    "eclid": [
        {"item": "alkohol", "status": "tidak_aman",
         "penjelasan": "Alkohol dapat meningkatkan risiko hipoglikemia (gula darah rendah) saat dikonsumsi bersama Eclid.",
         "sumber": "Interaksi mayor golongan antidiabetes-alkohol"},
    ],
    "paracetamol": [
        {"item": "alkohol", "status": "tidak_aman",
         "penjelasan": "Konsumsi alkohol bersama Paracetamol dalam jangka panjang meningkatkan risiko kerusakan hati.",
         "sumber": "Interaksi mayor, dikenal luas"},
    ],
    "aspirin": [
        {"item": "alkohol", "status": "tidak_aman",
         "penjelasan": "Alkohol meningkatkan risiko iritasi dan pendarahan lambung saat dikonsumsi bersama Aspirin.",
         "sumber": "Interaksi mayor golongan NSAID-alkohol"},
    ],
    "alprazolam": [
        {"item": "alkohol", "status": "tidak_aman",
         "penjelasan": "Kombinasi ini dapat menyebabkan penekanan sistem saraf pusat yang berbahaya, termasuk gangguan pernapasan.",
         "sumber": "Interaksi mayor golongan benzodiazepine-alkohol"},
    ],
    "captopril": [
        {"item": "makanan/garam tinggi kalium (pisang, garam diet rendah natrium)", "status": "perlu_perhatian",
         "penjelasan": "Captopril dapat meningkatkan kadar kalium darah; konsumsi berlebih makanan tinggi kalium berisiko hiperkalemia.",
         "sumber": "Interaksi moderat golongan ACE inhibitor-kalium"},
    ],
    "abilify": [
        {"item": "grapefruit / jeruk bali", "status": "tidak_aman",
         "penjelasan": "Grapefruit dapat meningkatkan kadar Abilify dalam darah dan memperbesar risiko efek samping.",
         "sumber": "Interaksi mayor golongan grapefruit-CYP3A4"},
    ],
    "ambroxol": [
        {"item": "susu", "status": "aman",
         "penjelasan": "Boleh diminum bersama susu, namun sebaiknya beri jeda agar penyerapan optimal.",
         "sumber": "Catatan penyerapan umum"},
    ],
}

with open(DATA_DIR / "interactions_food.json", "w", encoding="utf-8") as f:
    json.dump(FOOD_INTERACTIONS, f, indent=2, ensure_ascii=False)

print(f"Selesai: {len(DRUGS)} obat, {len(DRUG_INTERACTIONS)} interaksi obat-obat, {sum(len(v) for v in FOOD_INTERACTIONS.values())} interaksi obat-makanan")
