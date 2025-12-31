import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")

if not API_KEY:
    print("Error: OPENAI_API_KEY not found in .env file.")
    exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def generate_vocab_image():
    csv_path = "/Users/solo/Desktop/work/trae.ai/ai/street_english_app/vocabulary.csv"
    
    if not os.path.exists(csv_path):
        print(f"Error: File not found at {csv_path}")
        return

    try:
        df = pd.read_csv(csv_path)
        
        # User requested: "OK，就用这种方法，每次取五个单词，依次生图，把6-20单词取出生图"
        # Strategy: Loop through words 6-20 in batches of 5.
        # Use specific prompts and layouts for each batch to ensure quality.
        # Fallback to a generic grid if no config exists.
        
        # Define batches: start_index (0-based) -> config
        # Words 6-20 correspond to indices 5-19 (inclusive) in 0-based indexing.
        # Batch 1: 5-9 (Words 6-10)
        # Batch 2: 10-14 (Words 11-15)
        # Batch 3: 15-19 (Words 16-20)
        
        batches = [
            (5, 10),
            (10, 15),
            (15, 20)
        ]
        
        # Configuration for specific batches to ensure high quality layouts
        batch_configs = {
            5: {
                "name": "words_6_10_earth_layers",
                "prompt": (
                    "A scientific diagram of Earth's structure. "
                    "Layout: Vertical cross-section showing the Core at the bottom, Mantle in the middle, Crust at the surface, and Sky at the top. "
                    "Style: Clean vector art, educational, flat design, no text."
                ),
                "labels": [
                    # Words: oxide(5-wrong? No, wait), carbon dioxide, hydrogen, core, crust, mantle
                    # Let's check the words in the loop dynamically, but here is the plan:
                    # 0: carbon dioxide (Sky)
                    # 1: hydrogen (Sky)
                    # 2: core (Bottom)
                    # 3: crust (Surface/Top of rock)
                    # 4: mantle (Middle)
                    # Wait, the order in DF is: 
                    # 5: oxide (Wait, let's check CSV content from previous turns)
                    # Previous turn: 0-4 were atmosphere, hydrosphere, lithosphere, oxygen, oxide.
                    # So 5 is 'carbon dioxide', 6 is 'hydrogen'...
                    # Let's assume standard order and map by index in the batch (0-4).
                    
                    # Batch 0 (idx 5): carbon dioxide -> Sky Left
                    {"x": 250, "y": 150, "color": "#E0F7FA"},
                    # Batch 1 (idx 6): hydrogen -> Sky Right
                    {"x": 774, "y": 150, "color": "#E0F7FA"},
                    # Batch 2 (idx 7): core -> Bottom Center
                    {"x": 512, "y": 900, "color": "#FFCCBC"}, 
                    # Batch 3 (idx 8): crust -> Surface
                    {"x": 512, "y": 400, "color": "#D7CCC8"},
                    # Batch 4 (idx 9): mantle -> Middle
                    {"x": 512, "y": 650, "color": "#FFAB91"}
                ]
            },
            10: {
                "name": "words_11_15_geography",
                "prompt": (
                    "A landscape scene with a globe overlay. "
                    "Layout: Split composition. Left side features a large Globe with grid lines. "
                    "Right side features a landscape with a clear Horizon and a high mountain peak. "
                    "Style: Clean vector art, educational, flat design, no text."
                ),
                "labels": [
                    # Words: longitude, latitude, horizon, altitude, disaster
                    # 0: longitude (Globe)
                    {"x": 250, "y": 250, "color": "white"},
                    # 1: latitude (Globe)
                    {"x": 250, "y": 600, "color": "white"},
                    # 2: horizon (Landscape Line)
                    {"x": 750, "y": 500, "color": "white"},
                    # 3: altitude (Mountain Peak/Sky)
                    {"x": 750, "y": 200, "color": "white"},
                    # 4: disaster (Maybe a crack or storm?) -> Let's put it bottom right
                    {"x": 750, "y": 800, "color": "#FFCDD2"}
                ]
            },
            15: {
                "name": "words_16_20_disasters",
                "prompt": (
                    "A comic strip style layout with 5 distinct panels showing different danger scenarios. "
                    "Layout: Top row has 3 panels, Bottom row has 2 panels. "
                    "Scenes: 1. Minor accident. 2. Huge explosion. 3. Flood. 4. Person in danger. 5. Ticking bomb. "
                    "Style: Clean vector art, educational, flat design, no text."
                ),
                "labels": [
                    # Words: mishap, catastrophic, calamity, endanger, jeopardise
                    # 0: mishap (Top Left)
                    {"x": 170, "y": 250, "color": "white"},
                    # 1: catastrophic (Top Center)
                    {"x": 512, "y": 250, "color": "red"},
                    # 2: calamity (Top Right)
                    {"x": 854, "y": 250, "color": "white"},
                    # 3: endanger (Bottom Left)
                    {"x": 340, "y": 750, "color": "white"},
                    # 4: jeopardise (Bottom Right)
                    {"x": 684, "y": 750, "color": "white"}
                ]
            }
        }

        import requests
        from PIL import Image, ImageDraw, ImageFont
        from io import BytesIO

        # Try to load font once
        try:
            font_path = "/System/Library/Fonts/Helvetica.ttc"
            if not os.path.exists(font_path):
                 font_path = "/Library/Fonts/Arial.ttf"
            font_large = ImageFont.truetype(font_path, 50)
            font_medium = ImageFont.truetype(font_path, 40)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()

        for start_idx, end_idx in batches:
            batch_df = df.iloc[start_idx:end_idx].reset_index(drop=True)
            print(f"\nProcessing batch {start_idx+1}-{end_idx}...")
            print(batch_df[['word', 'meaning']])
            
            config = batch_configs.get(start_idx)
            if not config:
                print(f"No config for batch starting at {start_idx}, skipping...")
                continue
                
            prompt_text = config["prompt"] + " IMPORTANT: NO TEXT. NO LABELS."
            image_save_path = f"/Users/solo/Desktop/work/trae.ai/ai/street_english_app/{config['name']}.png"
            
            print(f"Generating background for {config['name']}...")
            
            try:
                # Generate Image
                response = client.images.generate(
                    model="black-forest-labs/FLUX.1-schnell",
                    prompt=prompt_text,
                    size="1024x1024",
                    n=1,
                )
                image_url = response.data[0].url
                print(f"Background generated: {image_url}")
                
                # Download and Process
                img_data = requests.get(image_url).content
                image = Image.open(BytesIO(img_data))
                draw = ImageDraw.Draw(image)
                width, height = image.size
                
                # Overlay Labels
                for i, row in batch_df.iterrows():
                    word = row['word']
                    # Get label config for this index (0-4)
                    if i < len(config["labels"]):
                        lbl = config["labels"][i]
                        x, y = lbl["x"], lbl["y"]
                        color = lbl.get("color", "white")
                        
                        # Draw centered at x, y
                        # Calculate text size to center it
                        left, top, right, bottom = draw.textbbox((0, 0), word, font=font_large)
                        text_w = right - left
                        text_h = bottom - top
                        
                        draw_x = x - text_w / 2
                        draw_y = y - text_h / 2
                        
                        # Outline
                        outline_color = "black"
                        stroke = 3
                        for ox in range(-stroke, stroke+1):
                            for oy in range(-stroke, stroke+1):
                                if ox == 0 and oy == 0: continue
                                draw.text((draw_x+ox, draw_y+oy), word, font=font_large, fill=outline_color)
                        
                        # Text
                        draw.text((draw_x, draw_y), word, font=font_large, fill=color)
                
                image.save(image_save_path)
                print(f"Saved labeled image: {image_save_path}")
                
            except Exception as e:
                print(f"Error processing batch {start_idx}-{end_idx}: {e}")
        
        # End of batch processing
        return
        
        # Original single-batch code commented out below...
        # Take the first 5 words directly
        target_words = df.head(5)
            
        print("Selected words for programmatically labeled combination:")
        print(target_words[['word', 'meaning']])
        
        # Create a prompt for a CLEAN background
        prompt_text = "A scientific cross-section diagram of Earth's spheres. "
        prompt_text += "Layout: Three distinct horizontal layers.\n"
        prompt_text += "1. Top Layer: Blue sky and clouds (representing Atmosphere).\n"
        prompt_text += "2. Middle Layer: Blue ocean water (representing Hydrosphere).\n"
        prompt_text += "3. Bottom Layer: Underground rock and earth strata (representing Lithosphere).\n"
        prompt_text += "Style: Flat vector art, educational illustration, clean lines, high quality.\n"
        prompt_text += "IMPORTANT: NO TEXT. NO LABELS. CLEAN IMAGE ONLY."
        
        print(f"Generating background image with prompt: {prompt_text[:200]}...")

        # Try SiliconFlow specific models
        model_name = "black-forest-labs/FLUX.1-schnell"
        
        image_save_path = "/Users/solo/Desktop/work/trae.ai/ai/street_english_app/combined_concepts_labeled.png"
        
        try:
            response = client.images.generate(
                model=model_name,
                prompt=prompt_text,
                size="1024x1024",
                n=1,
            )
            
            image_url = response.data[0].url
            print(f"Background image generated successfully: {image_url}")
            
            import requests
            from PIL import Image, ImageDraw, ImageFont
            from io import BytesIO
            
            # Download image
            img_data = requests.get(image_url).content
            image = Image.open(BytesIO(img_data))
            draw = ImageDraw.Draw(image)
            
            # Try to load a font, fall back to default if necessary
            try:
                # macOS default font path
                font_path = "/System/Library/Fonts/Helvetica.ttc"
                if not os.path.exists(font_path):
                     font_path = "/Library/Fonts/Arial.ttf"
                
                # Large font for main layers
                font_large = ImageFont.truetype(font_path, 60)
                # Medium font for sub-elements
                font_medium = ImageFont.truetype(font_path, 40)
            except:
                print("Warning: Custom font not found, using default.")
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()

            # Define labels and approximate positions (for 1024x1024)
            # Coordinates are (x, y). Centered horizontally.
            
            width, height = image.size
            
            def draw_text_centered(text, y, font, color="white", outline="black"):
                # Get text bbox
                left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
                text_width = right - left
                text_height = bottom - top
                x = (width - text_width) / 2
                
                # Draw outline/stroke for visibility
                stroke_width = 3
                draw.text((x-stroke_width, y), text, font=font, fill=outline)
                draw.text((x+stroke_width, y), text, font=font, fill=outline)
                draw.text((x, y-stroke_width), text, font=font, fill=outline)
                draw.text((x, y+stroke_width), text, font=font, fill=outline)
                
                # Draw text
                draw.text((x, y), text, font=font, fill=color)

            # 1. atmosphere (Sky - Top)
            draw_text_centered("atmosphere", 100, font_large)
            
            # 4. oxygen (Sky - slightly lower)
            draw_text_centered("oxygen", 200, font_medium, color="#E0F7FA") # Light cyan

            # 2. hydrosphere (Water - Middle)
            draw_text_centered("hydrosphere", 500, font_large)

            # 3. lithosphere (Rock - Bottom)
            draw_text_centered("lithosphere", 800, font_large)
            
            # 5. oxide (Rock - slightly lower)
            draw_text_centered("oxide", 900, font_medium, color="#FFE0B2") # Light orange
            
            # Save final image
            image.save(image_save_path)
            print(f"Final labeled image saved to: {image_save_path}")
            
        except Exception as e:
            print(f"Error generating image: {e}")
            # Fallback logic removed for brevity as we are focusing on the text overlay fix which requires the image first.
            # If primary generation fails, we should retry or handle gracefully, but the overlay logic is key here.

    except Exception as e:
        print(f"Error processing CSV: {e}")

if __name__ == "__main__":
    generate_vocab_image()
