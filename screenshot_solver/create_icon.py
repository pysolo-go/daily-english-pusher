from PIL import Image, ImageDraw

def create_icon():
    # Create a 22x22 image (standard for macOS menu bar) with transparent background
    size = (44, 44) # 2x for Retina
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a simple viewfinder / target icon in black
    # macOS will automatically invert this for dark mode if we set setTemplate_(True)
    
    # Outer box corners
    # Top-left
    draw.line([(4, 4), (16, 4)], fill='black', width=3)
    draw.line([(4, 4), (4, 16)], fill='black', width=3)
    
    # Top-right
    draw.line([(28, 4), (40, 4)], fill='black', width=3)
    draw.line([(40, 4), (40, 16)], fill='black', width=3)
    
    # Bottom-left
    draw.line([(4, 40), (16, 40)], fill='black', width=3)
    draw.line([(4, 40), (4, 28)], fill='black', width=3)
    
    # Bottom-right
    draw.line([(28, 40), (40, 40)], fill='black', width=3)
    draw.line([(40, 40), (40, 28)], fill='black', width=3)
    
    # Center dot
    draw.ellipse([(19, 19), (25, 25)], fill='black')
    
    # Save as PNG
    image.save('icon.png', 'PNG')
    print("icon.png created successfully.")

if __name__ == "__main__":
    create_icon()
