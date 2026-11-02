import argparse
import json
import re
from pathlib import Path

from rank_bm25 import BM25Okapi


def tokenize(text):
    return re.findall(r"[a-z0-9]+", str(text).lower())


def load_questions(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["data"] if isinstance(data, dict) else data


def get_ocr_lines(ocr_data):
    if "recognitionResults" in ocr_data:
        results = ocr_data["recognitionResults"]

        if results:
            return [
                line.get("text", "")
                for line in results[0].get("lines", [])
                if line.get("text", "").strip()
            ]

    if "lines" in ocr_data:
        return [
            line.get("text", "")
            for line in ocr_data["lines"]
            if isinstance(line, dict)
            and line.get("text", "").strip()
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
    if overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be smaller than chunk size."
        )

    words = []

    for line in lines:
        words.extend(line.split())

    if not words:
        return []

    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(words), step):
        chunk_words = words[start:start + chunk_size]

        if not chunk_words:
            break

        chunks.append(" ".join(chunk_words))

        if start + chunk_size >= len(words):
            break

    return chunks


def answer_is_in_text(answers, text):
    text_tokens = tokenize(text)

    for answer in answers:
        answer_tokens = tokenize(answer)

        if not answer_tokens:
            continue

        answer_length = len(answer_tokens)

        for start in range(
            len(text_tokens) - answer_length + 1
        ):
            candidate_tokens = text_tokens[
                start:start + answer_length
            ]

            if candidate_tokens == answer_tokens:
                return True

    return False


def build_page_index(
    image_name,
    ocr_dir,
    chunk_size,
    chunk_overlap
):
    ocr_file = find_ocr_file(ocr_dir, image_name)

    if ocr_file is None:
        raise FileNotFoundError(
            f"OCR file not found for image: {image_name}"
        )

    with open(ocr_file, "r", encoding="utf-8") as file:
        ocr_data = json.load(file)

    lines = get_ocr_lines(ocr_data)

    page_chunks_text = make_chunks(
        lines,
        chunk_size=chunk_size,
        overlap=chunk_overlap
    )

    if not page_chunks_text:
        raise RuntimeError(
            f"No OCR chunks found for image: {image_name}"
        )

    page_chunks = [
        {
            "image": image_name,
            "chunk_number": chunk_number,
            "text": chunk_text
        }
        for chunk_number, chunk_text in enumerate(page_chunks_text)
    ]

    tokenized_chunks = [
        tokenize(chunk["text"])
        for chunk in page_chunks
    ]

    bm25 = BM25Okapi(tokenized_chunks)

    return page_chunks, bm25


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Page-specific BM25 baseline for "
            "Single-Page DocVQA"
        )
    )

    parser.add_argument(
        "--qas",
        required=True,
        help="Path to the QAS JSON file"
    )

    parser.add_argument(
        "--ocr-dir",
        required=True,
        help="Directory containing OCR JSON files"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path for the output JSON file"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional number of questions for a smoke test"
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=80,
        help="Number of words per OCR chunk"
    )

    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=20,
        help="Number of overlapping words between chunks"
    )

    args = parser.parse_args()

    qas_path = Path(args.qas)
    ocr_dir = Path(args.ocr_dir)
    output_path = Path(args.output)

    questions = load_questions(qas_path)

    if args.limit is not None:
        questions = questions[:args.limit]

    print(f"Loaded questions: {len(questions)}")

    retrieval_k = [1, 5, 10]
    evidence_hits = {k: 0 for k in retrieval_k}

    page_cache = {}
    predictions = []

    for number, item in enumerate(questions, start=1):
        question = item.get("question", "")
        gold_image = item.get("image")
        answers = item.get("answers", [])

        if not question or not gold_image:
            raise ValueError(
                f"Question {number} is missing a question or image."
            )

        if not isinstance(answers, list):
            answers = [answers]

        if not answers:
            raise ValueError(
                f"Question {number} has no answer labels."
            )

        if gold_image not in page_cache:
            page_cache[gold_image] = build_page_index(
                image_name=gold_image,
                ocr_dir=ocr_dir,
                chunk_size=args.chunk_size,
                chunk_overlap=args.chunk_overlap
            )

        page_chunks, bm25 = page_cache[gold_image]

        scores = bm25.get_scores(tokenize(question))

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True
        )

        ranked_chunks = [
            {
                **page_chunks[index],
                "score": float(scores[index])
            }
            for index in ranked_indices
        ]

        for k in retrieval_k:
            top_chunks = ranked_chunks[:k]

            evidence_found = any(
                answer_is_in_text(
                    answers,
                    chunk["text"]
                )
                for chunk in top_chunks
            )

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
            print(
                f"Processed {number}/{len(questions)} questions"
            )

    total_questions = len(questions)
    total_page_chunks = sum(
        len(page_chunks)
        for page_chunks, _ in page_cache.values()
    )

    metrics = {
        "task": "single_page_docvqa",
        "search_scope": "question_associated_page",
        "num_questions_loaded": total_questions,
        "num_questions_evaluated": total_questions,
        "num_unique_pages": len(page_cache),
        "num_total_page_chunks": total_page_chunks,
        "average_chunks_per_page": (
            total_page_chunks / len(page_cache)
            if page_cache else 0.0
        ),
        "chunk_size_words": args.chunk_size,
        "chunk_overlap_words": args.chunk_overlap,
        "evidence_recall": {
            f"Recall@{k}": evidence_hits[k] / total_questions
            for k in retrieval_k
        }
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output = {
        "baseline": "BM25",
        "metrics": metrics,
        "predictions": predictions
    }

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\nBM25 page-specific baseline finished.")
    print(json.dumps(metrics, indent=2))
    print(f"Saved results to: {output_path}")


if __name__ == "__main__":
    main()