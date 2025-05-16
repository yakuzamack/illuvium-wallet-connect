from flask import Flask, send_from_directory, send_file, Response, make_response, request
import os
import requests
import mimetypes
import logging
import io
import urllib.parse
import shutil


logger = logging.getLogger(__name__)

def init_static_files(app):
    """Initialize static file handling"""
    # Register proper JS MIME types consistently across the application
    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('application/javascript', '.mjs')
    mimetypes.add_type('text/javascript', '.js')  # Fallback for older browsers
    
    # Create necessary directories
    os.makedirs(os.path.join(app.root_path, '_next', 'static', 'chunks'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, '_next', 'static', 'css'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, '_next', 'static', 'media'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'images'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'static', 'js'), exist_ok=True)
    
    # Helper function to add CORS headers to responses
    def add_cors_headers(response, is_js=False):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS, HEAD'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Range, Authorization'
        response.headers['Access-Control-Expose-Headers'] = 'Content-Length, Content-Range, Accept-Ranges'
        response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
        response.headers['Cross-Origin-Embedder-Policy'] = 'credentialless'
        response.headers['Vary'] = 'Origin, Accept-Encoding'  # Important for caching in HTTP/2 contexts
        response.headers['Timing-Allow-Origin'] = '*'
        
        if is_js:
            response.headers['Content-Type'] = 'application/javascript; charset=utf-8'
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            
        return response
    
    # Helper function to process cookies for cross-site contexts
    def fix_cookies_for_cross_site(response):
        """Modify cookies to work in cross-site contexts"""
        if not response.headers.getlist('Set-Cookie'):
            return response
            
        for cookie in response.headers.getlist('Set-Cookie'):
            # Handle amplify-polling-started cookie and any other cookies needing cross-site access
            if 'amplify-polling-started' in cookie or 'cross-site' in cookie.lower():
                # Remove the existing cookie
                response.headers.remove('Set-Cookie')
                
                # Add it back with SameSite=None and Secure flag
                parts = cookie.split(';')
                modified_parts = []
                
                for part in parts:
                    part = part.strip()
                    if 'samesite' in part.lower():
                        continue  # Skip existing SameSite directive
                    modified_parts.append(part)
                
                # Add SameSite=None and Secure flag for cross-site contexts
                modified_parts.append('SameSite=None')
                modified_parts.append('Secure')
                
                # Set the modified cookie
                response.headers.add('Set-Cookie', '; '.join(modified_parts))
        
        return response
    
    # Helper to create properly configured JS responses
    def create_js_response(content, filename=None):
        """Create a properly configured response for JavaScript content"""
        response = Response(
            content,
            mimetype='application/javascript',
            headers={
                'Content-Type': 'application/javascript; charset=utf-8',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS, HEAD',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Range, Authorization',
                'Cross-Origin-Resource-Policy': 'cross-origin',
                'Cross-Origin-Embedder-Policy': 'credentialless',
                'Vary': 'Origin, Accept-Encoding',
                'Timing-Allow-Origin': '*',
                'X-Content-Type-Options': 'nosniff',
                'Access-Control-Allow-Private-Network': 'true',
                'Access-Control-Expose-Headers': 'Content-Length, Content-Range, Accept-Ranges'
            }
        )
        
        # Add special handling for our critical files
        if filename and (filename.endswith('settings.js') or filename.endswith('gkohcg1u379.js')):
            logger.debug(f"Adding special headers for critical file: {filename}")
            # These files need to load properly in any context
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['Access-Control-Allow-Private-Network'] = 'true'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            
            # Set the amplify-polling-started cookie with proper cross-site attributes
            if 'settings.js' in filename:
                response.set_cookie(
                    'amplify-polling-started', 
                    value='true',
                    max_age=86400,
                    samesite='None',
                    secure=True,
                    httponly=False,
                    path='/'
                )
        
        return response
    
    @app.route('/_next/static/<path:path>')
    def serve_next_static(path):
        """Handle Next.js static files with proper binary handling"""
        local_path = os.path.join(app.root_path, '_next', 'static', path)
        local_dir = os.path.dirname(local_path)
        os.makedirs(local_dir, exist_ok=True)
        
        # Check if the file exists locally and isn't corrupted
        file_exists = os.path.exists(local_path) and os.path.isfile(local_path)
        is_js_file = path.endswith('.js')
        
        # Ensure we have fresh JS files
        if is_js_file and (not file_exists or os.path.getsize(local_path) == 0):
            file_exists = False  # Force re-download for empty or missing JS files
        
        if file_exists:
            # Serve the local file
            # For JS files, improve headers setup
            if is_js_file:
                try:
                    with open(local_path, 'rb') as f:
                        content = f.read()
                    return create_js_response(content, path)
                except Exception as e:
                    logger.error(f"Error reading JS file {path}: {str(e)}")
                    # Fall back to standard sending
            
            response = send_file(local_path)
            if is_js_file:
                return add_cors_headers(response, is_js=True)
            return response
        
        # Download from original site
        try:
            # Use raw binary mode for JS files to prevent text processing
            url = f"https://overworld.illuvium.io/_next/static/{path}"
            logger.info(f"Downloading: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
            }
            
            # Use streaming for binary files
            response = requests.get(url, headers=headers, stream=True)
            
            if response.status_code == 200:
                # Ensure directory exists
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                # For JS files, download as binary without text manipulation
                with open(local_path, 'wb') as f:
                    # Use raw content without text processing
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Serve the downloaded file
                if is_js_file:
                    try:
                        with open(local_path, 'rb') as f:
                            content = f.read()
                        return create_js_response(content, path)
                    except Exception as e:
                        logger.error(f"Error reading downloaded JS file {path}: {str(e)}")
                        # Fall back to standard sending
                
                resp = send_file(local_path)
                
                # Set appropriate cache headers
                if is_js_file:
                    return add_cors_headers(resp, is_js=True)
                else:
                    resp.headers['Cache-Control'] = 'public, max-age=31536000'
                    
                return resp
            else:
                logger.error(f"Failed to download: {url} - Status: {response.status_code}")
                return "File not found", 404
        except Exception as e:
            logger.error(f"Error processing {path}: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return "Error processing file", 500
    
    # Image handling routes
    @app.route('/images/<path:path>')
    def serve_images(path):
        """Handle image file requests"""
        logger.info(f"Serving image: {path}")
        images_dir = os.path.join(app.root_path, 'images')
        os.makedirs(images_dir, exist_ok=True)
        file_path = os.path.join(images_dir, path)
        
        # Check if image exists locally
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_file(file_path)
        
        # Try to proxy from original site
        try:
            url = f"https://overworld.illuvium.io/images/{path}"
            logger.info(f"Downloading image: {url}")
            
            response = requests.get(url, stream=True)
            
            if response.status_code == 200:
                # Create directory structure
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Save file
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Serve the downloaded file
                return send_file(file_path)
            else:
                logger.warning(f"Failed to download image: {response.status_code}")
                return "Image not found", 404
        except Exception as e:
            logger.error(f"Error downloading image: {str(e)}")
            return "Error processing image", 500
    
    # Add handler for images with extensions
    @app.route('/images/<path:path>.<ext>')
    def serve_images_with_extension(path, ext):
        """Fallback handler for image requests with extensions"""
        full_path = f"{path}.{ext}"
        return serve_images(full_path)  # Now this function is defined above
    
    # Add handler for Next.js image optimization
    @app.route('/_next/image')
    def next_image_optimization():
        """Enhanced Next.js image optimization handler that preserves transparency"""
        # Get query parameters
        url = request.args.get('url', '')
        width = request.args.get('w', '256')
        quality = request.args.get('q', '75')
        
        logger.info(f"Image optimization request: url={url}, w={width}, q={quality}")
        
        if not url:
            return "Missing url parameter", 400
        
        # URL decode the image path
        decoded_url = urllib.parse.unquote(url)
        
        # Generate cache path
        cache_key = f"{decoded_url.replace('/', '_')}_{width}_{quality}"
        cache_dir = os.path.join(app.root_path, 'image_cache')
        os.makedirs(cache_dir, exist_ok=True)
        cache_path = os.path.join(cache_dir, cache_key)
        
        # Check if cached
        if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
            logger.info(f"Serving cached image: {cache_path}")
            
            # Determine MIME type from file extension
            content_type = "image/webp"  # Default for Next.js images
            if decoded_url.lower().endswith('.png'):
                content_type = "image/png"
            elif decoded_url.lower().endswith(('.jpg', '.jpeg')):
                content_type = "image/jpeg"
            
            # Use send_file with only supported parameters
            return send_file(
                cache_path,
                mimetype=content_type
            )
        
        # Not found in cache, try direct proxy to Next.js image optimizer
        try:
            # First try to get the image from the original Next.js optimizer
            original_url = f"https://overworld.illuvium.io/_next/image?url={url}&w={width}&q={quality}"
            logger.info(f"Fetching from original Next.js: {original_url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
                'Accept': 'image/webp,image/png,image/*,*/*;q=0.8'
            }
            
            response = requests.get(original_url, headers=headers, stream=True)
            
            if response.status_code == 200:
                # Save the image to cache (as raw binary data to preserve all image data)
                with open(cache_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                logger.info(f"Successfully downloaded image: {cache_path}")
                
                # Get the content type from the response headers
                content_type = response.headers.get('Content-Type', 'image/webp')
                
                # Serve the cached file with the correct content type
                return send_file(
                    cache_path,
                    mimetype=content_type
                )
        except Exception as e:
            logger.warning(f"Error with Next.js proxy: {str(e)}")
        
        # If Next.js proxy failed, try to serve the original image directly
        try:
            # If url starts with /, it's a local path
            if decoded_url.startswith('/'):
                # First check if image exists in local images directory
                local_path = os.path.join(app.root_path, decoded_url.lstrip('/'))
                
                if os.path.exists(local_path) and os.path.isfile(local_path):
                    logger.info(f"Serving local image: {local_path}")
                    
                    # Determine content type from file extension
                    _, ext = os.path.splitext(local_path)
                    if ext.lower() == '.webp':
                        content_type = 'image/webp'
                    elif ext.lower() == '.png':
                        content_type = 'image/png'
                    elif ext.lower() in ('.jpg', '.jpeg'):
                        content_type = 'image/jpeg'
                    else:
                        content_type = 'application/octet-stream'
                    
                    # Copy file to cache so future requests go through cache
                    shutil.copyfile(local_path, cache_path)
                    
                    # Return the file with explicit mimetype
                    return send_file(
                        local_path,
                        mimetype=content_type
                    )
                else:
                    # Try to download from original website
                    original_file_url = f"https://overworld.illuvium.io{decoded_url}"
                    logger.info(f"Trying to download original image: {original_file_url}")
                    
                    orig_response = requests.get(original_file_url, headers=headers, stream=True)
                    
                    if orig_response.status_code == 200:
                        # Save the original image
                        local_dir = os.path.dirname(local_path)
                        os.makedirs(local_dir, exist_ok=True)
                        
                        with open(local_path, 'wb') as f:
                            for chunk in orig_response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        
                        # Also save to cache
                        shutil.copyfile(local_path, cache_path)
                        
                        logger.info(f"Downloaded original image: {local_path}")
                        
                        # Get content type
                        content_type = orig_response.headers.get('Content-Type', 'image/webp')
                        
                        # Return the downloaded file
                        return send_file(
                            local_path,
                            mimetype=content_type
                        )
        
            # If we've reached here, we couldn't get the image
            logger.error(f"Failed to serve image for: {decoded_url}")
            
            # Try a default placeholder as last resort
            placeholder_path = os.path.join(app.root_path, 'static', 'placeholder.webp')
            if os.path.exists(placeholder_path):
                return send_file(placeholder_path, mimetype='image/webp')
            
            return "Image not found", 404
        except Exception as e:
            logger.error(f"Error serving image: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return "Error processing image", 500
    
    # Add direct route for JS files that are causing issues
    @app.route('/_next/<path:filename>')
    def serve_next_files(filename):
        """Direct handler for Next.js files"""
        # Special handling for problematic JS files
        if filename.endswith('.js'):
            try:
                url = f"https://overworld.illuvium.io/_next/{filename}"
                logger.info(f"Direct proxying JS: {url}")
                
                response = requests.get(url, stream=True)
                
                if response.status_code == 200:
                    # Create directory structure
                    local_path = os.path.join(app.root_path, '_next', filename)
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    
                    # Save as binary
                    with open(local_path, 'wb') as f:
                        f.write(response.content)
                    
                    # Stream directly from memory to avoid any text processing
                    return Response(
                        io.BytesIO(response.content),
                        mimetype='application/javascript',
                        headers={
                            'Content-Type': 'application/javascript; charset=utf-8',
                            'Cache-Control': 'no-cache, no-store, must-revalidate',
                            'Pragma': 'no-cache',
                            'Expires': '0',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'GET, OPTIONS, HEAD',
                            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Range, X-Requested-With, Authorization',
                            'Cross-Origin-Resource-Policy': 'cross-origin',
                            'Cross-Origin-Embedder-Policy': 'credentialless'
                        }
                    )
                else:
                    return f"File not found: {filename}", 404
            except Exception as e:
                logger.error(f"Error with JS file {filename}: {str(e)}")
                return "Error processing file", 500
        
        # Regular handling for other files
        local_path = os.path.join(app.root_path, '_next', filename)
        if os.path.exists(local_path):
            return send_file(local_path)
        
        # Proxy other files
        try:
            url = f"https://overworld.illuvium.io/_next/{filename}"
            response = requests.get(url, stream=True)
            
            if response.status_code == 200:
                # Save file
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                return send_file(local_path)
            else:
                return f"File not found: {filename}", 404
        except Exception as e:
            logger.error(f"Error with file {filename}: {str(e)}")
            return "Error processing file", 500

    # Add specific route for static/settings.js with enhanced reliability
    @app.route('/static/settings.js')
    def serve_settings_js():
        """Direct handler for settings.js file with improved content delivery"""
        logger.debug("Serving settings.js with enhanced handling")
        file_path = os.path.join(app.root_path, 'static', 'settings.js')
        
        try:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                # Read file as binary to avoid encoding issues
                with open(file_path, 'rb') as f:
                    content = f.read()
                    
                # Create a special response for this critical file
                response = Response(
                    content,
                    mimetype='application/javascript',
                    headers={
                        'Content-Type': 'application/javascript; charset=utf-8',
                        'X-Content-Type-Options': 'nosniff',
                        'Cache-Control': 'no-cache, no-store, must-revalidate',
                        'Pragma': 'no-cache',
                        'Expires': '0',
                        'Cross-Origin-Resource-Policy': 'cross-origin',
                        'Timing-Allow-Origin': '*',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET, OPTIONS, HEAD',
                        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Range, Authorization',
                        'Access-Control-Expose-Headers': 'Content-Length, Content-Range, Accept-Ranges',
                        'Access-Control-Allow-Private-Network': 'true',
                        'Access-Control-Allow-Credentials': 'true'
                    }
                )
            else:
                # Create a stub settings file with required properties
                logger.warning(f"Settings.js not found or empty, creating default version")
                stub_content = """// Default settings for Illuvium website
window.ILV_SETTINGS = {
  apiBaseUrl: window.location.origin,
  enablePolling: true,
  pollingInterval: 15000,
  debug: false,
  site_settings: {
    baseUrl: window.location.origin,
    assetPath: '/static',
    apiPath: '/api'
  },
  version: '1.0.0'
};

// Export settings for module usage
if (typeof module !== 'undefined') {
  module.exports = window.ILV_SETTINGS;
}"""
                
                # Create the settings.js file for future use
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as f:
                    f.write(stub_content)
                
                response = Response(
                    stub_content,
                    mimetype='application/javascript',
                    headers={
                        'Content-Type': 'application/javascript; charset=utf-8',
                        'X-Content-Type-Options': 'nosniff',
                        'Cache-Control': 'no-cache, no-store, must-revalidate',
                        'Pragma': 'no-cache',
                        'Expires': '0',
                        'Cross-Origin-Resource-Policy': 'cross-origin',
                        'Timing-Allow-Origin': '*',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET, OPTIONS, HEAD',
                        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Range, Authorization',
                        'Access-Control-Expose-Headers': 'Content-Length, Content-Range, Accept-Ranges',
                        'Access-Control-Allow-Private-Network': 'true',
                        'Access-Control-Allow-Credentials': 'true'
                    }
                )
            
            # Set the amplify-polling-started cookie with proper cross-site attributes
            response.set_cookie(
                'amplify-polling-started', 
                value='true',
                max_age=86400,
                samesite='None',
                secure=True,
                httponly=False,
                path='/'
            )
            
            logger.debug("Adding special headers for critical file: settings.js")
            return response
            
        except Exception as e:
            logger.error(f"Error serving settings.js: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            
            # Return a fallback settings file on error
            fallback_content = """// Fallback settings
window.ILV_SETTINGS = {
  apiBaseUrl: window.location.origin,
  enablePolling: true,
  pollingInterval: 15000,
  debug: false,
  site_settings: {
    baseUrl: window.location.origin,
    assetPath: '/static',
    apiPath: '/api'
  },
  version: '1.0.0'
};

// Export settings for module usage
if (typeof module !== 'undefined') {
  module.exports = window.ILV_SETTINGS;
}"""
            
            response = Response(
                fallback_content,
                mimetype='application/javascript',
                headers={
                    'Content-Type': 'application/javascript; charset=utf-8',
                    'X-Content-Type-Options': 'nosniff',
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Access-Control-Allow-Origin': '*'
                }
            )
            return response

    @app.route('/static/gkohcg1u379.js')
    def serve_gkohcg1u379_js():
        """Direct handler for gkohcg1u379.js file with improved content delivery"""
        logger.debug("Serving gkohcg1u379.js with enhanced handling")
        file_path = os.path.join(app.root_path, 'static', 'gkohcg1u379.js')
        if os.path.exists(file_path):
            try:
                # Read file as binary to avoid encoding issues
                with open(file_path, 'rb') as f:
                    content = f.read()
                    
                # Create a special response for this critical file
                response = Response(
                    content,
                    mimetype='application/javascript',
                    headers={
                        'Content-Type': 'application/javascript; charset=utf-8',
                        'X-Content-Type-Options': 'nosniff',
                        'Cache-Control': 'no-cache, no-store, must-revalidate',
                        'Pragma': 'no-cache',
                        'Expires': '0',
                        'Cross-Origin-Resource-Policy': 'cross-origin',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET, OPTIONS, HEAD',
                        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Range, Authorization',
                        'Access-Control-Expose-Headers': 'Content-Length, Content-Range, Accept-Ranges',
                        'Access-Control-Allow-Private-Network': 'true',
                        'Access-Control-Allow-Credentials': 'true'
                    }
                )
                
                logger.debug("Adding special headers for critical file: gkohcg1u379.js")
                return response
            except Exception as e:
                logger.error(f"Error reading gkohcg1u379.js: {str(e)}")
                
                # Return a stub script file on error
                stub_js = """// Fallback script
console.log('Using fallback gkohcg1u379.js');
// Define ILV_SETTINGS if not already defined to prevent errors
if (!window.ILV_SETTINGS) {
    window.ILV_SETTINGS = {
        site_settings: {
            baseUrl: window.location.origin,
            assetPath: '/static',
            apiPath: '/api'
        }
    };
}
"""
                response = Response(
                    stub_js,
                    mimetype='application/javascript',
                    headers={
                        'Content-Type': 'application/javascript; charset=utf-8',
                        'X-Content-Type-Options': 'nosniff',
                        'Cache-Control': 'no-cache, no-store, must-revalidate',
                        'Access-Control-Allow-Origin': '*'
                    }
                )
                return response
        else:
            logger.warning(f"File not found: {file_path}, generating stub file")
            
            # Create a stub script file
            stub_js = """// Stub gkohcg1u379.js file
console.log('Using stub gkohcg1u379.js');
// Define ILV_SETTINGS if not already defined to prevent errors
if (!window.ILV_SETTINGS) {
    window.ILV_SETTINGS = {
        site_settings: {
            baseUrl: window.location.origin,
            assetPath: '/static',
            apiPath: '/api'
        }
    };
}
"""
            # Save the stub file for future use
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(stub_js)
            
            response = Response(
                stub_js,
                mimetype='application/javascript',
                headers={
                    'Content-Type': 'application/javascript; charset=utf-8',
                    'X-Content-Type-Options': 'nosniff',
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0',
                    'Cross-Origin-Resource-Policy': 'cross-origin',
                    'Access-Control-Allow-Origin': '*'
                }
            )
            return response
    
    # Add CSS file handler for proper MIME type
    @app.route('/037b440f/index.css')
    def serve_037b440f_css():
        """Direct handler for 037b440f/index.css file with proper MIME type"""
        logger.info("Serving 037b440f/index.css with proper MIME type")
        file_path = os.path.join(app.root_path, 'static', '037b440f', 'index.css')
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                response = Response(
                    content,
                    content_type='text/css; charset=utf-8',
                )
                
                # Add CORS headers
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
                response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
                response.headers['Access-Control-Allow-Origin'] = '*'
                
                return response
            except Exception as e:
                logger.error(f"Error serving 037b440f/index.css: {str(e)}")
        
        # If file doesn't exist, create a stub CSS file with empty content
        # This prevents the CSS parsing error
        stub_css = "/* Stub CSS file for missing 037b440f/index.css */\n/* Empty CSS content to prevent parsing errors */\n"
        
        response = Response(
            stub_css,
            content_type='text/css; charset=utf-8',
        )
        
        # Add CORS headers
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
        response.headers['Access-Control-Allow-Origin'] = '*'
        
        return response
    
    # Add CSS file handler for 7c93fa6a directory
    @app.route('/7c93fa6a/index.css')
    def serve_7c93fa6a_css():
        """Direct handler for 7c93fa6a/index.css file with proper MIME type"""
        logger.info("Serving 7c93fa6a/index.css with proper MIME type")
        file_path = os.path.join(app.root_path, 'static', '7c93fa6a', 'index.css')
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                response = Response(
                    content,
                    content_type='text/css; charset=utf-8',
                )
                
                # Add CORS headers
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
                response.headers['Access-Control-Allow-Origin'] = '*'
                
                return response
            except Exception as e:
                logger.error(f"Error reading 7c93fa6a/index.css: {str(e)}")
                return f"Error reading file: {str(e)}", 500
        else:
            # Try to create an empty CSS file if it doesn't exist
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as f:
                    f.write('/* CSS file created by server */')
                logger.info(f"Created empty CSS file: {file_path}")
                
                response = Response(
                    '/* CSS file created by server */',
                    content_type='text/css; charset=utf-8',
                )
                
                # Add CORS headers
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
                response.headers['Access-Control-Allow-Origin'] = '*'
                
                return response
            except Exception as e:
                logger.error(f"Error creating CSS file: {str(e)}")
                return f"Error creating file: {str(e)}", 500
    
    # Add handlers for JS chunk files with proper MIME types
    @app.route('/037b440f/chunk.<path:filename>')
    def serve_037b440f_chunk(filename):
        """Direct handler for 037b440f/chunk.* JavaScript files with proper MIME type"""
        logger.info(f"Serving 037b440f/chunk.{filename} with proper MIME type")
        file_path = os.path.join(app.root_path, 'static', '037b440f', f'chunk.{filename}')
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                response = Response(
                    content,
                    content_type='application/javascript; charset=utf-8',
                )
                
                # Add CORS headers
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
                response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
                response.headers['Access-Control-Allow-Origin'] = '*'
                
                return response
                
            except Exception as e:
                logger.error(f"Error serving 037b440f/chunk.{filename}: {str(e)}")
        
        # If file doesn't exist, create a stub JavaScript file
        stub_js = f"// Stub file for missing 037b440f/chunk.{filename}\nconsole.log('Stub module loaded for chunk.{filename}');\nexport default {{}};"
        
        response = Response(
            stub_js,
            content_type='application/javascript; charset=utf-8',
        )
        
        # Add CORS headers
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
        response.headers['Access-Control-Allow-Origin'] = '*'
        
        return response

    @app.route('/7c93fa6a/chunk.<path:filename>')
    def serve_7c93fa6a_chunk(filename):
        """Direct handler for 7c93fa6a/chunk.* JavaScript files with proper MIME type"""
        logger.info(f"Serving 7c93fa6a/chunk.{filename} with proper MIME type")
        file_path = os.path.join(app.root_path, 'static', '7c93fa6a', f'chunk.{filename}')
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                response = Response(
                    content,
                    content_type='application/javascript; charset=utf-8',
                )
                
                # Add CORS headers
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
                response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
                response.headers['Access-Control-Allow-Origin'] = '*'
                
                return response
                
            except Exception as e:
                logger.error(f"Error serving 7c93fa6a/chunk.{filename}: {str(e)}")
        
        # If file doesn't exist, create a stub JavaScript file
        stub_js = f"// Stub file for missing 7c93fa6a/chunk.{filename}\nconsole.log('Stub module loaded for chunk.{filename}');\nexport default {{}};"
        
        response = Response(
            stub_js,
            content_type='application/javascript; charset=utf-8',
        )
        
        # Add CORS headers
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
        response.headers['Access-Control-Allow-Origin'] = '*'
        
        return response

    # Handle OPTIONS requests specifically for critical JS files
    @app.route('/static/settings.js', methods=['OPTIONS'])
    @app.route('/static/gkohcg1u379.js', methods=['OPTIONS'])
    def handle_critical_js_options():
        """Special OPTIONS handler for critical JS files"""
        logger.debug(f"Handling OPTIONS for critical JS file: {request.path}")
        response = app.make_default_options_response()
        
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, HEAD',
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Range, Authorization, Cookie, Set-Cookie',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '86400',  # 24 hours
            'Access-Control-Allow-Private-Network': 'true',
            'Access-Control-Expose-Headers': 'Set-Cookie',
            'Vary': 'Origin, Access-Control-Request-Method, Access-Control-Request-Headers',
            'Content-Type': 'application/javascript; charset=utf-8'
        })
        
        # Set the amplify-polling-started cookie with proper cross-site attributes in preflight
        response.set_cookie(
            'amplify-polling-started', 
            value='true',
            max_age=86400,
            samesite='None',
            secure=True,
            httponly=False,
            path='/'
        )
        
        return response

    # Generic static file handler with proper MIME types
    @app.route('/static/<path:path>')
    def serve_static_files(path):
        """Serve static files with enhanced security and performance headers"""
        file_path = os.path.join(app.root_path, 'static', path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                # Determine proper content type based on file extension
                ext = os.path.splitext(path)[1].lower()
                content_type = None
                
                if ext == '.js':
                    content_type = 'application/javascript; charset=utf-8'
                elif ext == '.css':
                    content_type = 'text/css; charset=utf-8'
                elif ext == '.json':
                    content_type = 'application/json; charset=utf-8'
                elif ext == '.html':
                    content_type = 'text/html; charset=utf-8'
                elif ext == '.txt':
                    content_type = 'text/plain; charset=utf-8'
                elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']:
                    # Use standard image MIME types
                    pass  # Flask will determine this automatically
                
                # Send file with optional content type if explicitly set
                if content_type:
                    response = send_file(file_path, mimetype=content_type)
                else:
                    response = send_file(file_path)
                
                # Add CORS headers for all static files
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
                
                # Cache for 1 hour by default, but browser should revalidate
                response.headers['Cache-Control'] = 'max-age=3600, must-revalidate'
                
                return response
            except Exception as e:
                logger.error(f"Error serving static file {path}: {str(e)}")
                return f"Error serving file: {str(e)}", 500
        else:
            logger.warning(f"Static file not found: {file_path}")
            return f"File not found: {path}", 404

    @app.route('/blob/<path:path>')
    def serve_blob_resources(path):
        """Handle blob resources (images and videos) for autodrone feature"""
        logger.info(f"Serving blob resource: {path}")
        
        # Create blob directory structure if it doesn't exist
        blob_dir = os.path.join(app.root_path, 'blob')
        os.makedirs(blob_dir, exist_ok=True)
        
        # Full local path for the requested resource
        local_path = os.path.join(blob_dir, path)
        local_dir = os.path.dirname(local_path)
        
        # Check if directory exists, create if not
        os.makedirs(local_dir, exist_ok=True)
        
        # Check if file exists locally
        if os.path.exists(local_path) and os.path.isfile(local_path):
            logger.info(f"Serving local blob file: {local_path}")
            return send_file(local_path)
        
        # File doesn't exist locally, try to proxy from original site
        try:
            url = f"https://overworld.illuvium.io/blob/{path}"
            logger.info(f"Proxying blob resource from: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, stream=True)
            
            if response.status_code == 200:
                # Save file for future requests
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                logger.info(f"Saved blob resource to: {local_path}")
                
                # Determine content type based on file extension
                content_type = response.headers.get('Content-Type')
                if not content_type:
                    if path.endswith('.webp'):
                        content_type = 'image/webp'
                    elif path.endswith('.webm'):
                        content_type = 'video/webm'
                    elif path.endswith('.mov'):
                        content_type = 'video/quicktime'
                    else:
                        content_type = mimetypes.guess_type(local_path)[0] or 'application/octet-stream'
                
                # Serve the downloaded file
                return send_file(
                    local_path,
                    mimetype=content_type
                )
            else:
                logger.warning(f"Failed to proxy blob resource: {response.status_code} - {url}")
                return f"Resource not found: {path}", 404
        except Exception as e:
            logger.error(f"Error proxying blob resource: {str(e)} - {url}")
            import traceback
            logger.error(traceback.format_exc())
            return f"Error fetching resource: {str(e)}", 500

    # Add this fallback route for any other autodrone resources
    @app.route('/autodrone/<path:path>')
    def serve_autodrone_resources(path):
        """Fallback handler for autodrone resources"""
        logger.info(f"Serving autodrone resource: {path}")
        
        # Check if the file exists in several possible locations
        possible_locations = [
            os.path.join(app.root_path, 'autodrone', path),
            os.path.join(app.root_path, '_next', 'autodrone', path),
            os.path.join(app.root_path, '_next', 'static', 'autodrone', path)
        ]
        
        for location in possible_locations:
            if os.path.exists(location) and os.path.isfile(location):
                logger.info(f"Found autodrone resource at: {location}")
                return send_file(location)
        
        # If not found locally, try to proxy from original site
        try:
            url = f"https://overworld.illuvium.io/autodrone/{path}"
            logger.info(f"Proxying autodrone resource from: {url}")
            
            response = requests.get(url, stream=True)
            
            if response.status_code == 200:
                # Save for future use
                save_location = os.path.join(app.root_path, 'autodrone', path)
                os.makedirs(os.path.dirname(save_location), exist_ok=True)
                
                with open(save_location, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                return send_file(save_location)
            else:
                logger.warning(f"Failed to proxy autodrone resource: {response.status_code}")
                return f"Resource not found: {path}", 404
        except Exception as e:
            logger.error(f"Error proxying autodrone resource: {str(e)}")
            return f"Error fetching resource: {str(e)}", 500

    @app.route('/_next/images/<path:path>')
    def serve_next_images(path):
        """Handle Next.js image files specifically"""
        logger.info(f"Serving Next.js image: {path}")
        
        # Create local path for the image
        local_path = os.path.join(app.root_path, '_next', 'images', path)
        local_dir = os.path.dirname(local_path)
        os.makedirs(local_dir, exist_ok=True)
        
        # Check if the file exists locally
        if os.path.exists(local_path) and os.path.isfile(local_path):
            return send_file(local_path)
        
        # Download from original site
        try:
            url = f"https://overworld.illuvium.io/_next/images/{path}"
            logger.info(f"Downloading image: {url}")
            
            response = requests.get(url, stream=True)
            
            if response.status_code == 200:
                # Create directory structure
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                # Save file
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            
                # Serve the downloaded file
                return send_file(local_path)
            else:
                logger.warning(f"Failed to download image: {response.status_code}")
                return "Image not found", 404
        except Exception as e:
            logger.error(f"Error downloading image: {str(e)}")
            return "Error processing image", 500
    
    # Add a direct OPTIONS handler for all paths to support preflight requests for CORS
    @app.route('/<path:path>', methods=['OPTIONS'])
    @app.route('/', methods=['OPTIONS'])
    def handle_options_request(path=''):
        """Handle OPTIONS requests for CORS preflight"""
        logger.debug(f"Handling CORS OPTIONS request for: {path}")
        response = make_response()
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, DELETE',
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Range, Authorization',
            'Access-Control-Max-Age': '86400',  # 24 hours
            'Vary': 'Origin, Access-Control-Request-Method, Access-Control-Request-Headers',
            'Access-Control-Allow-Private-Network': 'true',
            'Access-Control-Allow-Credentials': 'true'
        })
        return response
    
    @app.route('/header.webp')
    def serve_header_webp():
        """Direct handler for header.webp to fix 404 issues"""
        logger.info("Serving header.webp with direct handler")
        
        # First check in root directory
        file_path = os.path.join(app.root_path, 'header.webp')
        
        # If not in root, check in images directory
        if not os.path.exists(file_path):
            file_path = os.path.join(app.root_path, 'images', 'play-now', 'header', 'header.webp')
            
        if os.path.exists(file_path):
            return send_file(file_path, mimetype='image/webp')
        
        # If not found, try downloading it
        try:
            url = "https://overworld.illuvium.io/header.webp"
            logger.info(f"Downloading header.webp from {url}")
            
            response = requests.get(url, stream=True)
            
            if response.status_code == 200:
                # Save to root directory for future use
                with open(os.path.join(app.root_path, 'header.webp'), 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Serve the downloaded file
                return send_file(os.path.join(app.root_path, 'header.webp'), mimetype='image/webp')
            
            # If download fails but we have a file in images directory, use that
            if os.path.exists(os.path.join(app.root_path, 'images', 'play-now', 'header', 'header.webp')):
                return send_file(os.path.join(app.root_path, 'images', 'play-now', 'header', 'header.webp'), mimetype='image/webp')
                
            # Return a transparent 1x1 pixel webp if all else fails
            transparent_pixel = b'RIFF\x1a\x00\x00\x00WEBPVP8L\x0e\x00\x00\x00/\x00\x00\x00\x00\x00\x00\x00\x00'
            return Response(transparent_pixel, mimetype='image/webp')
            
        except Exception as e:
            logger.error(f"Error serving header.webp: {str(e)}")
            
            # Return a transparent 1x1 pixel webp if all else fails
            transparent_pixel = b'RIFF\x1a\x00\x00\x00WEBPVP8L\x0e\x00\x00\x00/\x00\x00\x00\x00\x00\x00\x00\x00'
            return Response(transparent_pixel, mimetype='image/webp')
    
    logger.info("Static files module initialized with enhanced JS handling for HTTP/2 context support")
    