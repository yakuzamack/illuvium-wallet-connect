from flask import request, current_app
import logging

logger = logging.getLogger(__name__)

def init_security_headers(app):
    """Initialize security headers handling"""
    
    @app.after_request
    def add_security_headers(response):
        """Add necessary security headers to all responses"""
        # Set a proper Content-Security-Policy
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://esm.sh; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: blob: https://media.illuvium.io https://overworld.illuvium.io; "
            "media-src 'self' data: blob: https://media.illuvium.io; "
            "connect-src 'self' https://media.illuvium.io https://overworld.illuvium.io wss: https:; "
            "frame-src 'self' https://illuvium.io https://overworld.illuvium.io; "
            "object-src 'none'; "
            "base-uri 'self';"
        )
        
        # Set other security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        return response
        
    logger.info("Security headers middleware initialized")