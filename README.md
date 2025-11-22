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

- **Batch Processing:**  
  Scalable for thousands of records—tested up to 50k with threading.

- **Discogs-Ready Export:**  
  Generates artist/album CSV for upload/import in Discogs bulk listing tools.

***

## Repo Structure

```
RECORDS2DISCOGS/
├── ml-mobileclip/          # MobileCLIP vision model, weights, utilities
│   ├── models/             # Downloaded model weights (e.g. MobileCLIP2-L-14)
│   └── ...                 # CLIP code, transforms
├── vinyl-record-indexing/  # Main orchestration pipeline
│   ├── app.py              # Entry point for webcam capture + AI record identification
│   └── ...                 # CSV, configs, utils
```

***

## Installation

1. **Clone the repo:**
    ```bash
    git clone https://github.com/olosnoks/RECORDS2DISCOGS.git
    cd RECORDS2DISCOGS
    ```

2. **Install dependencies:**
    ```bash
    pip install -r ml-mobileclip/requirements.txt
    ```

3. **Download model weights:**
    - **MobileCLIP:**  
      Place checkpoints in `ml-mobileclip/models/`
      - Example: `mobileclip_s0.pt`, `MobileCLIP2-L-14.pt`, etc.
    - **LLaVA (Vision Language Models):**  
      Use LM Studio to download and load models.

4. **Verify Python path/module install:**
    ```bash
    cd ml-mobileclip
    pip install -e .
    ```

***

## Usage

1. **Start LM Studio**
    - Load compatible multimodal vision model.
    - Confirm server available at `http://localhost:1234/v1/chat/completions`.

2. **Run the main pipeline:**
    ```bash
    cd vinyl-record-indexing
    python app.py
    ```

3. **Feed your vinyl covers to the webcam.**
    - **Label buffer** prevents false positives.
    - **Open palm** gesture breaks acquisition loop.

4. **Output:**
    - Record covers saved to `/vinyls/`
    - Artist/title inference auto-runs in threads.
    - Results CSV (`results.csv`) exported—ready for Discogs bulk upload.

***

## Architecture

| Module                        | Purpose                                                     |
|-------------------------------|-------------------------------------------------------------|
| **MobileCLIP (ml-mobileclip)**| Vision encoding, image deduplication                        |
| **LLaVA via LM Studio**       | Captioning, OCR, artist/album extraction                    |
| **app.py (vinyl-indexing)**   | Orchestrates webcam, AI, batch processing, CSV output       |
| **ThreadPoolExecutor**        | Accelerates inference for large batches                     |

***

## Technical Guide (for devs)

- **Batch Size:**  
  Optimized for up to 50-record batches; memory safe on consumer GPUs (RTX 4050/4060).
- **Modular AI:**  
  Swap models or checkpoints at will—no code lock-in.
- **Local-Only:**  
  No OpenAI/remote API dependency. Your data never leaves your box.

***

## Troubleshooting

- **Imports fail?**  
  Double-check PYTHONPATH or use editable install: `pip install -e ml-mobileclip/`
- **LM Studio not reachable?**  
  Make sure port is correct and model is loaded (check LM Studio GUI/logs).
- **Accuracy low?**  
  Switch to higher-tier models (LLaVA-13B), check input image quality.

***

## Acknowledgements

- [MobileCLIP (Apple CVPR 2024)](https://github.com/apple/ml-mobileclip) — Official implementation
- [LLaVA](https://github.com/haotian-liu/LLaVA) — Open source multimodal LLM
- [Discogs API & CSV tools](https://www.discogs.com/developers/) — Bulk listing workflows

***

## Roadmap

- [ ] Direct Discogs API integration (optional)
- [ ] Post-processing for genre/condition lookup
- [ ] Non-technical UI for record store owners (TBD)

***

## License  
See LICENSE for details.
  
***
