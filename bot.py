import os, requests, datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENCLAW_API_KEY")
BASE_URL = os.getenv("OPENCLAW_BASE_URL").strip().rstrip('/')
BLOG_ID = os.getenv("BLOG_ID")

def buat_artikel():
    full_url = f"{BASE_URL}/chat/completions"
    print(f"[*] Menghubungi AI...")
    
    judul = "Update Tren: " + str(datetime.date.today())
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": f"Tulis artikel blog SEO bahasa Indonesia tentang {judul}. Gunakan format HTML (pakai <p>, <h3>, <b>)."}],
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(full_url, json=data, headers=headers, timeout=60)
        if response.status_code == 200:
            isi_artikel = response.json()['choices'][0]['message']['content']
            
            # --- SIMPAN LOKAL (Untuk Netlify) ---
            os.makedirs("artikel", exist_ok=True)
            with open("artikel/konten-terbaru.md", "w", encoding="utf-8") as f:
                f.write(f"---\ntitle: {judul}\n---\n\n{isi_artikel}")
            print("[v] File lokal berhasil diperbarui.")

            # --- KIRIM KE BLOGGER ---
            # Catatan: Bagian ini butuh file client_secrets.json atau API Key Blogger
            # Untuk tahap awal, pastikan file lokal aman dulu.
            print(f"[!] Artikel siap diposting ke Blog ID: {BLOG_ID}")
            
        else:
            print(f"[x] Error AI: {response.status_code}")
    except Exception as e:
        print(f"[x] Error: {e}")

if __name__ == "__main__":
    buat_artikel()
