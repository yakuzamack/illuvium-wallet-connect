// Click Tracker JavaScript
// This script tracks button clicks and dispatches custom events

console.log('[ClickTracker] Initializing click tracking system...');

(function() {
    // Config
    const config = window.APP_CONFIG || {};
    const clickConfig = config.clicks || {
        debug: true,
        logAllClicks: true
    };
    
    // Track if we're currently processing a click to avoid duplicate processing
    let isProcessingClick = false;
    
    // Performance-optimized function to handle clicks
    // The main handler is wrapped in requestAnimationFrame to prevent long-running handlers
    function handleButtonClick(event) {
        // Skip if already processing
        if (isProcessingClick) return;
        isProcessingClick = true;
        
        // Use requestAnimationFrame to defer non-critical processing to next frame
        requestAnimationFrame(() => {
            try {
                const target = event.target;
                
                // Find the button or link (if the target is a child of a button)
                const button = target.closest('button');
                const link = target.closest('a');
                
                // Get the element that was clicked (button, link, or other)
                const elem = button || link || target;
                
                // Skip if not a clickable element
                if (!elem) {
                    isProcessingClick = false;
                    return;
                }
                
                // Extract information about the clicked element
                const buttonInfo = {
                    id: elem.id || '',
                    text: elem.textContent?.trim() || '',
                    tag: elem.tagName?.toLowerCase() || '',
                    class: elem.className || '',
                    href: elem.href || '',
                    type: elem.type || '',
                    timestamp: Date.now()
                };
                
                // Log click if debug mode is enabled
                if (clickConfig.debug && clickConfig.logAllClicks) {
                    console.log('[ClickTracker] Button clicked:', buttonInfo);
                }
                
                // Create custom event with button information
                const customEvent = new CustomEvent('ILLUVIUM_BUTTON_CLICKED', {
                    detail: {
                        buttonInfo,
                        originalEvent: event
                    },
                    bubbles: true,
                    cancelable: true
                });
                
                // Dispatch custom event
                document.dispatchEvent(customEvent);
            } catch (error) {
                console.error('[ClickTracker] Error processing click:', error);
            } finally {
                isProcessingClick = false;
            }
        });
    }
    
    // Use passive event listener for better performance
    document.addEventListener('click', handleButtonClick, { passive: true });
    
    // Also track touch events for mobile
    document.addEventListener('touchend', (e) => {
        // Only process if it looks like a tap (not a scroll)
        if (e.changedTouches && e.changedTouches.length === 1) {
            // Check if this touch event is likely a tap rather than a scroll
            const touch = e.changedTouches[0];
            if (!touch.movementX && !touch.movementY) {
                handleButtonClick(e);
            }
        }
    }, { passive: true });
    
    console.log('[ClickTracker] Button click tracking initialized with performance optimizations');
})(); 