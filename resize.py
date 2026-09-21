# resize_images.py — run once from your repo root
from pathlib import Path
from PIL import Image

MAX_DIM = 1800      # longest edge, in pixels
QUALITY = 80         # JPEG quality, 0–100
ROOT = Path("static/Images")

for path in ROOT.rglob("*"):
    if path.suffix.lower() not in (".jpg", ".jpeg", ".png"):
        continue

    img = Image.open(path)
    w, h = img.size
    changed = False

    if max(w, h) > MAX_DIM:
        scale = MAX_DIM / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        changed = True

    if path.suffix.lower() == ".png":
        # AmericanD.png etc — flat artwork doesn't need PNG's
        # transparency support, so convert to JPEG for a big size win
        out = path.with_suffix(".jpg")
        img.convert("RGB").save(out, "JPEG", quality=QUALITY, optimize=True)
        path.unlink()  # remove the old .png
        print(f"{path.name} -> {out.name}")
    else:
        img.save(path, "JPEG", quality=QUALITY, optimize=True)
        print(f"{path.name} resized" if changed else f"{path.name} already small, recompressed")

print("Done.")