import os
import json
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
import time
import random

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('models/gemini-3-flash-preview')

def jalan():
    hari = datetime.now().strftime('%d %B %Y')
    print(f"[*] Menulis artikel pagi (Viral) untuk {hari}...")

    prompt = f"""Tulis artikel blog viral 2000 kata tentang tren teknologi hari ini {hari}. 
    Gaya bahasa: Sangat manusiawi, santai, provokatif. 
    Baris pertama Judul. Baris kedua Kategori (pilih satu: Viral, Teknologi, atau Bisnis). 
    Baris selanjutnya Konten Lengkap."""
    
    try:
        res = model.generate_content(prompt, generation_config={"max_output_tokens": 8192, "temperature": 0.9})
        clean_text = res.text.replace('**', '').replace('##', '').strip()
        baris = [b for b in clean_text.split('\n') if b.strip()]
        
        judul = baris[0]
        kategori = baris[1] if baris[1] in ["Viral", "Teknologi", "Bisnis"] else "Viral"
        konten = '\n\n'.join(baris[2:])

        # Gambar Permanen berdasarkan Judul
        seed = sum(ord(c) for c in judul)
        img_url = f"https://loremflickr.com/800/450/tech,digital?lock={seed}"

        file_path = 'data.json'
        data = json.load(open(file_path)) if os.path.exists(file_path) else []
        data.append({
            "title": judul, 
            "content": konten, 
            "date": hari, 
            "image": img_url, 
            "tag": "PAGI",
            "category": kategori
        })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        os.system('git add . && git commit -m "Update Pagi" && git push')
        print(f"[V] Sukses: {judul}")
    except Exception as e:
        print(f"[X] Gagal: {e}")

if __name__ == "__main__":
    jalan()
