# /Users/home/LLM/illuvidex/app.py

from flask import Flask, jsonify, render_template, request, send_from_directory, redirect, send_file, Response
import logging
import os
import sys
import mimetypes
from importlib import import_module
import requests

# Set JavaScript MIME type
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/json', '.json')
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('application/wasm', '.wasm')

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Register important MIME types immediately for consistency
mimetypes.add_type('application/javascript', '.mjs')
mimetypes.add_type('text/javascript', '.js')  # Fallback for older browsers

# Create Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload

# Add HTTP/2 support configuration
app.config['PREFERRED_URL_SCHEME'] = 'https'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for development

# Add a test route to verify basic Flask functionality
@app.route('/test')
def test_route():
    return jsonify({"status": "ok", "message": "Test route working"})

# Define a route for the index page
@app.route('/')
def index():
    logger.info("Serving index page")
    return render_template('index.html')

# Initialize modules with better error handling
logger.info("Starting Illuvidex application")

# Initialize security headers first to ensure proper CORS handling
try:
    logger.debug("Loading security_headers module")
    from modules.security_headers import init_security_headers
    init_security_headers(app)
    logger.info("Security headers initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize security_headers: {str(e)}")
    import traceback
    logger.error(traceback.format_exc())

# Then try to initialize static files module
try:
    logger.debug("Loading static_files module")
    from modules.static_files import init_static_files
    init_static_files(app)
    logger.info("Static files module initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize static_files: {str(e)}")
    import traceback
    logger.error(traceback.format_exc())

try:
    logger.debug("Loading content_proxy module")
    from modules.content_proxy import init_content_proxy
    init_content_proxy(app)
    logger.info("Content proxy initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize content_proxy: {str(e)}")
    import traceback
    logger.error(traceback.format_exc())

# Try to load other modules if they exist
for module_name in ['error_handler', 'image_handler', 'ip_validation']:
    try:
        module_path = f'modules.{module_name}'
        logger.debug(f"Attempting to load {module_path}")
        module = import_module(module_path)
        init_func = getattr(module, f'init_{module_name}', None)
        if init_func:
            logger.debug(f"Initializing {module_name}")
            init_func(app)
            logger.info(f"{module_name} initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to initialize {module_name}: {str(e)}")

# Log all registered routes for debugging
logger.info(f"Registered routes:")
for rule in app.url_map.iter_rules():
    logger.info(f"  {rule.endpoint}: {rule}")

@app.route('/autodrone', methods=['GET', 'HEAD', 'OPTIONS'])
def serve_autodrone_default():
    """Handle requests to /autodrone without path parameter"""
    try:
        logger.info("Handling direct request to /autodrone")
        
        # Instead of showing a directory listing or redirecting to a non-existent page,
        # redirect to the main page with a special query parameter to indicate we should 
        # navigate to the autodrone section
        return redirect('/?section=autodrone')
    except Exception as e:
        logger.error(f"Error serving autodrone default page: {str(e)}")
        return f"Error serving autodrone page: {str(e)}", 500

@app.route('/037b440f/index.js')
def serve_037b440f_index_js():
    """Direct handler for 037b440f/index.js file"""
    logger.info("Serving 037b440f/index.js file")
    file_path = os.path.join(app.root_path, 'static', '037b440f', 'index.js')
    if os.path.exists(file_path):
        try:
            # Use Flask's send_file with the appropriate MIME type
            response = send_file(file_path, mimetype='application/javascript')
            
            # Add necessary headers
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
            response.headers['Access-Control-Allow-Origin'] = '*'
            
            return response
        except Exception as e:
            logger.error(f"Error serving 037b440f/index.js: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
    
    return "File not found", 404

@app.route('/7c93fa6a/index.js')
def serve_7c93fa6a_index_js():
    """Direct handler for 7c93fa6a/index.js file"""
    logger.info("Serving 7c93fa6a/index.js file")
    file_path = os.path.join(app.root_path, 'static', '7c93fa6a', 'index.js')
    if os.path.exists(file_path):
        try:
            # Use Flask's send_file with the appropriate MIME type
            response = send_file(file_path, mimetype='application/javascript')
            
            # Add necessary headers
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
            response.headers['Access-Control-Allow-Origin'] = '*'
            
            return response
        except Exception as e:
            logger.error(f"Error serving 7c93fa6a/index.js: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
    
    return "File not found", 404

@app.route('/037b440f/chunk.<path:filename>', methods=['GET', 'HEAD', 'OPTIONS'])
def serve_specific_037b440f_chunk(filename):
    """Serve specific chunk files for 037b440f directory"""
    logger.info(f"Serving specific 037b440f/chunk.{filename}")
    file_path = os.path.join(app.root_path, 'static', '037b440f', f'chunk.{filename}')
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    if not os.path.exists(file_path):
        # Create stub file for missing chunks
        logger.info(f"Creating stub file for missing 037b440f/chunk.{filename}")
        stub_content = f"// Stub file for missing 037b440f/chunk.{filename}\nconsole.log('Stub module loaded for chunk.{filename}');\nexport default {{}};"
        with open(file_path, 'w') as f:
            f.write(stub_content)
    
    # Serve the file with proper MIME type
    response = send_file(file_path, mimetype='application/javascript')
    
    # Add CORS headers
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    return response

@app.route('/7c93fa6a/chunk.<path:filename>', methods=['GET', 'HEAD', 'OPTIONS'])
def serve_specific_7c93fa6a_chunk(filename):
    """Serve specific chunk files for 7c93fa6a directory"""
    logger.info(f"Serving specific 7c93fa6a/chunk.{filename}")
    file_path = os.path.join(app.root_path, 'static', '7c93fa6a', f'chunk.{filename}')
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    if not os.path.exists(file_path):
        # Create stub file for missing chunks
        logger.info(f"Creating stub file for missing 7c93fa6a/chunk.{filename}")
        stub_content = f"// Stub file for missing 7c93fa6a/chunk.{filename}\nconsole.log('Stub module loaded for chunk.{filename}');\nexport default {{}};"
        with open(file_path, 'w') as f:
            f.write(stub_content)
    
    # Serve the file with proper MIME type
    response = send_file(file_path, mimetype='application/javascript')
    
    # Add CORS headers
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    return response

@app.route('/037b440f/index.css', methods=['GET', 'HEAD', 'OPTIONS'])
def serve_specific_037b440f_css():
    """Serve index.css file for 037b440f directory"""
    logger.info("Serving specific 037b440f/index.css")
    file_path = os.path.join(app.root_path, 'static', '037b440f', 'index.css')
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    if not os.path.exists(file_path):
        # Create stub file for missing CSS
        logger.info("Creating stub file for missing 037b440f/index.css")
        stub_content = "/* Stub file for missing 037b440f/index.css */\n/* Empty CSS file created by server */"
        with open(file_path, 'w') as f:
            f.write(stub_content)
    
    # Serve the file with proper MIME type
    response = send_file(file_path, mimetype='text/css')
    
    # Add CORS headers
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    return response

# Global CORS middleware
@app.after_request
def add_cors_headers(response):
    """Add CORS headers to all responses"""
    
    # Add CORS headers to all responses
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, HEAD'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Range, Authorization'
    response.headers['Access-Control-Max-Age'] = '86400'  # 24 hours
    
    # For specific paths, add more permissive CORS
    if request.path.startswith('/static/') or '.js' in request.path or '.css' in request.path:
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Private-Network'] = 'true'
    
    return response

# Run the app with a different port when executed directly
if __name__ == '__main__':
    logger.info(f"Flask routes: {app.url_map}")
    app.run(host='0.0.0.0', port=8000, debug=True)