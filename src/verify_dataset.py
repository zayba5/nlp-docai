from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
QAS_DIR = PROJECT_ROOT / "data" / "raw" / "qas"

files = [
    "train_v1.0_withQT.json",
    "val_v1.0_withQT.json",
    "test_v1.0.json",
]

all_doc_ids = {}
all_image_names = {}

for filename in files:
    file_path = QAS_DIR / filename

    if not file_path.exists():
        print(f"\nMISSING: {filename}")
        continue

    with open(file_path, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    records = dataset.get("data", [])

    doc_ids = {
        str(record.get("docId"))
        for record in records
        if record.get("docId") is not None
    }

    image_names = {
        Path(record["image"]).name
        for record in records
        if record.get("image")
    }

    records_with_answers = sum(
        1 for record in records
        if record.get("answers")
    )

    print(f"\n{filename}")
    print(f"Questions: {len(records)}")
    print(f"Unique documents: {len(doc_ids)}")
    print(f"Unique images: {len(image_names)}")
    print(f"Records with answers: {records_with_answers}")

    all_doc_ids[filename] = doc_ids
    all_image_names[filename] = image_names

print("\nDocument overlap checks:")

filenames = list(all_doc_ids.keys())

for i in range(len(filenames)):
    for j in range(i + 1, len(filenames)):
        first = filenames[i]
        second = filenames[j]

        overlap = all_doc_ids[first] & all_doc_ids[second]

        print(f"{first} vs {second}: {len(overlap)} overlapping documents")

print("\nImage overlap checks:")

for i in range(len(filenames)):
    for j in range(i + 1, len(filenames)):
        first = filenames[i]
        second = filenames[j]

        overlap = all_image_names[first] & all_image_names[second]

        print(f"{first} vs {second}: {len(overlap)} overlapping images")