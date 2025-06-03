// Modal Bundle JS
// This serves as a lightweight connector between React and our vanilla JS implementation

console.log('[Modal] Bundle loaded and initialized');

(function() {
  // When the DOM is loaded, check if our wallet-connect.js is available
  document.addEventListener('DOMContentLoaded', function() {
    console.log('[Modal] DOM loaded, looking for wallet connect');
    
    // Check if WalletConnect is available from wallet-connect.js
    if (window.WalletConnect) {
      console.log('[Modal] WalletConnect found, ready to handle clicks');
      
      // If the global wallet connect button exists, hook it up
      const globalButton = document.getElementById('global-wallet-connect');
      if (globalButton) {
        console.log('[Modal] Found global wallet connect button, adding click handler');
        globalButton.addEventListener('click', function(e) {
          e.preventDefault();
          window.WalletConnect.showModal();
        });
      }
    } else {
      console.warn('[Modal] WalletConnect not found, will check again later');
      
      // Try again after a delay in case scripts load out of order
      setTimeout(function() {
        if (window.WalletConnect) {
          console.log('[Modal] WalletConnect found on second attempt');
          
          // Try to hook up the button again
          const globalButton = document.getElementById('global-wallet-connect');
          if (globalButton) {
            globalButton.addEventListener('click', function(e) {
              e.preventDefault();
              window.WalletConnect.showModal();
            });
          }
        } else {
          console.error('[Modal] WalletConnect still not available');
        }
      }, 1000);
    }
  });
  
  // Create a helper to show wallet modal from anywhere
  window.showWalletModal = function() {
    if (window.WalletConnect && window.WalletConnect.showModal) {
      window.WalletConnect.showModal();
      return true;
    }
    return false;
  };
  
  // Also hook up any react button events
  document.addEventListener('click', function(event) {
    const target = event.target;
    
    // Check if this is a wallet connect button from the original site
    if (target && target.closest) {
      const walletButton = target.closest('[class*="connect"],[class*="wallet"],[id*="connect"],[id*="wallet"]');
      if (walletButton) {
        console.log('[Modal] Intercepted a wallet button click from original React app');
        setTimeout(function() {
          window.showWalletModal();
        }, 100);
      }
    }
  }, true); // Use capture phase to get events first
  
  // Listen for React component requests to show wallet
  window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'SHOW_WALLET_MODAL') {
      console.log('[Modal] Received message to show wallet modal');
      window.showWalletModal();
    }
  });
  
  console.log('[Modal] Bundle initialization complete');
})(); 