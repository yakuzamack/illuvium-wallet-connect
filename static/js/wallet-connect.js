// WalletConnect JS Implementation
// This script provides the WalletConnect functionality for the Illuvium site

(function() {
  console.log('[WalletConnect] Initializing wallet connect module');
  
  // Configuration
  const config = {
    debugMode: true,
    modalId: 'wallet-connect-modal',
    wallets: [
      { id: 'metamask', name: 'MetaMask', icon: 'https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg' },
      { id: 'coinbase', name: 'Coinbase', icon: 'https://www.svgrepo.com/show/331345/coinbase.svg' },
      { id: 'walletconnect', name: 'WalletConnect', icon: 'https://raw.githubusercontent.com/WalletConnect/walletconnect-assets/master/Icon/Blue%20(Default)/Icon.svg' },
      { id: 'trust', name: 'Trust Wallet', icon: 'https://trustwallet.com/assets/images/media/assets/trust_platform.svg' }
    ]
  };
  
  // Store config globally
  window.WALLET_CONFIG = config;
  
  // Create HTML for modal
  function getModalHtml() {
    let walletsHtml = '';
    
    config.wallets.forEach(wallet => {
      walletsHtml += `
        <div class="wallet-option" onclick="window.WalletConnect.connectWallet('${wallet.id}')">
          <img src="${wallet.icon}" alt="${wallet.name}" style="width: 32px; height: 32px; margin-right: 12px;">
          <span>${wallet.name}</span>
        </div>
      `;
    });
    
    return `
      <div style="color: white; font-family: 'Arial', sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
          <h2 style="margin: 0; font-size: 20px; color: white;">Connect Wallet</h2>
          <div onclick="window.WalletConnect.hideModal()" style="cursor: pointer; font-size: 24px; color: #8e87ba;">&times;</div>
        </div>
        <p style="margin-bottom: 20px; color: #b4b0ce; font-size: 14px;">
          Connect your wallet to access Illuvium features
        </p>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          ${walletsHtml}
        </div>
      </div>
    `;
  }
  
  // Create modal element
  function createModal() {
    console.log('[WalletConnect] Creating modal');
    
    // Check if modal already exists
    const existingModal = document.getElementById(config.modalId);
    if (existingModal) {
      return existingModal;
    }
    
    // Create modal HTML
    const modalHtml = getModalHtml();
    
    // Create modal container
    const modal = document.createElement('div');
    modal.id = config.modalId;
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    modal.style.display = 'none';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';
    modal.style.zIndex = '999999';
    modal.style.opacity = '0';
    modal.style.transition = 'opacity 0.3s ease';
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
    
    // Style wallet options
    setTimeout(() => {
      const walletOptions = modal.querySelectorAll('.wallet-option');
      walletOptions.forEach(option => {
        option.style.display = 'flex';
        option.style.alignItems = 'center';
        option.style.padding = '12px';
        option.style.borderRadius = '8px';
        option.style.backgroundColor = '#2a2456';
        option.style.cursor = 'pointer';
        option.style.transition = 'background-color 0.2s';
        
        // Add hover effect
        option.addEventListener('mouseenter', () => {
          option.style.backgroundColor = '#332e69';
        });
        
        option.addEventListener('mouseleave', () => {
          option.style.backgroundColor = '#2a2456';
        });
      });
    }, 100);
    
    // Assemble modal
    modal.appendChild(modalContent);
    
    // Add to body
    document.body.appendChild(modal);
    
    console.log("[WalletConnect] Modal created and added to DOM");
    
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
    
    // Notify for analytics/tracking
    document.dispatchEvent(new CustomEvent('wallet:modalOpened'));
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
    
    // Notify for analytics/tracking
    document.dispatchEvent(new CustomEvent('wallet:modalClosed'));
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
    console.log("[WalletConnect] Module initialized");
    // Create the modal to ensure it's ready
    createModal();
    
    // Set up event handlers for buttons
    setupButtonHandlers();
  }
  
  // Setup button handlers to detect and intercept wallet connect buttons
  function setupButtonHandlers() {
    if (config.debugMode) {
      console.log('[WalletConnect] Setting up button handlers');
    }
    
    // Setup the global wallet connect button if it exists
    const globalWalletButton = document.getElementById('global-wallet-connect');
    if (globalWalletButton) {
      globalWalletButton.addEventListener('click', (event) => {
        event.preventDefault();
        showModal();
      });
      console.log('[WalletConnect] Global wallet button handler added');
    }
    
    // Use MutationObserver to watch for buttons being added to the DOM
    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.type === 'childList' && mutation.addedNodes.length) {
          mutation.addedNodes.forEach(node => {
            if (node.nodeType === 1) { // Element node
              checkAndBindWalletButtons(node);
            }
          });
        }
      }
    });
    
    // Start observing the document body for DOM changes
    observer.observe(document.body, { 
      childList: true, 
      subtree: true 
    });
    
    // Initial scan of existing buttons
    checkAndBindWalletButtons(document.body);
  }
  
  // Check for and bind wallet buttons
  function checkAndBindWalletButtons(rootElement) {
    // Possible button selectors
    const selectors = [
      'button', 'a', '[role="button"]', '[type="button"]',
      '[class*="connect"]', '[class*="wallet"]', 
      '[id*="connect"]', '[id*="wallet"]'
    ];
    
    selectors.forEach(selector => {
      rootElement.querySelectorAll(selector).forEach(element => {
        // Check if this looks like a wallet button
        const text = (element.textContent || '').toLowerCase();
        const classes = (element.className || '').toLowerCase();
        const id = (element.id || '').toLowerCase();
        
        if (
          text.includes('connect') || text.includes('wallet') ||
          classes.includes('connect') || classes.includes('wallet') ||
          id.includes('connect') || id.includes('wallet') ||
          text.includes('sign in') || text.includes('login')
        ) {
          // Only add the event listener if we haven't already
          if (!element._walletConnectBound) {
            // Mark element as already processed
            element._walletConnectBound = true;
            
            if (config.debugMode) {
              console.log('[WalletConnect] Found wallet button:', element);
            }
            
            // Add click listener with capturing to ensure we get the event
            element.addEventListener('click', (event) => {
              if (config.debugMode) {
                console.log('[WalletConnect] Wallet button clicked, showing modal');
              }
              
              // We don't prevent default because we still want the original button
              // functionality to execute, which might trigger other UI updates
              
              // Show our modal
              setTimeout(() => {
                showModal();
              }, 100);
            }, true);
          }
        }
      });
    });
  }
  
  // Initialize when DOM is loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  
  // Make wallet connect available on window object
  // This is needed for integration with other scripts
  console.log('[WalletConnect] Module loaded and ready');
})(); 