from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Pengetahuan (Knowledge Base)
PENYAKIT = {
    "P1": {"nama": "Busuk Akar", "solusi": "Hentikan penyiraman, ganti media tanam yang lebih porous, potong akar yang busuk, dan gunakan fungisida."},
    "P2": {"nama": "Bercak Daun (Leaf Spot)", "solusi": "Potong daun yang terinfeksi, hindari menyiram daun (siram di media tanam), gunakan fungisida berbahan tembaga."},
    "P3": {"nama": "Hama Kutu Putih (Mealybugs)", "solusi": "Bersihkan manual dengan kapas beralkohol, semprot dengan neem oil atau insektisida sistemik."}
}

# Gejala List (untuk referensi saja di backend, UI yang akan define id ini)
# G1: Daun bawah menguning
# G2: Terdapat bercak coklat/hitam pada daun
# G3: Daun rontok berlebihan
# G4: Batang tanaman melunak atau membusuk
# G5: Media tanam berbau kotor/tidak sedap
# G6: Terdapat serangga kecil putih seperti kapas
# G7: Pertumbuhan lambat / kerdil

@app.route('/diagnosa', methods=['POST'])
def diagnosa():
    data = request.json
    gejala_input = data.get('gejala', [])  # list of gejala codes e.g. ["G1", "G4", "G5"]
    
    hasil = None
    
    # Mesin Inferensi (Forward Chaining)
    # R1: IF G1 AND G4 AND G5 THEN P1
    if "G1" in gejala_input and "G4" in gejala_input and "G5" in gejala_input:
        hasil = "P1"
    # R2: IF G2 AND (G1 OR G3) THEN P2
    elif "G2" in gejala_input and ("G1" in gejala_input or "G3" in gejala_input):
        hasil = "P2"
    # R3: IF G6 AND (G7 OR G1) THEN P3
    elif "G6" in gejala_input and ("G7" in gejala_input or "G1" in gejala_input):
        hasil = "P3"
    # R4: Fallback independent symptoms
    elif "G6" in gejala_input:
        hasil = "P3"
    elif "G4" in gejala_input or "G5" in gejala_input:
        hasil = "P1"
    elif "G2" in gejala_input:
        hasil = "P2"
        
    if hasil:
        return jsonify({
            "status": "success",
            "penyakit": PENYAKIT[hasil]["nama"],
            "solusi": PENYAKIT[hasil]["solusi"]
        })
    else:
        # Jika gejala tidak spesifik atau tidak ada rules yang pas
        if len(gejala_input) == 0:
            return jsonify({
                "status": "unknown",
                "pesan": "Anda belum memilih gejala apapun."
            })
        else:
            return jsonify({
                "status": "unknown",
                "pesan": "Gejala tidak spesifik mengarah ke penyakit utama kami. Perbaiki perawatan umum/pencahayaan."
            })

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Port 5001 to avoid clash with fuzzy (5000)
