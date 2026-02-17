import os, requests, datetime, random
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENCLAW_API_KEY")
BASE_URL = os.getenv("OPENCLAW_BASE_URL").strip().rstrip('/')

def buat_artikel():
    full_url = f"{BASE_URL}/chat/completions"
    hari_ini = datetime.date.today().strftime("%d %B %Y")
    
    print(f"[*] Robot sedang menganalisis tren viral untuk {hari_ini}...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Instruksi super detail agar artikel panjang dan berkualitas
    prompt = f"""Bertindaklah sebagai Jurnalis Teknologi Senior. Hari ini adalah {hari_ini}. 
    Tulis artikel blog yang SANGAT MENDALAM (Minimal 2000 kata) tentang tren teknologi yang paling VIRAL/TRENDING saat ini.
    
    Struktur Artikel Wajib:
    1. Judul yang Bombastis & SEO Friendly (Gunakan HTML <h1>).
    2. Pendahuluan yang memikat tentang mengapa topik ini viral.
    3. Minimal 7 Sub-judul (Gunakan <h3>) yang membahas detail teknis, dampak sosial, dan sisi ekonomi.
    4. Gunakan list (<ul><li>) untuk poin-poin penting.
    5. Analisis mendalam minimal 5 paragraf per sub-judul.
    6. Kesimpulan dan Prediksi Masa Depan di tahun 2027.
    
    Format: Gunakan HTML murni tanpa Markdown. 
    Bahasa: Indonesia yang luwes, profesional, dan kaya kosakata.
    Target: 2000+ Kata."""

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4000,
        "temperature": 0.9,
        "presence_penalty": 0.6,
        "frequency_penalty": 0.5
    }
    
    try:
        # Timeout dinaikkan ke 300 detik karena memproses 2000 kata butuh waktu lama
        response = requests.post(full_url, json=data, headers=headers, timeout=300)
        
        if response.status_code == 200:
            isi_artikel = response.json()['choices'][0]['message']['content']
            
            # Pilih gambar acak bertema teknologi agar tidak bosan
            img_id = random.randint(100, 1000)
            url_gambar = f"https://picsum.photos/id/{img_id}/1200/600"
            
            header_gambar = f'''
            <div style="text-align:center; margin-bottom:30px;">
                <img src="{url_gambar}" style="width:100%; border-radius:15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);" alt="Trending Technology">
                <p style="font-style:italic; color:#7f8c8d; margin-top:10px;">Visualisasi Tren Masa Depan - {hari_ini}</p>
            </div>
            '''
            
            os.makedirs("artikel", exist_ok=True)
            with open("artikel/konten-terbaru.md", "w", encoding="utf-8") as f:
                f.write(f"{header_gambar}\n\n{isi_artikel}")
            
            print(f"[v] BERHASIL! Artikel panjang 2000 kata tentang tren {hari_ini} telah siap.")
            
        else:
            print(f"[x] Gagal menghubungi AI. Status: {response.status_code}")
            print(f"Pesan Error: {response.text}")
            
    except Exception as e:
        print(f"[x] Terjadi kesalahan sistem: {e}")

if __name__ == "__main__":
    buat_artikel()
