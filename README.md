# RECORDS2DISCOGS

**Automated Vinyl Record Indexing & Discogs Bulk Upload Toolkit Powered by Local AI**

***

## Overview

This project automates the *identification, cataloging, and bulk uploading* of your entire vinyl collection to Discogs—up to scale.  
It combines local computer vision (MobileCLIP), multimodal AI (LLaVA via LM Studio), and Discogs-ready data output.  
**No cloud APIs, no vendor lock-in—100% local inference and privacy.**

***

## Features

- **Local Computer Vision:**  
  MobileCLIP image encoder for efficient, privacy-safe identification.

- **AI-Powered Captioning:**  
  LLaVA (7B, 13B) via LM Studio for text+image labeling and record recognition.

- **Automated Capture:**  
  Webcam loop records vinyl covers as they're presented, no manual cropping.

- **Deduplication:**  
  Cosine similarity checks to prevent duplicate images in batch runs.

- **Discogs-Ready Export:**  
  Generates artist/album CSV for upload/import in Discogs bulk listing tools.

- **Automated Cleanup:**  
  `cleanup.py` script consolidates batches, archives runs, and maintains master catalog.

***

## Repo Structure

```
RECORDS2DISCOGS/
├── indexing-output/              # All output management centralized here
│   ├── csv-backups/              # Timestamped batch archives
│   │   ├── batch_20251121_200530.csv
│   │   └── batch_20251121_201245.csv
│   ├── cleanup.py                # Batch cleanup automation script
│   └── master.csv                # Master consolidated catalog of all records
├── ml-mobileclip/                # MobileCLIP vision model (submodule)
│   ├── models/                   # Downloaded model weights (e.g. MobileCLIP2-L-14)
│   └── ...                       # CLIP code, transforms
├── vinyl-record-indexing/        # Main orchestration pipeline (submodule)
│   ├── app.py                    # Entry point for webcam capture + AI record ID
│   └── ...                       # (output.csv and vinyls/ created during runs)
├── .gitmodules
├── LICENSE
└── README.md
```

***

## Installation

1. **Clone the repo:**
    ```
    git clone --recursive https://github.com/olosnoks/RECORDS2DISCOGS.git
    cd RECORDS2DISCOGS
    ```

2. **Install dependencies:**
    ```
    pip install -r ml-mobileclip/requirements.txt
    ```

3. **Download model weights:**
    - **MobileCLIP:**  
      Place checkpoints in `ml-mobileclip/models/`
      - Example: `mobileclip_s0.pt`, `MobileCLIP2-L-14.pt`, etc.
    - **LLaVA (Vision Language Models):**  
      Use LM Studio to download and load models.

4. **Verify Python path/module install:**
    ```
    cd ml-mobileclip
    pip install -e .
    ```

***

## Usage

### 1. Start LM Studio
- Load compatible multimodal vision model.
- Confirm server available at `http://localhost:1234/v1/chat/completions`.

### 2. Run the main pipeline:
```
cd vinyl-record-indexing
python app.py
```

### 3. Feed your vinyl covers to the webcam.
- **Label buffer** prevents false positives.
- **Open palm** gesture breaks acquisition loop.

### 4. Output:
- Record covers saved to `vinyl-record-indexing/vinyls/`
- Artist/title inference auto-runs in threads.
- Results written to `vinyl-record-indexing/output.csv`

### 5. After each batch run, clean up and consolidate:
```
cd ../indexing-output
python cleanup.py
```

**What `cleanup.py` does:**
1. ✅ **Backs up** the batch CSV to `indexing-output/csv-backups/batch_TIMESTAMP.csv`
2. ✅ **Appends** all records to `indexing-output/master.csv` (your complete catalog)
3. ✅ **Deletes** `vinyl-record-indexing/output.csv` (after backup)
4. ✅ **Deletes** `vinyl-record-indexing/vinyls/` folder (temporary images no longer needed)
5. ✅ Prepares `vinyl-record-indexing/` for the next batch run

**Final output:**
- `indexing-output/csv-backups/` contains timestamped archives of each batch
- `indexing-output/master.csv` contains your complete consolidated catalog—ready for Discogs bulk upload
- `vinyl-record-indexing/` is clean and ready for the next run

### Workflow Summary:
```
# Run batch indexing
cd vinyl-record-indexing
python app.py

# Cleanup and consolidate
cd ../indexing-output
python cleanup.py

# Repeat for next batch!
```

***

## Architecture

| Module                        | Purpose                                                     |
|-------------------------------|-------------------------------------------------------------|
| **MobileCLIP (ml-mobileclip)**| Vision encoding, image deduplication                        |
| **LLaVA via LM Studio**       | Captioning, OCR, artist/album extraction                    |
| **app.py (vinyl-indexing)**   | Orchestrates webcam, AI, batch processing, CSV output       |
| **cleanup.py (indexing-output)** | Batch management, archival, master catalog consolidation |
| **ThreadPoolExecutor**        | Accelerates inference for large batches                     |

***

## Technical Guide (for devs)

- **Batch Size:**  
  Optimized for up to 50-record batches; memory safe on consumer GPUs (RTX 4050/4060).
- **Modular AI:**  
  Swap models or checkpoints at will—no code lock-in.
- **Local-Only:**  
  No OpenAI/remote API dependency. Your data never leaves your box.
- **Batch Management:**  
  `cleanup.py` automates the post-run workflow: backup → consolidate → clean. Safe for 50k+ records.
- **Centralized Output:**  
  All output management (backups, master catalog, cleanup) lives in `indexing-output/` for clean organization.

***

## Models Used

### Computer Vision: MobileCLIP
- **Model:** MobileCLIP-S0 and MobileCLIP2-L-14
- **Purpose:** Image encoding for efficient vinyl cover identification
- **Source:** [Apple ML-MobileCLIP](https://github.com/apple/ml-mobileclip)
- **Performance:** Processes images in ~100ms on CPU

### Language Model: LLaVA (via LM Studio)
- **Models:** LLaVA 7B and 13B (multimodal vision-language)
- **Purpose:** Text+image understanding for record metadata extraction
- **Recommended:**
  - 7B for faster processing (4-5 records/min)
  - 13B for higher accuracy on obscure releases

### Why Local Models?
- **Privacy:** Your vinyl collection data stays on your machine
- **Cost:** No API fees for processing 50k+ records
- **Speed:** Batch processing without rate limits
- **Offline:** Works without internet after initial setup

***

## Troubleshooting

- **Imports fail?**  
  Double-check PYTHONPATH or use editable install: `pip install -e ml-mobileclip/`
- **LM Studio not reachable?**  
  Make sure port is correct and model is loaded (check LM Studio GUI/logs).
- **Accuracy low?**  
  Switch to higher-tier models (LLaVA-13B), check input image quality.
- **Cleanup script fails?**  
  Verify `vinyl-record-indexing/output.csv` exists before running cleanup. Check file permissions.

***

## Acknowledgements

- [MobileCLIP (Apple CVPR 2024)](https://github.com/apple/ml-mobileclip) — Official implementation
- [LLaVA](https://github.com/haotian-liu/LLaVA) — Open source multimodal LLM
- [vinyl-record-indexing](https://github.com/capjamesg/vinyl-record-indexing) by James G — Original inspiration
- [Discogs API & CSV tools](https://www.discogs.com/developers/) — Bulk listing workflows

***

## Roadmap

- [x] Automated batch cleanup and consolidation
- [ ] Direct Discogs API integration (optional)
- [ ] Post-processing for genre/condition lookup
- [ ] Non-technical UI for record store owners (TBD)

***

## License  
See LICENSE for details.
  
***
