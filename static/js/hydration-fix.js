// Fix for React hydration errors
document.addEventListener('DOMContentLoaded', function() {
  console.log('Hydration fix initialized');
  
  // Detect hydration errors and log details
  const originalError = console.error;
  console.error = function() {
    // Check if this is a hydration error
    if (arguments[0] && 
        (arguments[0].includes('Hydration failed') || 
         arguments[0].includes('Minified React error #418') ||
         arguments[0].includes('Minified React error #423'))) {
      
      console.log('Hydration error detected. Details:');
      
      // Try to help with debugging
      const rootElements = document.querySelectorAll('[id^="__next"]');
      console.log('Root elements:', rootElements);
      
      // Log warning about potential issues
      console.warn('This may be caused by:');
      console.warn('1. Different content being rendered server-side vs client-side');
      console.warn('2. Different React versions between server and client');
      console.warn('3. Issues with script loading order or timing');
    }
    
    // Call original console.error with all arguments
    originalError.apply(console, arguments);
  };
});