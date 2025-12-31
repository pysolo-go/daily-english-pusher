# Screenshot Solver Plugin

This tool allows you to automatically extract questions from screenshots and get answers using AI.

## Prerequisites

1.  **Python 3.8+**
2.  **Tesseract OCR**: This is required for text extraction.
    *   **macOS**: `brew install tesseract tesseract-lang`
    *   **Windows**: Download installer from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
    *   **Linux**: `sudo apt install tesseract-ocr tesseract-ocr-chi-sim`

## Installation

1.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Set up API Key:
    *   Copy `.env.example` to `.env`
    *   Add your OpenAI API Key: `OPENAI_API_KEY=sk-...`

## Usage

### 1. Process specific image
```bash
python main.py /path/to/image.png
```

### 2. Process all images in `input_images` folder
Place your screenshots in the `input_images` folder and run:
```bash
python main.py
```

## How it works
1.  **OCR**: Uses Tesseract to read text from the image (supports English + Simplified Chinese).
### 3. Interactive Mode (Screenshot & Solve)
Run this command to interactively select a region on your screen (macOS) or take a full screenshot (Windows/Linux) and get the answer immediately:
```bash
python interactive_mode.py
```

