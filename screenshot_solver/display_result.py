import sys
import os
import re
import io
import tkinter as tk
from tkinter import font
import matplotlib
# Use Agg backend for non-interactive PNG generation (safer/faster)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

import json

# Configure Matplotlib to support Chinese (Arial Unicode MS is standard on macOS)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # Ensure minus signs render correctly

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'window_config.json')

def load_config():
    """Loads window configuration from JSON file."""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
    return {"width": 240, "height": 150}

def save_config(width, height):
    """Saves window configuration to JSON file."""
    try:
        config = {"width": width, "height": height}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Error saving config: {e}")

def close_window(event=None):
    sys.exit()

def render_math_to_image(latex_str, fontsize=14, dpi=150):
    """Renders a LaTeX string to a PIL Image."""
    try:
        # Create a figure
        fig = plt.figure(figsize=(0.1, 0.1), dpi=dpi)
        # Add text
        # We wrap in $ if not present, but our parsing logic splits by $.
        # The parser strips the $ signs.
        fig.text(0, 0, f"${latex_str}$", fontsize=fontsize)
        
        # Save to buffer
        buf = io.BytesIO()
        plt.axis('off')
        
        # Save with tight bbox to crop exactly to the text
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.01, transparent=True)
        plt.close(fig)
        
        buf.seek(0)
        img = Image.open(buf)
        return img
    except Exception as e:
        print(f"Error rendering latex '{latex_str}': {e}")
        plt.close(fig)
        return None

def display_content(text_widget, content):
    """Parses content and inserts text/images into text_widget."""
    # Clean up Markdown Headers (User request: "不要#井号")
    # Remove leading hashes and optional space
    content = re.sub(r'(?m)^#+\s*', '', content)

    # Split by double dollar signs for block math $$...$$
    # This regex captures the delimiter so we can process it
    block_parts = re.split(r'(\$\$[\s\S]*?\$\$)', content)
    
    text_widget.images = [] # Keep references to images
    
    for block_part in block_parts:
        if block_part.startswith('$$') and block_part.endswith('$$'):
            # Block Math
            latex = block_part[2:-2].strip()
            # Render larger for blocks
            # Adjusted for standard display size (DPI 100) to avoid huge images
            img = render_math_to_image(latex, fontsize=10, dpi=70)
            if img:
                photo = ImageTk.PhotoImage(img)
                text_widget.images.append(photo)
                text_widget.insert(tk.END, '\n') # Ensure newline before
                text_widget.image_create(tk.END, image=photo, align='center')
                text_widget.insert(tk.END, '\n') # Ensure newline after
            else:
                # Fallback to text if render fails
                text_widget.insert(tk.END, block_part)
        else:
            # This part contains text and possibly inline math $...$
            # Split by single dollar sign
            # Avoid splitting \$ (escaped dollar) if we were robust, but for now simple split
            inline_parts = re.split(r'(\$[^\$\n]+\$)', block_part)
            
            for part in inline_parts:
                if part.startswith('$') and part.endswith('$') and len(part) > 2:
                    # Inline Math
                    latex = part[1:-1].strip()
                    # Adjusted for standard display size to match text
                    img = render_math_to_image(latex, fontsize=9, dpi=65)
                    if img:
                        photo = ImageTk.PhotoImage(img)
                        text_widget.images.append(photo)
                        text_widget.image_create(tk.END, image=photo, align='center')
                    else:
                        text_widget.insert(tk.END, part)
                else:
                    # Regular Text
                    text_widget.insert(tk.END, part)

def main():
    text_content = "No result provided."
    if len(sys.argv) > 1:
        input_arg = sys.argv[1]
        # Check if the argument is a file path
        if os.path.exists(input_arg) and os.path.isfile(input_arg):
            try:
                with open(input_arg, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                
                # DO NOT remove backslashes anymore! We need them for LaTeX.
                
                # Optionally delete the temp file after reading
                try:
                    os.remove(input_arg)
                except:
                    pass
            except Exception as e:
                text_content = f"Error reading result file: {e}"
        else:
            text_content = input_arg

    root = tk.Tk()
    root.title("Answer")
    
    # Remove window decorations (frameless)
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    
    # Window settings
    config = load_config()
    win_width = config.get("width", 240)
    win_height = config.get("height", 150)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = screen_width - win_width
    y = 0
    root.geometry(f"{win_width}x{win_height}+{x}+{y}")
    
    # Appearance
    bg_color = '#FFFFFF'
    root.configure(bg=bg_color)
    root.attributes('-alpha', 0.8) # 80% opacity

    # Frame
    frame = tk.Frame(root, bg=bg_color)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Close button
    close_btn = tk.Label(frame, text="✕", bg=bg_color, fg="#555555", cursor="hand2", font=("Helvetica", 18))
    close_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)
    close_btn.bind("<Button-1>", close_window)
    
    # Text Area
    text_frame = tk.Frame(frame, bg=bg_color)
    text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(25, 15))
    
    custom_font = font.Font(family="Arial Unicode MS", size=10)
    
    txt = tk.Text(
        text_frame, 
        bg=bg_color, 
        fg="#000000", 
        font=custom_font, 
        wrap=tk.WORD, 
        highlightthickness=0, 
        bd=0
    )
    txt.pack(fill=tk.BOTH, expand=True)
    
    # Add scrollbar
    scrollbar = tk.Scrollbar(text_frame, command=txt.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    txt.config(yscrollcommand=scrollbar.set)
    
    # Parse and Display Content (with Math Rendering)
    try:
        display_content(txt, text_content)
    except Exception as e:
        txt.insert(tk.END, f"\n\n[Error rendering content]: {e}\nRaw Content:\n{text_content}")
    
    # Disable editing
    txt.config(state=tk.DISABLED)
    
    # Drag functionality
    def start_move(event):
        root.x = event.x
        root.y = event.y

    def stop_move(event):
        root.x = None
        root.y = None

    def do_move(event):
        deltax = event.x - root.x
        deltay = event.y - root.y
        x = root.winfo_x() + deltax
        y = root.winfo_y() + deltay
        root.geometry(f"+{x}+{y}")

    frame.bind("<ButtonPress-1>", start_move)
    frame.bind("<ButtonRelease-1>", stop_move)
    frame.bind("<B1-Motion>", do_move)
    
    # Double click to exit
    root.bind("<Double-Button-1>", close_window)
    
    # Auto-exit after 5 minutes (300,000 ms)
    root.after(300000, close_window)

    # Resize Grip (Custom implementation for frameless window)
    # Changed cursor to "crosshair" to avoid TclError on macOS (se-resize is not always supported)
    # Bottom-Left Grip (User request: "左下角自由拉拽")
    grip = tk.Label(root, text="◣", bg=bg_color, fg="#999999", cursor="crosshair", font=("Arial", 10))
    grip.place(relx=0.0, rely=1.0, anchor="sw", x=0, y=0)
    
    # Resize State Container
    resize_state = {}

    def start_resize(event):
        resize_state['start_x'] = event.x_root
        resize_state['start_y'] = event.y_root
        resize_state['start_w'] = root.winfo_width()
        resize_state['start_h'] = root.winfo_height()
        resize_state['start_win_x'] = root.winfo_x()
        resize_state['start_win_y'] = root.winfo_y()

    def do_resize(event):
        try:
            if 'start_x' not in resize_state:
                return
                
            dx = event.x_root - resize_state['start_x']
            dy = event.y_root - resize_state['start_y']
            
            # Dragging left (dx < 0) -> Increase width
            # Dragging right (dx > 0) -> Decrease width
            new_width = int(resize_state['start_w'] - dx)
            
            # Dragging down (dy > 0) -> Increase height
            new_height = int(resize_state['start_h'] + dy)
            
            # Adjust X coordinate to keep right edge fixed
            # New X = Old X + dx
            new_x = int(resize_state['start_win_x'] + dx)
            
            if new_width > 50 and new_height > 50: # Minimum size
                root.geometry(f"{new_width}x{new_height}+{new_x}+{resize_state['start_win_y']}")
        except Exception as e:
            print(f"Resize error: {e}")

    def end_resize(event):
        save_config(root.winfo_width(), root.winfo_height())
        # Clear state just in case
        resize_state.clear()

    grip.bind("<ButtonPress-1>", start_resize)
    grip.bind("<B1-Motion>", do_resize)
    grip.bind("<ButtonRelease-1>", end_resize)

    root.mainloop()

if __name__ == "__main__":
    main()
