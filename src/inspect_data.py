from pathlib import Path
import json
import re
from collections import Counter


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Dataset folders
QAS_DIR = PROJECT_ROOT / "data" / "raw" / "qas"
IMAGES_DIR = PROJECT_ROOT / "data" / "raw" / "images"
OCR_DIR = PROJECT_ROOT / "data" / "raw" / "ocr"

TRAIN_FILE = QAS_DIR / "train_v1.0_withQT.json"

# Load the training annotations
with open(TRAIN_FILE, "r", encoding="utf-8") as file:
    dataset = json.load(file)

records = dataset["data"]

print("Dataset name:", dataset.get("dataset_name"))
print("Dataset version:", dataset.get("dataset_version"))
print("Dataset split:", dataset.get("dataset_split"))
print("Number of questions:", len(records))

# Count images and documents
unique_images = {record["image"] for record in records}
unique_documents = {record["docId"] for record in records}

print("Number of unique images:", len(unique_images))
print("Number of unique documents:", len(unique_documents))

# Count question types
question_type_counts = Counter()

for record in records:
    for question_type in record.get("question_types", []):
        question_type_counts[question_type] += 1

print("\nQuestion types:")
for question_type, count in question_type_counts.most_common():
    print(f"  {question_type}: {count}")


def normalize_text(text):
    """Make text easier to compare."""
    text = text.lower()
    return re.sub(r"[^a-z0-9]+", "", text)


# Inspect the specific example you provided
target_filename = "ffbf0023_4.png"

matching_records = [
    record
    for record in records
    if Path(record["image"]).name == target_filename
]

print("\nMatching Q&A records for:", target_filename)
print("Number of matching questions:", len(matching_records))

image_path = IMAGES_DIR / target_filename
ocr_path = OCR_DIR / "ffbf0023_4.json"

print("Image exists:", image_path.exists())
print("OCR file exists:", ocr_path.exists())

# Load OCR data
with open(ocr_path, "r", encoding="utf-8") as file:
    ocr_data = json.load(file)

recognition_results = ocr_data.get("recognitionResults", [])

ocr_lines = []

for page in recognition_results:
    for line in page.get("lines", []):
        ocr_lines.append(line.get("text", ""))

ocr_text = "\n".join(ocr_lines)
normalized_ocr_text = normalize_text(ocr_text)

print("Number of OCR lines:", len(ocr_lines))
print("\nFirst five OCR lines:")

for line in ocr_lines[:5]:
    print(" ", line)

print("\nQuestions and answer checks:")

for record in matching_records:
    question = record["question"]
    answers = record.get("answers", [])

    print("\nQuestion ID:", record["questionId"])
    print("Question:", question)
    print("Answers:", answers)

    for answer in answers:
        answer_found = normalize_text(answer) in normalized_ocr_text
        print(f"Answer found in OCR ({answer}):", answer_found)