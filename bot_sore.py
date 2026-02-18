import os
import json
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
import time

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('models/gemini-3-flash-preview')

def jalan():
    hari = datetime.now().strftime('%d %B %Y')
    print(f"[*] Menulis analisis sore untuk {hari}...")

    prompt = f"""Tulis esai analisis teknologi 2000 kata tentang masa depan AI. 
    Gaya bahasa: Profesional, cerdas, filosofis. 
    Baris pertama Judul. Baris kedua Kategori (pilih satu: Teknologi, Masa Depan, atau Sains). 
    Baris selanjutnya Konten Lengkap."""
    
    try:
        res = model.generate_content(prompt, generation_config={"max_output_tokens": 8192, "temperature": 0.8})
        clean_text = res.text.replace('**', '').replace('##', '').strip()
        baris = [b for b in clean_text.split('\n') if b.strip()]
        
        judul = baris[0]
        kategori = baris[1] if baris[1] in ["Teknologi", "Masa Depan", "Sains"] else "Masa Depan"
        konten = '\n\n'.join(baris[2:])

        seed = sum(ord(c) for c in judul)
        img_url = f"https://loremflickr.com/800/450/artificialintelligence,robot?lock={seed}"

        file_path = 'data.json'
        data = json.load(open(file_path)) if os.path.exists(file_path) else []
        data.append({
            "title": judul, 
            "content": konten, 
            "date": hari, 
            "image": img_url, 
            "tag": "SORE",
            "category": kategori
        })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        os.system('git add . && git commit -m "Update Sore" && git push')
    except Exception as e:
        print(f"[X] Gagal: {e}")

if __name__ == "__main__":
    jalan()
