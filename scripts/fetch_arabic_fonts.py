import urllib.request
import os
import sys

FONTS_DIR = "/home/omar_alnemr04/vault/raw/assets/fonts"
os.makedirs(FONTS_DIR, exist_ok=True)

# Curated high-aesthetic Arabic Google & Open-Source fonts with identical rounded & display calligraphy
FONT_URLS = {
    "Marhey-Rounded-Display.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/marhey/Marhey%5Bwght%5D.ttf",
    "Beiruti-Modern-Script.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/beiruti/Beiruti%5Bwght%5D.ttf",
    "ReemKufi-Calligraphic.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/reemkufi/ReemKufi%5Bwght%5D.ttf",
    "Amiri-Quranic-Calligraphy.ttf": "https://raw.githubusercontent.com/aliftype/amiri/master/Amiri-Regular.ttf",
    "Changa-Modern-Bold.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/changa/Changa%5Bwght%5D.ttf"
}

def download_fonts():
    downloaded = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for filename, url in FONT_URLS.items():
        dest = os.path.join(FONTS_DIR, filename)
        if not os.path.exists(dest) or os.path.getsize(dest) == 0:
            print(f"Downloading {filename}...")
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as resp:
                    with open(dest, "wb") as f:
                        f.write(resp.read())
                downloaded.append(dest)
                print(f"Successfully downloaded: {filename} ({os.path.getsize(dest)} bytes)")
            except Exception as e:
                print(f"Failed to download {filename}: {e}")
        else:
            downloaded.append(dest)
            print(f"Already present: {filename}")
    return downloaded

if __name__ == "__main__":
    download_fonts()
