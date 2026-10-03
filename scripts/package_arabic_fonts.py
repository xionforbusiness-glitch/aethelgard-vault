import urllib.request
import os
import zipfile

FONTS_DIR = "/home/omar_alnemr04/vault/raw/assets/fonts"
os.makedirs(FONTS_DIR, exist_ok=True)

MORE_FONTS = {
    "ArefRuqaa-Artistic-Ruqah.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/arefruqaa/ArefRuqaa-Regular.ttf",
    "Rakkas-Display-Headline.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/rakkas/Rakkas-Regular.ttf",
    "Katibeh-Poetic-Naskh.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/katibeh/Katibeh-Regular.ttf",
    "Cairo-Modern-Sans.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/cairo/Cairo%5Bslnt%2Cwght%5D.ttf"
}

headers = {"User-Agent": "Mozilla/5.0"}
for fname, url in MORE_FONTS.items():
    dest = os.path.join(FONTS_DIR, fname)
    if not os.path.exists(dest):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                with open(dest, "wb") as f:
                    f.write(r.read())
            print(f"Downloaded: {fname}")
        except Exception as e:
            print(f"Failed {fname}: {e}")

# Create an all-in-one ZIP package for easy 1-click import into CapCut / PixelLab
zip_path = os.path.join(FONTS_DIR, "Arabic_Aesthetic_Display_Fonts_Pack.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for f in os.listdir(FONTS_DIR):
        if f.endswith(".ttf") or f.endswith(".otf"):
            z.write(os.path.join(FONTS_DIR, f), arcname=f)

print(f"Zip created at: {zip_path} ({os.path.getsize(zip_path)} bytes)")
