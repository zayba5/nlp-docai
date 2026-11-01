import argparse
import json
import re
from pathlib import Path

from rank_bm25 import BM25Okapi


def tokenize(text):
    return re.findall(r"[a-z0-9]+", str(text).lower())


def normalize(text):
    return " ".join(tokenize(text))


def load_questions(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["data"] if isinstance(data, dict) else data


def get_ocr_lines(ocr_data):
    # Official DocVQA OCR format
    if "recognitionResults" in ocr_data:
        results = ocr_data["recognitionResults"]

        if results:
            return [
                line.get("text", "")
                for line in results[0].get("lines", [])
                if line.get("text", "").strip()
            ]

    # Alternative OCR format
    if "lines" in ocr_data:
        return [
            line.get("text", "")
            for line in ocr_data["lines"]
            if isinstance(line, dict) and line.get("text", "").strip()
        ]

    return []


def find_ocr_file(ocr_dir, image_name):
    image_stem = Path(image_name).stem

    direct_path = ocr_dir / f"{image_stem}.json"

    if direct_path.exists():
        return direct_path

    matches = list(ocr_dir.rglob(f"{image_stem}.json"))

    return matches[0] if matches else None


def make_chunks(lines, chunk_size=80, overlap=20):
    words = []

    for line in lines:
        words.extend(line.split())

    if not words:
        return []

    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(words), step):
        chunk = words[start:start + chunk_size]

        if not chunk:
            break

        chunks.append(" ".join(chunk))

        if start + chunk_size >= len(words):
            break

    return chunks


def answer_is_in_text(answers, text):
    text = normalize(text)

    for answer in answers:
        if normalize(answer) in text:
            return True

    return False


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--qas", required=True)
    parser.add_argument("--ocr-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--limit", type=int, default=None)

    args = parser.parse_args()

    qas_path = Path(args.qas)
    ocr_dir = Path(args.ocr_dir)
    output_path = Path(args.output)

    questions = load_questions(qas_path)

    if args.limit is not None:
        questions = questions[:args.limit]

    print(f"Loaded questions: {len(questions)}")

    # Build one corpus from the validation document pages
    image_names = sorted({
        item["image"]
        for item in questions
    })

    corpus = []

    for image_name in image_names:
        ocr_file = find_ocr_file(ocr_dir, image_name)

        if ocr_file is None:
            print(f"OCR file not found: {image_name}")
            continue

        with open(ocr_file, "r", encoding="utf-8") as file:
            ocr_data = json.load(file)

        lines = get_ocr_lines(ocr_data)
        chunks = make_chunks(lines)

        for chunk_number, chunk_text in enumerate(chunks):
            corpus.append({
                "image": image_name,
                "chunk_number": chunk_number,
                "text": chunk_text
            })

    if not corpus:
        raise RuntimeError(
            "No OCR chunks were created. Check the OCR directory path."
        )

    print(f"Built corpus chunks: {len(corpus)}")

    tokenized_corpus = [
        tokenize(chunk["text"])
        for chunk in corpus
    ]

    bm25 = BM25Okapi(tokenized_corpus)

    retrieval_k = [1, 5, 10]
    evidence_hits = {k: 0 for k in retrieval_k}
    page_hits = {k: 0 for k in retrieval_k}

    predictions = []

    for number, item in enumerate(questions, start=1):
        question = item["question"]
        gold_image = item["image"]
        answers = item.get("answers", [])

        if not isinstance(answers, list):
            answers = [answers]

        scores = bm25.get_scores(tokenize(question))

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True
        )

        ranked_chunks = [
            corpus[index]
            for index in ranked_indices
        ]

        for k in retrieval_k:
            top_chunks = ranked_chunks[:k]

            page_found = any(
                chunk["image"] == gold_image
                for chunk in top_chunks
            )

            evidence_found = any(
                chunk["image"] == gold_image
                and answer_is_in_text(answers, chunk["text"])
                for chunk in top_chunks
            )

            if page_found:
                page_hits[k] += 1

            if evidence_found:
                evidence_hits[k] += 1

        predictions.append({
            "question_id": item.get("questionId"),
            "question": question,
            "gold_image": gold_image,
            "answers": answers,
            "top_results": ranked_chunks[:5]
        })

        if number % 100 == 0:
            print(f"Processed {number}/{len(questions)} questions")

    total = len(questions)

    metrics = {
        "num_questions": total,
        "num_corpus_chunks": len(corpus),
        "page_recall": {
            f"Recall@{k}": page_hits[k] / total
            for k in retrieval_k
        },
        "evidence_recall": {
            f"Recall@{k}": evidence_hits[k] / total
            for k in retrieval_k
        }
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            {
                "metrics": metrics,
                "predictions": predictions
            },
            file,
            indent=2
        )

    print("\nBM25 baseline finished.")
    print(json.dumps(metrics, indent=2))
    print(f"Saved results to: {output_path}")


if __name__ == "__main__":
    main()