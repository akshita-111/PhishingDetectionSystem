"""
Generate simple placeholder icons for the browser extension.
Run this script to create icon16.png, icon48.png, icon128.png
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, color=(76, 175, 80)):
    """Create a simple square icon with a shield symbol"""
    # Create image with background color
    img = Image.new('RGB', (size, size), color)
    draw = ImageDraw.Draw(img)
    
    # Draw a simple shield shape
    margin = size // 8
    shield_width = size - 2 * margin
    shield_height = int(shield_width * 1.2)
    
    # Shield polygon points
    points = [
        (margin, margin),
        (size - margin, margin),
        (size - margin, margin + shield_height // 2),
        (size // 2, margin + shield_height),
        (margin, margin + shield_height // 2)
    ]
    
    draw.polygon(points, fill=(255, 255, 255))
    
    # Draw a checkmark
    check_start = (size // 3, size // 2)
    check_mid = (size // 2, size // 2 + size // 6)
    check_end = (size * 2 // 3, size // 3)
    
    draw.line([check_start, check_mid], fill=(76, 175, 80), width=max(2, size // 16))
    draw.line([check_mid, check_end], fill=(76, 175, 80), width=max(2, size // 16))
    
    return img

def main():
    # Create icons directory if it doesn't exist
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    
    # Generate icons
    sizes = [16, 48, 128]
    for size in sizes:
        icon = create_icon(size)
        icon.save(f'icon{size}.png')
        print(f'Created icon{size}.png')
    
    print('All icons generated successfully!')

if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print('PIL/Pillow not installed. Install with: pip install Pillow')
        print('Or add placeholder icons manually.')
