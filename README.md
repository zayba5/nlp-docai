# NLP DocAI Retrieval

A research-oriented NLP and document-understanding project studying whether document layout information improves question answering and evidence retrieval compared with text-only methods.

## Research Question

> Does incorporating document layout information improve document question answering and evidence retrieval compared with text-only retrieval?

## Dataset

This project uses the **DocVQA Single Page Document Visual Question Answering** dataset.

The dataset contains:

- Document-page images
- Natural-language questions
- Human-provided answers
- OCR text
- Word- and line-level coordinates
- Document identifiers
- Question types

Official sources:

- [DocVQA Dataset](https://www.docvqa.org/datasets/docvqa)
- [RRC Download Portal](https://rrc.cvc.uab.es/?ch=17)

The required dataset is available under:

**Task 1 – Single Page Document Visual Question Answering**

The raw dataset files are stored locally and are not committed to this repository.

## Approximate Dataset Size

The DocVQA Task 1 dataset contains approximately:

- **50,000 questions**
- **12,767 document-page images**
- **Approximately 12,767 OCR JSON files**
- **Three main annotation files**:
  - Training data
  - Validation data
  - Test data

| Component | Approximate contents |
|---|---|
| `spdocvqa_qas` | Approximately 50,000 questions, answers, document IDs, and question types |
| `spdocvqa_images` | Approximately 12,767 PNG document-page images |
| `spdocvqa_ocr` | OCR text and word/line coordinates for the document images |

These numbers are approximate. The exact counts used in the final experiments will be verified programmatically and recorded in the evidence record.

## Task Definition

Given a document page and a natural-language question, the system predicts the answer and identifies relevant document text or regions when reliable evidence information is available.

### Inputs

At prediction time, the system may use:

- Document images
- OCR text
- OCR word or line coordinates
- The question

Reference answers are used only for training, validation, and evaluation.

### Outputs

The system may produce:

- A predicted answer
- Ranked answer-supporting passages or regions
- Evidence information when reliable evidence annotations are available

## Methods

### Text-Only Baseline

BM25 ranks OCR text passages according to their lexical similarity to the question. This provides a simple and interpretable reference method.

### Strong Visual Baseline

A pretrained document question-answering model will be evaluated as a stronger comparison. This model receives the document image and question and predicts an answer.

This comparison helps determine whether the proposed approach provides value beyond simple text retrieval and an established visual document-understanding model.

### Proposed Layout-Aware Method

The proposed method will incorporate spatial information such as:

- Word coordinates
- Text-region positions
- Spatial grouping
- Document structure
- Relationships between nearby text elements

The layout-aware method will be evaluated using the same questions, documents, splits, and evaluation protocol as the baselines.

### Planned Ablation

A controlled ablation will remove or shuffle layout information while keeping the remaining retrieval process unchanged.

This will help determine whether any performance improvement is specifically caused by layout information.

## Evaluation Protocol

The primary split will be performed at the **document level**. All questions associated with the same document will remain in the same partition to prevent information leakage.

The partitions are:

- **Training/development:** Used to fit learned components when necessary.
- **Validation:** Used for model and parameter selection.
- **Protected test:** Used only for the final fixed evaluation.

The evaluation will use consistent:

- Documents
- Questions
- Preprocessing rules
- Model configurations
- Metrics
- Data boundaries

Possible evaluation metrics include:

- Answer Exact Match
- Answer F1
- Average Normalized Levenshtein Similarity (ANLS)
- Evidence Recall@K
- Mean Reciprocal Rank

If explicit evidence annotations are unavailable, evidence evaluation will use answer-to-OCR alignment or a manually verified subset.

## Error Analysis

The project will analyze performance on:

- Tables
- Forms
- Multi-column pages
- Dense text pages
- OCR-error examples
- Repeated answers
- Complex spatial layouts

The analysis will examine cases where:

- Text-only retrieval succeeds
- The visual baseline succeeds
- The layout-aware method succeeds
- Both methods fail
- The answer is correct but the evidence region is incorrect

## Reproducibility

The project will record:

- Dataset version
- Download date
- Inclusion and exclusion rules
- Document-level split identifiers
- Preprocessing settings
- Model configurations
- Random seeds
- Evaluation commands
- Predictions and metrics

## License and Dataset Usage

The source code in this repository is intended for academic and research purposes.

The DocVQA dataset is governed by the terms provided by the dataset organizers and the original document sources. The raw document images are provided for non-commercial research and educational use.

Raw images, OCR files, annotation archives, and restricted download URLs must not be committed to or redistributed through this repository. Users are responsible for reviewing and following the official dataset terms before downloading or using the data.

## Citation

If you use the DocVQA dataset, please cite:

```bibtex
@InProceedings{mathew2021docvqa,
    author = {Mathew, Minesh and Karatzas, Dimosthenis and Jawahar, C. V.},
    title = {DocVQA: A Dataset for VQA on Document Images},
    booktitle = {Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision},
    year = {2021}
}