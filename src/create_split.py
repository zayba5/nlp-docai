from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]

QAS_DIR = PROJECT_ROOT / "data" / "raw" / "qas"
SPLIT_DIR = PROJECT_ROOT / "splits"
SPLIT_DIR.mkdir(exist_ok=True)

files = {
    "train": "train_v1.0_withQT.json",
    "validation": "val_v1.0_withQT.json",
    "test": "test_v1.0.json",
}

manifest = {
    "dataset": "SP-DocVQA",
    "version": "1.0",
    "split_policy": "Official DocVQA partitions",
    "partitions": {}
}

for split_name, filename in files.items():
    file_path = QAS_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    records = dataset["data"]

    question_ids = [
        record["questionId"]
        for record in records
        if "questionId" in record
    ]

    document_ids = sorted({
        str(record["docId"])
        for record in records
        if record.get("docId") is not None
    })

    image_names = sorted({
        Path(record["image"]).name
        for record in records
        if record.get("image")
    })

    manifest["partitions"][split_name] = {
        "source_file": filename,
        "question_count": len(records),
        "document_count": len(document_ids),
        "image_count": len(image_names),
        "question_ids": question_ids,
        "document_ids": document_ids,
        "image_names": image_names,
    }

output_path = SPLIT_DIR / "docvqa_official_split.json"

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(manifest, file, indent=2)

print(f"Created: {output_path}")

for split_name, details in manifest["partitions"].items():
    print(
        f"{split_name}: "
        f"{details['question_count']} questions, "
        f"{details['document_count']} documents, "
        f"{details['image_count']} images"
    )