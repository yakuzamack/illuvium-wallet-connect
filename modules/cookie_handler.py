from flask import request, make_response
import logging

logger = logging.getLogger(__name__)

def init_cookie_handler(app):
    """Initialize cookie handling middleware"""
    
    @app.after_request
    def handle_cookies(response):
        """Modify cookies to address SameSite issues"""
        # Get all set-cookie headers
        cookies = response.headers.getlist('Set-Cookie')
        
        # No cookies to process
        if not cookies:
            return response
        
        # Clear existing cookies
        response.headers.pop('Set-Cookie', None)
        
        # Process each cookie
        for cookie in cookies:
            # Handle amplify cookies specifically
            if 'amplify' in cookie.lower():
                # Add SameSite=None and Secure attributes for cross-origin cookies
                if 'SameSite' not in cookie:
                    cookie += '; SameSite=None; Secure'
                else:
                    # Replace existing SameSite attribute
                    parts = cookie.split(';')
                    new_parts = []
                    for part in parts:
                        if 'samesite' not in part.lower():
                            new_parts.append(part)
                    new_parts.append('SameSite=None')
                    new_parts.append('Secure')
                    cookie = '; '.join(new_parts)
                
                logger.debug(f"Modified amplify cookie: {cookie}")
            
            # Add the modified/original cookie back
            response.headers.add('Set-Cookie', cookie)
        
        return response
    
    # Add CORS headers to allow cookies in cross-origin requests
    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get('Origin')
        if origin:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
        
    logger.info("Cookie handler initialized")