import os
from functools import wraps
import requests
from flask import request, render_template, jsonify

# Constants
BLOCKED_IPS = set()
BLOCKED_ISPS = set()
BLOCKED_ORGS = set()

def load_blocked_items(filepath):
    """Load blocked items from a file into a set."""
    items = set()
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip().lower()
                    if line and not line.startswith('#'):
                        items.add(line)
    except Exception as e:
        print(f"Error loading {filepath}: {str(e)}")
    return items

def get_client_ip():
    """Get the client's real IP address, considering X-Forwarded-For header"""
    if request.headers.getlist("X-Forwarded-For"):
        # If behind a proxy, get the real IP
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    else:
        # If not behind a proxy, get the direct IP
        ip = request.remote_addr
    return ip

def validate_ip_server_side(ip):
    """Server-side validation function
    Returns a tuple of (is_blocked, reason)
    """
    # Check if IP is directly blocked
    if ip.lower() in BLOCKED_IPS:
        return True, "IP address is directly blocked"
    
    # Check with IP-API Pro
    try:
        ip_api_response = requests.get(
            f"https://pro.ip-api.com/json/{ip}?fields=66842623&key=ipapiq9SFY1Ic4",
            headers={
                'Accept': '*/*',
                'Origin': 'https://members.ip-api.com',
                'Referer': 'https://members.ip-api.com/',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
        )
        ip_api_data = ip_api_response.json()
        
        # Check if ISP or organization is blocked
        if "isp" in ip_api_data and ip_api_data["isp"].lower() in BLOCKED_ISPS:
            return True, f"ISP '{ip_api_data['isp']}' is blocked"
        if "org" in ip_api_data and ip_api_data["org"].lower() in BLOCKED_ORGS:
            return True, f"Organization '{ip_api_data['org']}' is blocked"
    except Exception as e:
        print(f"IP-API Pro error: {str(e)}")
    
    # Check with Avast
    try:
        avast_response = requests.get(
            f"https://ip-info.ff.avast.com/v2/info?ip={ip}",
            headers={
                'Accept': '*/*',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
        )
        avast_data = avast_response.json()
        
        # Check if organization from Avast is blocked
        if "organization" in avast_data and avast_data["organization"].lower() in BLOCKED_ORGS:
            return True, f"Organization '{avast_data['organization']}' is blocked"
        if "isp" in avast_data and avast_data["isp"].lower() in BLOCKED_ISPS:
            return True, f"ISP '{avast_data['isp']}' is blocked"
    except Exception as e:
        print(f"Avast error: {str(e)}")
    
    # Check with Mind-Media proxy
    try:
        # Simple GET request without any special headers or payload
        mind_media_response = requests.get(f"http://proxy.mind-media.com/block/proxycheck.php?ip={ip}")
        
        # Handle raw Y/N response
        raw_response = mind_media_response.text.strip()
        
        # Check if proxy is detected
        if raw_response == "Y":
            return True, "Proxy detected by Mind-Media"
    except Exception as e:
        print(f"Mind-Media error: {str(e)}")
    
    return False, None

def validate_ip_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip validation for API endpoints and static files
        if request.path.startswith('/api/') or request.path.startswith('/static/'):
            return f(*args, **kwargs)
        
        # Get the user's IP address
        user_ip = get_client_ip()
        
        # Skip validation for localhost
        if user_ip == '127.0.0.1' or user_ip == 'localhost':
            return f(*args, **kwargs)
        
        # Validate the IP
        is_blocked, reason = validate_ip_server_side(user_ip)
        if is_blocked:
            # Log the blocked access
            app.logger.warning(f"Blocked access from IP {user_ip}: {reason}")
            # Render the 403 template with the reason
            return render_template('403.html', reason=reason), 403
            
        # IP is allowed, proceed with the request
        return f(*args, **kwargs)
    return decorated_function

# API endpoint for frontend validation
def check_ip_api(ip):
    """API endpoint to check an IP and return result to frontend"""
    is_blocked, reason = validate_ip_server_side(ip)
    return jsonify({
        'ip': ip,
        'blocked': is_blocked,
        'reason': reason
    })

def init_ip_validation(app):
    """Initialize the IP validation module"""
    global BLOCKED_IPS, BLOCKED_ISPS, BLOCKED_ORGS
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Load blocked lists
    BLOCKED_IPS = load_blocked_items('data/ips.txt')
    BLOCKED_ISPS = load_blocked_items('data/isps.txt')
    BLOCKED_ORGS = load_blocked_items('data/organisations.txt')
    
    app.logger.info(f"Loaded {len(BLOCKED_IPS)} blocked IPs, {len(BLOCKED_ISPS)} blocked ISPs, and {len(BLOCKED_ORGS)} blocked organizations")
    
    # Register the API endpoint for IP checking
    app.add_url_rule('/api/check/<ip>', 'check_ip', check_ip_api)
    
    # Register an API endpoint to reload blocked lists
    @app.route('/api/reload-lists')
    def reload_lists():
        BLOCKED_IPS = load_blocked_items('data/ips.txt')
        BLOCKED_ISPS = load_blocked_items('data/isps.txt')
        BLOCKED_ORGS = load_blocked_items('data/organisations.txt')
        app.logger.info(f"Reloaded {len(BLOCKED_IPS)} blocked IPs, {len(BLOCKED_ISPS)} blocked ISPs, and {len(BLOCKED_ORGS)} blocked organizations")
        return jsonify({'status': 'success'})
    
    # Add the validation decorator to handle all routes
    @app.before_request
    def validate_request():
        # Skip validation for API endpoints and static files
        if request.path.startswith('/api/') or request.path.startswith('/static/'):
            return None
        
        # Get the user's IP address
        user_ip = get_client_ip()
        
        # Skip validation for localhost
        if user_ip == '127.0.0.1' or user_ip == 'localhost':
            return None
        
        # Validate the IP
        is_blocked, reason = validate_ip_server_side(user_ip)
        if is_blocked:
            # Log the blocked access
            app.logger.warning(f"Blocked access from IP {user_ip}: {reason}")
            # Render the 403 template with the reason
            return render_template('403.html', reason=reason), 403
        
        # IP is allowed, proceed with the request
        return None

    @app.route('/api/test-ip-validation')
    def test_ip_validation():
        user_ip = get_client_ip()
        is_blocked, reason = validate_ip_server_side(user_ip)
        return jsonify({
            'ip': user_ip,
            'blocked': is_blocked,
            'reason': reason
        })