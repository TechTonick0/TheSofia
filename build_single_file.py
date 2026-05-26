import re
import base64
import os
from io import BytesIO
from PIL import Image

# Configuration
INPUT_HTML = 'prototype.html'
OUTPUT_HTML = 'prototype_embedded.html'
MAX_WIDTH = 1600
QUALITY = 80
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}

def optimize_and_encode_image(image_path):
    """
    Reads an image, resizes it if necessary, converts to WebP,
    and returns a base64 data URI.
    """
    if not os.path.exists(image_path):
        print(f"Warning: Image not found: {image_path}")
        return None

    try:
        with Image.open(image_path) as img:
            # Fix orientation based on EXIF data
            from PIL import ImageOps
            img = ImageOps.exif_transpose(img)

            # Convert to RGB if necessary (e.g. for PNGs with alpha being saved as JPEG, though we use WebP here which supports alpha)
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                 pass # WebP handles transparency fine
            
            # Resize logic
            width, height = img.size
            if width > MAX_WIDTH:
                new_height = int(height * (MAX_WIDTH / width))
                img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                print(f"  Resized {image_path} from {width}x{height} to {MAX_WIDTH}x{new_height}")
            
            # Save to buffer as WebP
            buffer = BytesIO()
            img.save(buffer, format='WEBP', quality=QUALITY)
            buffer.seek(0)
            
            # Encode to Base64
            b64_data = base64.b64encode(buffer.read()).decode('utf-8')
            return f"data:image/webp;base64,{b64_data}"
            
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def main():
    print(f"Reading {INPUT_HTML}...")
    with open(INPUT_HTML, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex patterns
    # 1. <img src="filename.ext">
    # 2. url('filename.ext') or url("filename.ext")
    
    # We find all unique image references first
    # This is a bit naive regex but sufficient for this specific project structure
    # Matches: src="...", src='...', url('...'), url("...")
    patterns = [
        r'src=["\']([^"\']+\.(?:jpg|jpeg|png|gif))["\']',
        r'url\([\"\']?([^"\')]+\.(?:jpg|jpeg|png|gif))[\"\']?\)'
    ]
    
    replacements = {}
    
    for pattern in patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            filename = match.group(1)
            if filename in replacements:
                continue
                
            print(f"Processing image: {filename}")
            data_uri = optimize_and_encode_image(filename)
            
            if data_uri:
                replacements[filename] = data_uri

    # Apply replacements
    print(f"Embedding {len(replacements)} images...")
    
    # Simple string replacement - safer than regex substitution for literals
    # We sort by length descending to avoid replacing substrings of other filenames (unlikely here but good practice)
    for filename in sorted(replacements.keys(), key=len, reverse=True):
        # We need to be careful. The regex extracted just the filename.
        # We replace the filename occurrences in the content.
        content = content.replace(filename, replacements[filename])

    print(f"Writing to {OUTPUT_HTML}...")
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Done!")

if __name__ == "__main__":
    main()
