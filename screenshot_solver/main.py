import os
import sys
import time
from typing import Optional
from dotenv import load_dotenv
from PIL import Image, ImageGrab
import pytesseract
import openai

# Load environment variables
# Try to load from the project root first, then current directory
root_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
if os.path.exists(root_env_path):
    load_dotenv(root_env_path)
else:
    load_dotenv()

import base64

# Configure OpenAI API Key
# You can set this in a .env file: OPENAI_API_KEY=sk-...
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

if api_key:
    client = openai.OpenAI(api_key=api_key, base_url=base_url)
else:
    client = None
    print("Warning: OPENAI_API_KEY not found in environment variables. Answering will be disabled.")

import io

import re

def clean_latex_to_text(text):
    """
    Post-processing to remove LaTeX commands and convert to readable text.
    """
    if not text:
        return text

    # 1. Remove standard delimiters and sizing commands
    text = text.replace('\\[', '').replace('\\]', '')
    text = text.replace('\\(', '').replace('\\)', '')
    # Remove \left and \right but keep the brackets/parentheses
    text = re.sub(r'\\left', '', text)
    text = re.sub(r'\\right', '', text)
    
    # Remove environments like \begin{cases} ... \end{cases}
    # We remove the tags but keep the content.
    # Also handle standard LaTeX newlines (\\) and alignment tabs (&)
    text = re.sub(r'\\begin\{[^}]+\}', '', text)
    text = re.sub(r'\\end\{[^}]+\}', '', text)
    text = text.replace(r'\\', '\n')
    text = text.replace('&', ' ')

    # 2. Common Math Symbols (Order matters! specific commands before general prefixes)
    replacements = [
        (r'\\sum', '∑'),
        (r'\\prod', '∏'),
        (r'\\int', '∫'),
        (r'\\partial', '∂'),
        (r'\\infty', '∞'),
        (r'\\approx', '≈'),
        (r'\\neq', '≠'),
        (r'\\cdot', '·'),
        (r'\\var', 'D'), # Convert \var to D for Variance
        (r'\\Var', 'D'),
        # Use word boundary or negative lookahead to prevent \le matching \left (if \left wasn't already removed)
        (r'\\le(?![a-zA-Z])', '≤'), 
        (r'\\ge(?![a-zA-Z])', '≥'),
        (r'\\pm', '±'),
        (r'\\times', '×'),
        (r'\\div', '÷'),
        (r'\\theta', 'θ'),
        (r'\\alpha', 'α'),
        (r'\\beta', 'β'),
        (r'\\gamma', 'γ'),
        (r'\\lambda', 'λ'),
        (r'\\mu', 'μ'),
        (r'\\sigma', 'σ'),
        (r'\\pi', 'π'),
        (r'\\Delta', 'Δ'),
        # Use Unicode combining characters for accents
        # \u0302 is combining circumflex accent (hat)
        (r'\\hat\{(\w)\}', r'\1' + '\u0302'),  # \hat{x} -> x̂
        # \u0304 is combining macron (bar)
        (r'\\bar\{(\w)\}', r'\1' + '\u0304'),  # \bar{x} -> x̄
        (r'\\overline\{(\w+)\}', r'\1' + '\u0304'), # Handle overline same as bar for single letters
    ]

    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)

    # 3. Handle Fractions: \frac{a}{b} -> (a)/(b)
    # Support up to 2 levels of nested braces for common cases like \frac{x^{2}}{2}
    # Allow optional spaces after \frac and between arguments
    nested_content = r'(?:[^{}]|(?:\{[^{}]*\}))*'
    text = re.sub(r'\\frac\s*\{(' + nested_content + r')\}\s*\{(' + nested_content + r')\}', r'(\1)/(\2)', text)
    # Run again to handle nested fractions
    text = re.sub(r'\\frac\s*\{(' + nested_content + r')\}\s*\{(' + nested_content + r')\}', r'(\1)/(\2)', text)

    # 4. Handle Subscripts/Superscripts
    text = re.sub(r'_\{([^{}]+)\}', r'_\1', text)
    text = re.sub(r'\^\{([^{}]+)\}', r'^\1', text)

    # 5. Clean remaining braces for commands like \text, \boxed, \mathbf
    text = re.sub(r'\\[a-zA-Z]+\s*\{(' + nested_content + r')\}', r'\1', text)
    
    # 6. Remove remaining spacing commands
    text = re.sub(r'\\[,;!:]', ' ', text)
    
    # 7. Final Cleanup: Remove any remaining LaTeX commands (\cmd) and braces
    # We carefully remove \words but keep the text.
    # If a backslash is followed by letters, it's likely a command we missed.
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    # Remove leftover braces
    text = text.replace('{', '').replace('}', '')
    # Remove stray backslashes
    text = text.replace('\\', '')

    return text.strip()

def encode_image(image_path):
    # Resize image if too large to speed up upload and processing
    with Image.open(image_path) as img:
        # Calculate new size maintaining aspect ratio
        # Increased to 2048 to preserve details for math formulas (subscripts, superscripts)
        max_size = 2048
        if img.width > max_size or img.height > max_size:
            img.thumbnail((max_size, max_size))
        
        # Save to buffer
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

class ScreenshotSolver:
    def __init__(self, tesseract_cmd: Optional[str] = None):
        """
        Initialize the solver.
        :param tesseract_cmd: Path to tesseract executable if not in PATH.
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_text(self, image_path: str = None, image_obj: Image.Image = None) -> str:
        """
        Extract text from an image path or PIL Image object using OCR.
        """
        if image_path:
            try:
                img = Image.open(image_path)
            except Exception as e:
                return f"Error opening image: {e}"
        elif image_obj:
            img = image_obj
        else:
            return "No image provided."

        print("Extracting text from image...")
        try:
            # Using chi_sim for Simplified Chinese + English
            # Use --psm 6 (Assume a single uniform block of text) for better accuracy on screenshots
            custom_config = r'--psm 6' 
            text = pytesseract.image_to_string(img, lang='chi_sim+eng', config=custom_config)
            
            # If text is too short, try again with default psm
            if len(text.strip()) < 5:
                 text = pytesseract.image_to_string(img, lang='chi_sim+eng')
                 
            return text.strip()
        except pytesseract.TesseractNotFoundError:
            return "Error: Tesseract is not installed or not in your PATH. Please install it."
        except Exception as e:
            return f"OCR Error: {e}"

    def solve(self, image_path: str) -> str:
        """
        End-to-end solver: tries Vision API first, falls back to OCR + LLM.
        """
        if not client:
            return "Error: OpenAI client not initialized. Please set OPENAI_API_KEY."
            
        # Determine strategy based on provider
        is_siliconflow = "siliconflow" in str(client.base_url)
        is_openai = "api.openai.com" in str(client.base_url)
        
        # Strategy 1: Vision API (Best for Math)
        # We prefer Vision for Math because OCR often mangles formulas.
        if is_siliconflow or is_openai:
            try:
                print("Attempting to use Vision API for better math accuracy...")
                return self.get_answer_via_vision(image_path)
            except Exception as e:
                print(f"Vision API failed ({e}), falling back to OCR...")
        
        # Strategy 2: OCR + Text LLM (Fallback)
        text = self.extract_text(image_path=image_path)
        if not text or "Error" in text:
            return f"Failed to extract text: {text}"
            
        return self.get_answer(text)

    def get_answer_via_vision(self, image_path: str) -> str:
        """
        Send image directly to LLM (GPT-4o / Qwen-VL).
        """
        base64_image = encode_image(image_path)
        
        # Select Vision Model
        model_name = "gpt-4o"
        if "siliconflow" in str(client.base_url):
            # SiliconFlow supports Qwen2-VL
            model_name = "Qwen/Qwen2-VL-72B-Instruct" 
        
        print(f"Using Vision Model: {model_name}")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert math tutor. The user has provided a screenshot of a math problem. "
                        "Your task is to **visually recognize** the problem and provide the correct answer in a **clear, step-by-step format**.\n\n"
                        "**CRITICAL INSTRUCTION: PURE INDEPENDENT CALCULATION**\n"
                         "- Treat the image ONLY as a source of the **PROBLEM STATEMENT** (numbers and operators).\n"
                         "- **COMPLETELY IGNORE** any results, answers, or handwriting shown after the equals sign.\n"
                         "- **DO NOT** mention or refute the wrong answer in the image. Just provide the **CORRECT** calculation.\n"
                         "- **GOAL**: Provide the mathematically precise result derived from first principles.\n\n"
                         "**Process:**\n"
                         "1. **Extract**: Read the expression on the left side (e.g., `1/6 + 1/3 + 1/6`).\n"
                         "2. **Calculate**: Perform the math step-by-step in your internal chain of thought.\n"
                         "3. **Verify**: Double-check every arithmetic step. (e.g. `1/6 + 2/6 + 1/6 = 4/6 = 2/3`).\n"
                         "4. **Output**: Present the correct derivation and final answer.\n\n"
                         "**Crucial Output Requirement:**\n"
                         "- **USE LATEX** for all mathematical expressions.\n"
                         "- Wrap inline math in single dollar signs, e.g., $x^2$.\n"
                         "- Wrap block math (centered) in double dollar signs, e.g., $$ \\frac{a}{b} $$.\n"
                         "- Ensure the text explanation is clear and concise.\n"
                         "- Use **Chinese** for all text explanations.\n"
                         "- **Variance Notation**: Use $D(X)$ for variance, NOT $Var(X)$ or $var(X).\n"
                         "- **Multiplication**: Use $\\times$ or $\\cdot$, do not use `*`.\n"
                         "- **Formatting**: Do NOT use Markdown headers (lines starting with #). Use **bold** for titles.\n\n"
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            temperature=0.1,
        )
        content = response.choices[0].message.content
        return content

    def get_answer(self, question: str) -> str:
        """
        Send the question to an LLM to get the answer.
        """
        if not client:
            return "Error: OpenAI client not initialized. Please set OPENAI_API_KEY."

        if not question:
            return "Error: Empty question text."

        print(f"Searching answer for: {question[:50]}...")
        
        try:
            # Check if base_url indicates SiliconFlow or DeepSeek to use compatible models
            model_name = "gpt-4o"
            if "siliconflow" in str(client.base_url):
                 model_name = "Qwen/Qwen2.5-7B-Instruct" # A reliable, fast model on SiliconFlow
            elif "deepseek" in str(client.base_url):
                 model_name = "deepseek-chat"

            response = client.chat.completions.create(
                model=model_name,
                messages = [
            {
                "role": "system", 
                "content": (
                    "You are an expert tutor. The user will provide a question extracted from a screenshot. "
                    "Your task is to provide the correct answer in a **clear, step-by-step, textbook-style format**.\n\n"
                    "**Process:**\n"
                    "1. **Analyze**: Carefully parse the question text.\n"
                    "2. **Chain of Thought**: Solve the problem step-by-step. Verify your logic and calculations explicitly.\n"
                    "3. **Self-Correction**: If your result seems odd, re-calculate.\n"
                    "4. **Answer**: Provide the final result clearly.\n\n"
                    "**Formatting Requirements:**\n"
                    "1. **Language**: ALWAYS answer in Chinese (Simplified).\n"
                    "2. **Multiple Choice**: If it is a multiple choice question, explicitly state the correct option.\n"
                    "3. **Structure**: Use clear headers for each step (e.g., '一、计算期望', '二、结论').\n"
                    "4. **Math Symbols (STRICT)**: ABSOLUTELY NO LaTeX code like '\\frac', '\\sqrt', '\\int', '\\left', '\\right', '\\[', '\\]'. Use plain text ONLY.\n"
                    "   - Use Unicode characters for math symbols (e.g., '∫', '²', '³', 'θ', 'π', '≈', '≠', '×', '÷', '·'). \n"
                    "   - Use '/' for fractions (e.g., '1/2').\n"
                    "   - Use '√' for square roots.\n"
                    "   - Use '^' for exponents if superscripts aren't available.\n"
                    "   - **Variance**: Use `D(X)` notation, NOT `Var(X)`.\n"
                    "5. **Layout**: Separate steps with newlines. Align equations where possible.\n"
                    "6. **Style**: Be concise but rigorous. Do not include conversational filler."
                )
            },
            {"role": "user", "content": f"Question:\n{question}\n\nPlease solve this step-by-step to ensure accuracy. Verify calculations twice. Remember: NO LATEX."}
        ],
                temperature=0.1
            )
            content = response.choices[0].message.content
            return clean_latex_to_text(content)
        except Exception as e:
            return f"API Error: {e}"

    def run_from_file(self, file_path: str):
        print(f"Processing file: {file_path}")
        text = self.extract_text(image_path=file_path)
        print("-" * 20)
        print(f"Extracted Text:\n{text}")
        print("-" * 20)
        
        if text and "Error" not in text:
            answer = self.get_answer(text)
            print(f"Answer:\n{answer}")
        else:
            print("Skipping answer generation due to OCR error or empty text.")

def main():
    solver = ScreenshotSolver()
    
    # Check if a file path is provided as argument
    if len(sys.argv) > 1:
        path_arg = sys.argv[1]
        if os.path.isdir(path_arg):
             print(f"Processing directory: {path_arg}")
             files = [f for f in os.listdir(path_arg) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
             if not files:
                 print("No images found in directory.")
             for f in files:
                 solver.run_from_file(os.path.join(path_arg, f))
                 print("\n" + "="*40 + "\n")
        else:
             solver.run_from_file(path_arg)
    else:
        # Default behavior: look for images in input_images folder
        input_dir = os.path.join(os.path.dirname(__file__), 'input_images')
        files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not files:
            print(f"No images found in {input_dir}. Please add some images or provide a path.")
            return

        for f in files:
            solver.run_from_file(os.path.join(input_dir, f))
            print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    main()
