from flask import Flask, render_template, request, send_from_directory, Response, redirect, url_for, make_response
import os
import mimetypes
import logging
import requests
import re
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set up MIME types
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/json', '.json')
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('application/wasm', '.wasm')

# Create Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for development

# Constants
ORIGINAL_SITE = "https://overworld.illuvium.io"
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

# Browser headers for proxying requests
BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Security headers for responses
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'Cross-Origin-Resource-Policy': 'cross-origin',
    'Timing-Allow-Origin': '*',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS, HEAD',
    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Range, Authorization',
    'Access-Control-Expose-Headers': 'Content-Length, Content-Range, Accept-Ranges',
    'Permissions-Policy': 'clipboard-read=*, clipboard-write=*, web-share=*, accelerometer=*, ambient-light-sensor=*, camera=*, geolocation=*, gyroscope=*, magnetometer=*, microphone=*, payment=*, usb=*, interest-cohort=()'
}

def add_security_headers(response):
    """Add security headers to the response"""
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    return response

def inject_wallet_connect_script(html_content):
    """Inject wallet connect script into HTML content"""
    # Add modal and script at end of body
    wallet_script = """
    <!-- Global Wallet Connect Button -->
    <div style="position: fixed; top: 20px; right: 20px; z-index: 9999;">
      <button id="global-wallet-connect" style="background-color: #3ddcff; color: #0e0c1d; border: none; padding: 10px 15px; border-radius: 4px; font-weight: bold; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.3); font-family: Arial, sans-serif;">
        Connect Wallet
      </button>
    </div>
    
    <!-- Wallet Connect Modal -->
    <div id="wallet-connect-modal" style="display:none;"></div>
    
    <!-- Wallet Connect Script -->
    <script src="/static/js/wallet-connect.js"></script>
    <script src="/static/js/modal.bundle.js"></script>
    """
    
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', wallet_script + '</body>')
    else:
        html_content += wallet_script
    
    # Add permissions fix in head
    head_script = """
    <meta http-equiv="Permissions-Policy" content="clipboard-read=*, clipboard-write=*, web-share=*, accelerometer=*, ambient-light-sensor=*, camera=*, geolocation=*, gyroscope=*, magnetometer=*, microphone=*, payment=*, usb=*, interest-cohort=()">
    <meta http-equiv="Cross-Origin-Opener-Policy" content="unsafe-none">
    <meta http-equiv="Cross-Origin-Embedder-Policy" content="unsafe-none">
    <meta http-equiv="Cross-Origin-Resource-Policy" content="cross-origin">
    """
    
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', head_script + '</head>')
    
    return html_content

def modify_links_in_html(html_content, base_url):
    """Modify links in HTML content to use our proxy"""
    # Fix absolute URLs to use our proxy
    html_content = re.sub(
        r'(href|src)=["\']https://overworld\.illuvium\.io/([^"\']*)["\']',
        r'\1="/\2"',
        html_content
    )
    
    # Fix relative URLs
    html_content = re.sub(
        r'(href|src)=["\']/([^"\']*)["\']',
        r'\1="/\2"',
        html_content
    )
    
    return html_content

@app.route('/test')
def test_route():
    """Test route to verify Flask is working"""
    return {'status': 'ok', 'message': 'Illuvium proxy is running'}

@app.route('/static/<path:path>')
def serve_static_files(path):
    """Serve static files from the static directory or proxy them"""
    static_dir = os.path.join(app.root_path, 'static')
    file_path = os.path.join(static_dir, path)
    
    # Check if the file exists locally
    if os.path.exists(file_path) and os.path.isfile(file_path):
        response = send_from_directory(static_dir, path)
        return add_security_headers(response)
    
    # Try to proxy from original site
    try:
        url = f"{ORIGINAL_SITE}/static/{path}"
        logger.info(f"Proxying static file: {url}")
        
        response = requests.get(url, headers=BROWSER_HEADERS)
        
        if response.status_code == 200:
            # Create directories if needed
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save file for future requests
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            # Determine content type
            content_type = response.headers.get('Content-Type')
            if not content_type:
                content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
            
            # Create response with proper headers
            flask_response = Response(
                response.content,
                status=response.status_code,
                mimetype=content_type
            )
            
            return add_security_headers(flask_response)
        else:
            logger.warning(f"Failed to proxy static file: {response.status_code}")
            return "File not found", 404
            
    except Exception as e:
        logger.error(f"Error proxying static file: {str(e)}")
        return "Error processing file", 500

@app.route('/images/<path:path>')
def serve_images(path):
    """Serve images from the images directory or proxy them"""
    images_dir = os.path.join(app.root_path, 'images')
    file_path = os.path.join(images_dir, path)
    
    # Check if the image exists locally
    if os.path.exists(file_path) and os.path.isfile(file_path):
        response = send_from_directory(images_dir, path)
        return add_security_headers(response)
    
    # Try to proxy from original site
    try:
        url = f"{ORIGINAL_SITE}/images/{path}"
        logger.info(f"Proxying image: {url}")
        
        response = requests.get(url, headers=BROWSER_HEADERS, stream=True)
        
        if response.status_code == 200:
            # Create directories if needed
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save file for future requests
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Determine content type
            content_type = response.headers.get('Content-Type', 'image/webp')
            
            # Create response with proper headers
            flask_response = send_from_directory(os.path.dirname(file_path), os.path.basename(file_path))
            flask_response.headers['Content-Type'] = content_type
            
            return add_security_headers(flask_response)
        else:
            logger.warning(f"Failed to proxy image: {response.status_code}")
            return "Image not found", 404
            
    except Exception as e:
        logger.error(f"Error proxying image: {str(e)}")
        return "Error processing image", 500

@app.route('/_next/<path:path>')
def serve_next_files(path):
    """Serve Next.js files or proxy them"""
    next_dir = os.path.join(app.root_path, '_next')
    file_path = os.path.join(next_dir, path)
    
    # Check if the file exists locally
    if os.path.exists(file_path) and os.path.isfile(file_path):
        response = send_from_directory(next_dir, path)
        return add_security_headers(response)
    
    # Try to proxy from original site
    try:
        url = f"{ORIGINAL_SITE}/_next/{path}"
        logger.info(f"Proxying Next.js file: {url}")
        
        response = requests.get(url, headers=BROWSER_HEADERS)
        
        if response.status_code == 200:
            # Create directories if needed
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save file for future requests
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            # Determine content type
            content_type = response.headers.get('Content-Type')
            if not content_type:
                content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
            
            # Create response with proper headers
            flask_response = Response(
                response.content,
                status=response.status_code,
                mimetype=content_type
            )
            
            return add_security_headers(flask_response)
        else:
            logger.warning(f"Failed to proxy Next.js file: {response.status_code}")
            return "File not found", 404
            
    except Exception as e:
        logger.error(f"Error proxying Next.js file: {str(e)}")
        return "Error processing file", 500

@app.route('/')
def index():
    """Proxy the index page with modifications"""
    try:
        url = f"{ORIGINAL_SITE}/"
        logger.info(f"Proxying index: {url}")
        
        response = requests.get(url, headers=BROWSER_HEADERS)
        
        if response.status_code == 200:
            html_content = response.text
            
            # Inject wallet connect script
            html_content = inject_wallet_connect_script(html_content)
            
            # Modify links to use our proxy
            html_content = modify_links_in_html(html_content, request.url_root)
            
            # Create response with proper headers
            flask_response = Response(
                html_content,
                status=response.status_code,
                mimetype='text/html'
            )
            
            return add_security_headers(flask_response)
        else:
            logger.warning(f"Failed to proxy index: {response.status_code}")
            return "Unable to retrieve the page", response.status_code
            
    except Exception as e:
        logger.error(f"Error proxying index: {str(e)}")
        return "Error processing page", 500

@app.route('/<path:path>')
def catch_all(path):
    """Catch-all route to proxy all other requests"""
    try:
        url = f"{ORIGINAL_SITE}/{path}"
        logger.info(f"Catch-all proxy for: {url}")
        
        # Add query parameters
        params = request.args.to_dict()
        
        # Make the request
        response = requests.get(url, headers=BROWSER_HEADERS, params=params)
        
        # Get content type
        content_type = response.headers.get('Content-Type', 'text/html')
        
        # If HTML, modify the content
        if 'text/html' in content_type:
            html_content = response.text
            
            # Inject wallet connect script
            html_content = inject_wallet_connect_script(html_content)
            
            # Modify links to use our proxy
            html_content = modify_links_in_html(html_content, request.url_root)
            
            # Create response with proper headers
            flask_response = Response(
                html_content,
                status=response.status_code,
                mimetype='text/html'
            )
        else:
            # For other content types, return as-is
            flask_response = Response(
                response.content,
                status=response.status_code,
                mimetype=content_type
            )
        
        return add_security_headers(flask_response)
            
    except Exception as e:
        logger.error(f"Error in catch-all proxy: {str(e)}")
        return "Error processing request", 500

@app.after_request
def add_cors_headers(response):
    """Add CORS headers to all responses"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS, HEAD'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Range, Authorization'
    return response

if __name__ == '__main__':
    # Make sure static directory exists
    os.makedirs(os.path.join(app.root_path, 'static', 'js'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'images'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, '_next'), exist_ok=True)
    
    logger.info("Starting Illuvium proxy app on http://localhost:8001")
    app.run(host='0.0.0.0', port=8001, debug=True) 