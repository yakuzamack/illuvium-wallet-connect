from flask import request, send_file, jsonify
import os
import requests
import logging
import mimetypes
import random
import time

logger = logging.getLogger(__name__)

# User agents to rotate through
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
]

def init_media_proxy(app):
    """Initialize media proxy handling"""
    # Create necessary directories
    os.makedirs(os.path.join(app.root_path, 'media_cache'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'static', 'fallbacks'), exist_ok=True)
    
    @app.route('/proxy/media/<path:path>')
    def proxy_media(path):
        """Proxy requests to media files with proper CORS headers"""
        logger.info(f"Proxying media request: {path}")
        
        # Normalize the path
        if path.startswith('/'):
            path = path[1:]
        
        # Local cache path for the media file
        cache_path = os.path.join(app.root_path, 'media_cache', path)
        
        # Check if file exists in cache
        if os.path.exists(cache_path) and os.path.isfile(cache_path):
            return serve_media_file(cache_path)
        
        # Try to download from original source
        try:
            # Create directory structure
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            
            # Possible URLs to try for the media file
            urls_to_try = [
                f"https://media.illuvium.io/{path}",
                f"https://overworld.illuvium.io/{path}",
                f"https://illuvium.io/{path}"
            ]
            
            for url in urls_to_try:
                try:
                    logger.info(f"Trying to download from: {url}")
                    response = requests.head(url, timeout=5)
                    
                    if response.status_code == 200:
                        # URL exists, download the file
                        download_response = requests.get(url, stream=True)
                        
                        if download_response.status_code == 200:
                            # Save the file to cache
                            with open(cache_path, 'wb') as f:
                                for chunk in download_response.iter_content(chunk_size=8192):
                                    if chunk:
                                        f.write(chunk)
                            
                            logger.info(f"Downloaded media file to: {cache_path}")
                            return serve_media_file(cache_path)
                except Exception as e:
                    logger.warning(f"Error downloading from {url}: {str(e)}")
                    continue
            
            # If we get here, none of the URLs worked - serve a fallback
            fallback_path = get_fallback_for_path(path, app.root_path)
            if fallback_path:
                logger.info(f"Serving fallback: {fallback_path}")
                return serve_media_file(fallback_path)
            
            # No fallback available
            logger.error(f"No file or fallback found for: {path}")
            return "", 404
            
        except Exception as e:
            logger.error(f"Error proxying media: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return "Error processing media", 500

    def get_fallback_for_path(path, root_path):
        """Get the appropriate fallback for a given path"""
        # Check extension
        _, ext = os.path.splitext(path)
        if not ext:
            ext = '.mp4'  # Default extension
        
        # Normalize extension
        ext = ext.lower()
        
        # Look for a fallback with the same extension
        fallback_path = os.path.join(root_path, 'static', 'fallbacks', f"fallback{ext}")
        if os.path.exists(fallback_path):
            return fallback_path
        
        # If we don't have a fallback with the same extension, try common video formats
        for alt_ext in ['.mp4', '.webm']:
            fallback_path = os.path.join(root_path, 'static', 'fallbacks', f"fallback{alt_ext}")
            if os.path.exists(fallback_path):
                return fallback_path
        
        # No fallback found
        return None

    def serve_media_file(file_path):
        """Serve a media file with proper CORS and content type headers"""
        if not os.path.exists(file_path):
            return "File not found", 404
        
        # Determine content type based on file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # Map extensions to MIME types
        content_types = {
            '.mp4': 'video/mp4',
            '.webm': 'video/webm',
            '.ogg': 'video/ogg',
            '.mov': 'video/quicktime',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.webp': 'image/webp',
            '.gif': 'image/gif'
        }
        
        content_type = content_types.get(ext, 'application/octet-stream')
        
        # Create a Flask response
        response = send_file(
            file_path,
            mimetype=content_type,
            conditional=True,
            etag=True,
            add_etags=True,
            max_age=86400  # Cache for 1 day
        )
        
        # Add CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept'
        response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
        
        # Ensure content type is set correctly
        response.headers['Content-Type'] = content_type
        
        return response
    
    # Add route for direct media paths
    @app.route('/media/<path:path>')
    def direct_media_path(path):
        """Handle direct media paths"""
        return proxy_media(path)
    
    # Create fallback videos if they don't exist
    def create_fallback_videos():
        """Create fallback videos for different formats"""
        fallback_dir = os.path.join(app.root_path, 'static', 'fallbacks')
        os.makedirs(fallback_dir, exist_ok=True)
        
        # List of extensions to create fallbacks for
        extensions = ['.mp4', '.webm']
        
        for ext in extensions:
            fallback_path = os.path.join(fallback_dir, f"fallback{ext}")
            if not os.path.exists(fallback_path) or os.path.getsize(fallback_path) < 1000:
                try:
                    # Create a small placeholder video
                    # In a real implementation, you would download or create actual video files
                    # This is just a placeholder that will satisfy the browser's content type detection
                    with open(fallback_path, 'wb') as f:
                        if ext == '.mp4':
                            # Minimal valid MP4 file header
                            f.write(bytes.fromhex('000000206674797069736F6D0000020069736F6D69736F326176633100000000'))
                        elif ext == '.webm':
                            # Minimal valid WebM file header
                            f.write(bytes.fromhex('1A45DFA3010000000000000000000000000000000000000000000000000000'))
                    
                    logger.info(f"Created fallback placeholder: {fallback_path}")
                except Exception as e:
                    logger.error(f"Error creating fallback: {str(e)}")
    
    # Create fallbacks on startup
    create_fallback_videos()
    logger.info("Media proxy initialized with fallbacks")