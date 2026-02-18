import os
import json
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
import time

# 1. Load Konfigurasi
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[!] Error: API Key tidak ditemukan di .env")
    exit()

# Gunakan model terbaru yang ada di daftar kamu
MODEL_NAME = 'models/gemini-3-flash-preview' 

genai.configure(api_key=api_key)
model = genai.GenerativeModel(MODEL_NAME)

def buat_artikel_viral():
    hari_ini = datetime.now().strftime('%d %B %Y')
    print(f"[*] Robot AI sedang memantau tren viral untuk {hari_ini}...")
    
    # Prompt super detail untuk hasil 1500-2000 kata & gaya manusia
    prompt = f"""Tulis sebuah artikel blog long-form yang sangat mendalam, personal, dan provokatif mengenai tren teknologi atau fenomena digital yang sedang viral hari ini, {hari_ini}. 

    TARGET PANJANG: Minimal 1500-2000 kata.
    
    STRUKTUR & GAYA BAHASA:
    1. JUDUL: Buat judul yang sangat menggoda (clickbait cerdas), tanpa tanda kutip atau hashtag di baris pertama.
    2. GAYA PENULISAN: Gunakan gaya 'Narrative Journalism' seperti penulis majalah Wired atau Vice. Sangat luwes, manusiawi, penuh opini tajam, sedikit humor, dan emosional.
    3. PENDAHULUAN (HOOK): Mulai dengan sebuah keresahan atau skenario nyata yang sedang terjadi saat ini. Jangan kaku.
    4. PEMBAHASAN: 
       - Hubungkan tren viral hari ini dengan masa depan AI di tahun 2026.
       - Jangan gunakan banyak poin-poin (bullet points). Gunakan paragraf naratif yang panjang dan mengalir.
       - Masukkan analogi-analogi unik agar pembaca awam pun paham.
       - Bedah sisi gelap dan sisi terang dari fenomena ini.
    5. OPINI PRIBADI (POV): Tulis seolah-olah kamu (penulis) punya posisi kuat terhadap isu ini.
    6. PENUTUP: Berikan kesimpulan yang puitis dan meninggalkan kesan mendalam bagi pembaca.

    PENTING: Gunakan bahasa Indonesia yang modern, hindari istilah robotik seperti 'pertama-tama', 'selain itu', 'kesimpulannya'. Biarkan tulisan mengalir seperti percakapan intelektual di sebuah kafe. Jika tulisan hampir selesai namun belum mencapai target kata, gali lebih dalam bagian dampaknya terhadap psikologi manusia."""

    try:
        # Mengatur konfigurasi generasi agar memberikan output maksimal
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=8192, # Memaksa AI memberikan teks sepanjang mungkin
                temperature=0.9,       # Membuat tulisan lebih kreatif dan tidak kaku
            )
        )
        
        full_text = response.text.strip()
        baris = full_text.split('\n')
        
        # Mengambil judul dari baris pertama
        judul = baris[0].replace('*', '').replace('#', '').strip()
        # Mengambil sisa teks sebagai konten
        konten = '\n'.join(baris[1:]).strip()
        
        if len(konten) < 500:
            print("[!] Peringatan: Hasil tulisan mungkin terlalu pendek. Mencoba optimasi...")

        # 2. Simpan ke data.json
        file_path = 'data.json'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []

        data.append({
            "title": judul,
            "content": konten,
            "date": hari_ini
        })

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # 3. Push ke GitHub
        print("[*] Mengunggah artikel ke GitHub...")
        os.system('git add .')
        os.system(f'git commit -m "Update Artikel Viral: {judul[:30]}..."')
        os.system('git push')

        print("-" * 50)
        print(f"[V] BERHASIL!")
        print(f"[V] Judul: {judul}")
        print(f"[V] Panjang: {len(konten.split())} kata")
        print("-" * 50)

    except Exception as e:
        print(f"[X] Gagal membuat artikel: {e}")

if __name__ == "__main__":
    buat_artikel_viral()
