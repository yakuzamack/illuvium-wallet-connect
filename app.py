# /Users/home/LLM/illuvidex/app.py

from flask import Flask, jsonify, render_template
import logging
import os
import sys
from importlib import import_module

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload

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

try:
    logger.debug("Loading content_proxy module")
    from modules.content_proxy import init_content_proxy
    init_content_proxy(app)
    logger.debug("Content proxy initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize content_proxy: {str(e)}")
    import traceback
    logger.error(traceback.format_exc())

# Try to load other modules if they exist
for module_name in ['error_handler', 'static_files', 'image_handler', 'ip_validation']:
    try:
        module_path = f'modules.{module_name}'
        logger.debug(f"Attempting to load {module_path}")
        module = import_module(module_path)
        init_func = getattr(module, f'init_{module_name}', None)
        if init_func:
            logger.debug(f"Initializing {module_name}")
            init_func(app)
            logger.debug(f"{module_name} initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize {module_name}: {str(e)}")

# Run the app
if __name__ == '__main__':
    logger.info(f"Flask routes: {app.url_map}")
    app.run(host='0.0.0.0', debug=True)