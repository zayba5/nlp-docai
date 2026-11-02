import json, zipfile
from pathlib import Path

qas_path = "data/raw/qas/val_v1.0_withQT.json"
qas = json.load(open(qas_path))["data"]
names = sorted({Path(q["image"]).name for q in qas})   # "documents/xxx.png" -> "xxx.png"

with zipfile.ZipFile("val_images.zip", "w", zipfile.ZIP_DEFLATED) as z:
    z.write(qas_path, "qas/val.json")
    for n in names:
        z.write(f"data/raw/images/{n}", f"images/{n}")

print(len(names), "images zipped")