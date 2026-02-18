import os
import json
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[!] Error: API Key tidak ditemukan!")
    exit()

genai.configure(api_key=api_key)

# Mencoba model flash, jika gagal otomatis pakai pro
try:
    model = model = genai.GenerativeModel('models/gemini-3-flash-preview')
    print("[*] Menggunakan model: gemini-3-flash-preview")
except:
    model = genai.GenerativeModel('gemini-pro')
    print("[*] Menggunakan model: Gemini Pro")

def buat_artikel():
    print(f"[*] Robot mulai bekerja untuk tanggal {datetime.now().strftime('%d %B %Y')}...")
    prompt = "Tulis artikel blog menarik tentang tren teknologi AI masa depan dalam bahasa Indonesia. Judul di baris pertama, lalu isi artikel. Jangan pakai markdown."
    
    try:
        response = model.generate_content(prompt)
        teks = response.text.split('\n')
        judul = teks[0].replace('#', '').strip()
        konten = '\n'.join(teks[1:]).strip()
        
        file_path = 'data.json'
        data = json.load(open(file_path)) if os.path.exists(file_path) else []
        data.append({"title": judul, "content": konten, "date": datetime.now().strftime("%d %B %Y")})
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
            
        os.system('git add . && git commit -m "Update artikel" && git push')
        print(f"[V] Berhasil! Artikel '{judul}' sudah tayang.")
    except Exception as e:
        print(f"[X] Masalah: {e}")

if __name__ == "__main__":
    buat_artikel()

