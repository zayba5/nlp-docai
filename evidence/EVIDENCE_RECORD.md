# Evidence Record

## 1. Dataset Verification

**Dataset:** SP-DocVQA  
**Dataset Version:** 1.0  
**Verification Date:** October 31, 2026

The project uses the three official SP-DocVQA partitions for baseline development, validation, and evaluation.

| Partition | Questions | Documents | Images | Answers |
|---|---:|---:|---:|---|
| Training | 39,463 | 10,194 | 10,194 | Available |
| Validation | 5,349 | 1,286 | 1,286 | Available |
| Test | 5,188 | 1,287 | 1,287 | Not included |
| **Total** | **50,000** | **12,767** | **12,767** | — |

The complete dataset contains:
- 50,000 question records.
- 12,767 unique document IDs.
- 12,767 unique document-page images.

Training and validation contain answer labels. Test answers are not available locally, so answer-based test evaluation cannot currently be performed.

## 2. Relationship Between Dataset Files

The dataset consists of three connected components:

| Component | Location | Contents |
|---|---|---|
| Images | `data/raw/images/` | Original document-page images |
| OCR | `data/raw/ocr/` | Extracted text, words, lines, coordinates, and confidence values |
| QAS | `data/raw/qas/` | Questions, answers, image names, document IDs, and question types |

Each QAS record identifies a question, its answer, and the associated document image. The matching OCR file is located using the same base filename.

For example, a QAS record contains:
- Question: What is the corporation name?
- Answer: USA Petroleum
- Image: `documents/ffbf0023_4.png`
- Document ID: `3278`

The corresponding local files are:
- Image: `data/raw/images/ffbf0023_4.png`
- OCR: `data/raw/ocr/ffbf0023_4.json`

The relationship between the files is:
- One document image corresponds to one expected OCR file.
- One document image can be referenced by multiple QAS question records.
- Each QAS record connects a question and its answer to the corresponding document image.
- The image and OCR files provide visual and machine-readable information about the same document page.

### 2.1 Question-to-Image Relationship

The dataset has a many-to-one relationship between questions and images. One document page can have several associated questions. Therefore, the number of questions is greater than the number of unique images.

For example, `ffbf0023_4.png` has three associated questions:

| Question ID | Question | Answer |
|---:|---|---|
| 9951 | When is the contract effective date? | `7 - 1 - 99` |
| 9952 | What is the type of organization? | `Corporation` |
| 9953 | What is the corporation name? | `USA Petroleum` |

All three questions reference the same image and OCR files:
- `data/raw/images/ffbf0023_4.png`
- `data/raw/ocr/ffbf0023_4.json`

This explains why the dataset contains 50,000 questions but only 12,767 unique images.

### 2.2 Count Calculations

The total number of questions is calculated by adding the three QAS partitions:

- Training: 39,463
- Validation: 5,349
- Test: 5,188

**Total questions:**

39,463 + 5,349 + 5,188 = **50,000**

The total number of unique images is calculated by adding the unique images in each partition:

- Training: 10,194
- Validation: 1,286
- Test: 1,287

**Total unique images:**

10,194 + 1,286 + 1,287 = **12,767**

The same calculation applies to the unique document IDs:

10,194 + 1,286 + 1,287 = **12,767 unique document IDs**

In the verified QAS metadata, the number of unique document IDs and unique image names is the same within each partition.

### 2.3 Average Questions per Image

The average number of questions per image is calculated by dividing the number of questions by the number of unique images.

| Partition | Calculation | Average Questions per Image |
|---|---|---:|
| Training | 39,463 / 10,194 | 3.87 |
| Validation | 5,349 / 1,286 | 4.16 |
| Test | 5,188 / 1,287 | 4.03 |
| **Complete Dataset** | **50,000 / 12,767** | **3.92** |

These values are averages. Individual images may have one question or several questions.

### 2.4 Image-to-OCR Relationship

Each document image is expected to have one corresponding OCR file with the same base filename.

For example:
- Image: `ffbf0023_4.png`
- OCR: `ffbf0023_4.json`

The expected relationship is one image to one OCR file.

Based on the QAS metadata, the expected total is approximately:
- 12,767 image files.
- 12,767 matching OCR files.

The physical image and OCR folder counts should be verified separately. These totals are based on unique image names and document IDs in the QAS metadata.

## 3. Dataset Partition Organization

The images and OCR files remain together in their original raw-data folders. They are not physically moved into separate training, validation, and test folders.

Instead, the QAS partition determines the logical assignment of each question and its associated document.

| Partition | QAS Source File | Questions | Unique Documents | Unique Images | Answers |
|---|---|---:|---:|---:|---|
| Training | `train_v1.0_withQT.json` | 39,463 | 10,194 | 10,194 | Available |
| Validation | `val_v1.0_withQT.json` | 5,349 | 1,286 | 1,286 | Available |
| Test | `test_v1.0.json` | 5,188 | 1,287 | 1,287 | Not included |
| **Total** | — | **50,000** | **12,767** | **12,767** | — |

### 3.1 Partition Proportions

The question distribution is:

| Partition | Percentage |
|---|---:|
| Training | 78.93% |
| Validation | 10.70% |
| Test | 10.38% |

The image distribution is:

| Partition | Percentage |
|---|---:|
| Training | 79.85% |
| Validation | 10.07% |
| Test | 10.08% |

The difference between question and image percentages occurs because different document images have different numbers of associated questions.

## 4. Partition Overlap Verification

The official partitions were checked for document and image overlap.

**Document overlap:**

| Partition Comparison | Overlapping Documents |
|---|---:|
| Training vs. Validation | 0 |
| Training vs. Test | 0 |
| Validation vs. Test | 0 |

**Image overlap:**

| Partition Comparison | Overlapping Images |
|---|---:|
| Training vs. Validation | 0 |
| Training vs. Test | 0 |
| Validation vs. Test | 0 |

No document-level or image-level overlap was identified between the three partitions.

This separation helps prevent data leakage caused by the same document appearing in multiple partitions.

## 5. OCR Inspection and Data Quality

The sample image `ffbf0023_4.png` was matched with its corresponding OCR file:

- Image: `data/raw/images/ffbf0023_4.png`
- OCR: `data/raw/ocr/ffbf0023_4.json`

The OCR file contained:
- 83 text lines.
- Word-level OCR information.
- Line-level OCR information.
- Word-level and line-level bounding boxes.
- OCR confidence values.

Three associated questions were checked against the extracted OCR text.

| Result | Count |
|---|---:|
| Associated questions inspected | 3 |
| Answers found directly in OCR text | 2 |
| Answers not found through simple string matching | 1 |

The answers `Corporation` and `USA Petroleum` were found directly in the OCR text.

The date answer `7 - 1 - 99` was not found through simple string matching. Possible reasons include:
- Differences in spacing.
- Different punctuation.
- OCR recognition errors.

This demonstrates that extracted OCR text may not always accurately represent information visible in the original document. This limitation is relevant to the project's comparison of text-based retrieval and layout-aware document question answering.

## 6. Baseline Evaluation Protocol

The project compares the following methods using the same fixed validation partition.

| Baseline | Purpose | Input |
|---|---|---|
| BM25 | Text-based retrieval baseline | OCR text and question |
| Visual baseline | Pretrained document question-answering comparison | Document image and question |
| Layout-aware method | Proposed approach investigating spatial information | OCR text, coordinates, and question |

The dataset partitions are used as follows:

- **Training:** Used for development and fitting learned components when required.
- **Validation:** Used for baseline comparison, development decisions, and model selection.
- **Test:** Reserved for final evaluation. Answer labels are not available locally.

All baseline methods will follow the same evaluation protocol and primary metric to ensure a fair comparison.

## 7. Frozen Evaluation Split

The project uses the official SP-DocVQA version 1.0 partitions:

- Training: `train_v1.0_withQT.json`
- Validation: `val_v1.0_withQT.json`
- Test: `test_v1.0.json`

The split manifest is saved at:

`splits/docvqa_official_split.json`

It records:
- Question IDs.
- Document IDs.
- Image filenames.
- Source QAS files.
- Partition assignments and counts.

The split is frozen to ensure consistent comparisons between baseline methods.

Raw images and OCR files are not moved or modified. Any necessary changes to the evaluation protocol will be documented, with the original version preserved and affected experiments rerun.

## 8. Reproducibility Evidence

The project package should contain:
- Runnable baseline source code or notebooks.
- Configuration and dependency information.
- Frozen split manifest.
- Baseline results and evaluation outputs.
- Runtime and hardware information.
- Teammate rerun results.

Each baseline result should record:
- Baseline and run IDs.
- Dataset and split version.
- Configuration and seed, where applicable.
- Evaluation count.
- Primary metric name and value.
- Runtime and hardware.
- Output file locations.

A teammate rerun should verify that the baselines can be executed using the provided instructions and produce consistent results.

## 9. Summary of Evidence

| Verification Item | Result |
|---|---|
| Dataset | SP-DocVQA v1.0 |
| Total questions | 50,000 |
| Unique document images | 12,767 |
| Unique document IDs | 12,767 |
| Training questions | 39,463 |
| Validation questions | 5,349 |
| Test questions | 5,188 |
| Training images | 10,194 |
| Validation images | 1,286 |
| Test images | 1,287 |
| Average questions per image | 3.92 |
| Expected image-to-OCR relationship | 1:1 |
| Document overlap | 0 |
| Image overlap | 0 |
| Sample OCR lines inspected | 83 |
| Sample questions inspected | 3 |
| Direct OCR answer matches | 2 |
| Unmatched OCR answers | 1 |
| Frozen split manifest | `splits/docvqa_official_split.json` |

## 10. Conclusion

The SP-DocVQA dataset provides the foundation for the project's baseline evaluation.

The dataset contains 50,000 questions associated with 12,767 unique document-page images, with an average of approximately 3.92 questions per image. Each image is expected to have one corresponding OCR file identified through its base filename.

The official training, validation, and test partitions were checked, with no document-level or image-level overlap identified.

The sample OCR inspection demonstrated that OCR extraction can introduce recognition and formatting errors. This limitation is relevant to the comparison between text-based retrieval and layout-aware document question answering.

These findings support proceeding with the BM25 and visual baselines before evaluating the proposed layout-aware method using the frozen evaluation protocol.