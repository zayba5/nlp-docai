
# Evidence Record

## Dataset Verification

**Dataset:** SP-DocVQA  
**Dataset version:** 1.0  
**Verification date:** October 31, 2026

The project uses three official DocVQA partitions.

| Partition | Questions | Documents | Images | Answers |
|---|---:|---:|---:|---|
| Training | 39,463 | 10,194 | 10,194 | Available |
| Validation | 5,349 | 1,286 | 1,286 | Available |
| Test | 5,188 | 1,287 | 1,287 | Not included |

The total dataset contains **50,000 questions and 12,767 document images**.

## File Relationships

Each question record in the QAS files points to a document image using its image filename.

For example:

```text
QAS record:
Question: What is the corporation name?
Image: documents/ffbf0023_4.png
Answer: USA Petroleum

The corresponding local files are:
data/raw/images/ffbf0023_4.png
data/raw/ocr/ffbf0023_4.json

The image file contains the document page. The OCR file contains the text extracted from that page, along with word and line coordinates.
```

## Verification Results

The training, validation, and test partitions were checked for document and image overlap.

### Document Overlap Results

| Partition Comparison | Overlapping Documents |
|---|---:|
| Training vs. Validation | 0 |
| Training vs. Test | 0 |
| Validation vs. Test | 0 |

### Image Overlap Results

The image overlap checks also found zero overlapping images between all partitions.

| Partition Comparison | Overlapping Images |
|---|---:|
| Training vs. Validation | 0 |
| Training vs. Test | 0 |
| Validation vs. Test | 0 |

### Verification Conclusion

This indicates that the official dataset partitions are separated and do not contain document-level leakage.

No overlapping documents or images were identified between the training, validation, and test partitions.

## OCR Inspection (example)

The sample document `ffbf0023_4.png` was successfully matched with its OCR file.

The page contained **83 OCR text lines and three associated questions**.

### OCR Answer Matching Results

| Result | Count |
|---|---:|
| Associated questions | 3 |
| Answers found directly in OCR text | 2 |
| Answers not found through simple string matching | 1 |

Two answers were found directly in the OCR text.

One date answer was not found through simple string matching, likely because OCR formatting differed from the answer format.

This demonstrates a realistic OCR limitation that will be considered during error analysis.

## Summary of Evidence

| Verification Item | Result |
|---|---|
| Dataset | SP-DocVQA |
| Dataset version | 1.0 |
| Total questions | 50,000 |
| Total document images | 12,767 |
| Training questions | 39,463 |
| Validation questions | 5,349 |
| Test questions | 5,188 |
| Document overlap | 0 |
| Image overlap | 0 |
| Sample OCR document | ffbf0023_4.png |
| OCR text lines inspected | 83 |
| Associated questions inspected | 3 |
| Direct OCR answer matches | 2 |
| Answers not directly matched | 1 |


The SP-DocVQA dataset partitions were checked for document-level and image-level overlap. No overlapping documents or images were identified between the training, validation, and test partitions.

The sample OCR inspection confirmed that the document image and its corresponding OCR file were correctly matched. Two of the three associated answers were found directly in the OCR text, while one date answer was not identified through simple string matching.

These findings provide evidence of dataset partition separation and demonstrate an OCR text-matching limitation that will be considered during subsequent error analysis.

## Frozen Evaluation Split

The project uses the official SP-DocVQA version 1.0 partitions:

- Training: `train_v1.0_withQT.json`
- Validation: `val_v1.0_withQT.json`
- Test: `test_v1.0.json`

The official partitions were checked for document and image overlap. No overlap was found.

The split manifest was saved at:

```text
splits/docvqa_official_split.json
