from PIL import Image
import os

# Create directory if it doesn't exist
os.makedirs('static', exist_ok=True)

# Create a transparent WebP placeholder
img = Image.new('RGBA', (640, 480), (0, 0, 0, 0))
img.save('static/placeholder.webp', 'WEBP')
print("Created transparent WebP placeholder at static/placeholder.webp")