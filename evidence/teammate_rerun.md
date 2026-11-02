** TEAMMATE RERUN**

Re-ran the BM25 text-only retrieval baseline over the full 5349 validation dataset questions.
With the respective evidence recall scores:
1. Evidence Recall @ 1 : 0.6724621424565339
2. Evidence Recall @ 5 : 0.8870816975135539
3. Evidence Recall @ 10 :  0.8994204524210133

Re-ran the Qwen visual-model baseline in Google Colab, over 15 validation questions from the same 5349 validation question dataset. Due to limited GPU power at the moment, gradually incrementing the validation questions and image for predictions.

Used the exact-match accuracy metric:
- Evaluated questions: 15
- Normalized exact-match accuracy: 60.00%

Examined the results of the run and noticed that some predictions that were marked false for exact-match were correct but genrated in a different format

1. "prediction": "1128 Sixteenth St., N.W., Washington, D.C. 20036",
    "answers": [
      "1128 SIXTEENTH ST., N. W., WASHINGTON, D. C. 20036",
      "1128 sixteenth st., N. W., washington, D. C. 20036"
    ],

2. "prediction": "THE ROBERT A. WELCH FOUNDATION",
    "answers": [
      "The Robert A. Welch Foundation"
    ],

3. "prediction": "$ 975.00",
    "answers": [
      "$975.00",
      "975.00"
    ],

As a result, the evaluation metric score seems low, but the model generates the right output. We will incorporate the ANLS metric- that measures textual similarity- next over the full validation set, once we get higher GPU power.