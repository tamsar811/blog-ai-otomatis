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
    print(f"[*] Menulis artikel pagi (Viral) untuk tanggal {hari}...")

    prompt = f"""Tulis artikel blog viral 2000 kata tentang tren teknologi hari ini {hari}. 
    Gaya bahasa: Santai, berjiwa muda, provokatif, dan sangat manusiawi (human-like).
    Struktur: 
    - Baris pertama: Judul (tanpa hashtag/tanda kutip).
    - Baris selanjutnya: Konten mengalir tanpa banyak poin-poin (bullet points).
    Gunakan cerita (storytelling) agar pembaca betah membaca sampai akhir."""
    
    try:
        res = model.generate_content(prompt, generation_config={"max_output_tokens": 8192, "temperature": 0.9})
        baris = res.text.split('\n')
        judul = baris[0].strip().replace('*', '').replace('#', '')
        konten = '\n'.join(baris[1:]).strip()

        # Link Gambar Otomatis (Topik: Tech & Viral)
        img_url = f"https://loremflickr.com/800/450/technology,trending?random={int(time.time())}"

        # Simpan ke data.json
        file_path = 'data.json'
        data = json.load(open(file_path)) if os.path.exists(file_path) else []
        data.append({
            "title": judul,
            "content": konten,
            "date": hari,
            "image": img_url,
            "tag": "VIRAL PAGI"
        })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # Push ke GitHub
        os.system('git add . && git commit -m "Update Pagi: Viral" && git push')
        print(f"[V] Berhasil Posting Pagi: {judul}")

    except Exception as e:
        print(f"[X] Gagal: {e}")

if __name__ == "__main__":
    jalan()

