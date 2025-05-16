from flask import request, current_app, make_response
import logging
import mimetypes
import os

logger = logging.getLogger(__name__)

def init_security_headers(app):
    """Initialize security headers for the Flask application"""
    
    # Register proper JS MIME types - this is crucial for modules to load correctly
    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('application/javascript', '.mjs')
    mimetypes.add_type('text/javascript', '.js')  # Fallback for older browsers
    
    @app.after_request
    def set_secure_headers(response):
        """Set security-related headers on all responses"""
        # Basic security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Add Content-Security-Policy header
        response.headers['Content-Security-Policy'] = "default-src 'self' * data: blob: 'unsafe-inline' 'unsafe-eval'; connect-src *; font-src * data:; img-src * data: blob:; media-src * data: blob:; script-src * 'unsafe-inline' 'unsafe-eval'; style-src * 'unsafe-inline';"
        
        # Fix cookies for cross-site contexts
        fix_cookies_for_cross_site(response)
        
        return response
    
    @app.route('/api/set-amplify-cookie', methods=['GET', 'OPTIONS'])
    def set_amplify_cookie():
        """Endpoint to set the amplify-polling-started cookie with proper flags"""
        resp = app.make_response("Cookie set")
        resp.set_cookie(
            'amplify-polling-started', 
            value='true',
            samesite='None', 
            secure=True,
            httponly=False,
            path='/'
        )
        add_cors_headers(resp)
        return resp
    
    def fix_cookies_for_cross_site(response):
        """Fix cookies for cross-site contexts by setting SameSite=None and Secure flags"""
        if response.headers.get('Set-Cookie'):
            # Flask's Headers object doesn't have getall, use the standard way to get all cookies
            cookies = response.headers.getlist('Set-Cookie')
            if cookies:
                # Clear existing cookies
                del response.headers['Set-Cookie']
                
                for cookie in cookies:
                    if 'SameSite=' not in cookie:
                        if 'amplify' in cookie or 'polling' in cookie:
                            # Fix specifically for amplify cookies
                            cookie = cookie.rstrip(';') + '; SameSite=None; Secure;'
                        else:
                            # For other cookies, use SameSite=Lax as a safer default
                            cookie = cookie.rstrip(';') + '; SameSite=Lax;'
                    
                    response.headers.add('Set-Cookie', cookie)
        
        return response
    
    @app.after_request
    def add_cors_headers(response):
        """Add CORS headers to all responses"""
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        response.headers.add('Cross-Origin-Resource-Policy', 'cross-origin')
        return response
        
    app.logger.info("Security headers middleware initialized with SameSite cookie handling")
    return app