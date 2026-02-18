import os
import json
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
import time

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gunakan Gemini 3 Flash
model = genai.GenerativeModel('models/gemini-3-flash-preview')

def jalan():
    hari = datetime.now().strftime('%d %B %Y')
    print(f"[*] Menulis analisis sore untuk tanggal {hari}...")

    prompt = f"""Tulis esai analisis teknologi mendalam 2000 kata tentang masa depan AI dan pengaruhnya bagi manusia. 
    Gaya bahasa: Profesional, filosofis, cerdas, dan luwes seperti jurnalis teknologi senior.
    Struktur: 
    - Baris pertama: Judul (tanpa hashtag/tanda kutip).
    - Baris selanjutnya: Konten yang mengalir dalam paragraf-paragraf panjang berisi wawasan tajam."""
    
    try:
        res = model.generate_content(prompt, generation_config={"max_output_tokens": 8192, "temperature": 0.8})
        baris = res.text.split('\n')
        judul = baris[0].strip().replace('*', '').replace('#', '')
        konten = '\n'.join(baris[1:]).strip()

        # Link Gambar Otomatis (Topik: AI & Future)
        img_url = f"https://loremflickr.com/800/450/artificialintelligence,robot?random={int(time.time())}"

        # Simpan ke data.json
        file_path = 'data.json'
        data = json.load(open(file_path)) if os.path.exists(file_path) else []
        data.append({
            "title": judul,
            "content": konten,
            "date": hari,
            "image": img_url,
            "tag": "ANALISIS SORE"
        })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # Push ke GitHub
        os.system('git add . && git commit -m "Update Sore: Analisis" && git push')
        print(f"[V] Berhasil Posting Sore: {judul}")

    except Exception as e:
        print(f"[X] Gagal: {e}")

if __name__ == "__main__":
    jalan()
