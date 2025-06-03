from flask import Flask, send_file, render_template, request, send_from_directory
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

@app.route('/')
def serve_static_site():
    """Serve the static Illuvium site with working wallet modal"""
    logger.info("Serving static Illuvium site")
    return send_file('illuvium_static_site.html')

@app.route('/images/<path:path>')
def serve_images(path):
    """Proxy image requests to the original site"""
    logger.info(f"Serving image: {path}")
    # First check if we have the image locally
    if os.path.exists(os.path.join('images', path)):
        return send_from_directory('images', path)
    # Otherwise return a placeholder or default image
    return send_file('images/placeholder.png') if os.path.exists('images/placeholder.png') else ''

@app.route('/_next/images/<path:path>')
def serve_next_images(path):
    """Proxy Next.js image requests to the original site"""
    logger.info(f"Serving Next.js image: {path}")
    # First check if we have the image locally
    if os.path.exists(os.path.join('_next/images', path)):
        return send_from_directory('_next/images', path)
    # Otherwise return a placeholder or default image
    return send_file('images/placeholder.png') if os.path.exists('images/placeholder.png') else ''

@app.after_request
def add_headers(response):
    """Add necessary headers to all responses"""
    # Set permissions policy to allow clipboard operations
    response.headers['Permissions-Policy'] = 'clipboard-read=*, clipboard-write=*, web-share=*, accelerometer=*, ambient-light-sensor=*, camera=*, geolocation=*, gyroscope=*, magnetometer=*, microphone=*, payment=*, usb=*, interest-cohort=()'
    
    # Set CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    
    # Set security headers
    response.headers['Cross-Origin-Opener-Policy'] = 'unsafe-none'
    response.headers['Cross-Origin-Embedder-Policy'] = 'unsafe-none'
    response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
    
    return response

if __name__ == '__main__':
    # Make sure image directories exist
    os.makedirs('images', exist_ok=True)
    os.makedirs(os.path.join('_next', 'images'), exist_ok=True)
    
    # Create a placeholder image if it doesn't exist
    if not os.path.exists('images/placeholder.png'):
        try:
            with open('images/placeholder.png', 'wb') as f:
                # Write a simple transparent PNG
                f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x00\x00\x02\x00\x01\xe5\'\xde\xfc\x00\x00\x00\x00IEND\xaeB`\x82')
        except Exception as e:
            logger.error(f"Failed to create placeholder image: {e}")
    
    logger.info("Starting static Illuvium site server on port 8002")
    app.run(host='0.0.0.0', port=8002, debug=True) 