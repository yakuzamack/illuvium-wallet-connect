// Default settings for Illuvium website
window.ILV_SETTINGS = {
  apiBaseUrl: window.location.origin,
  enablePolling: true,
  pollingInterval: 15000,
  debug: false,
  site_settings: {
    baseUrl: window.location.origin,
    assetPath: '/static',
    apiPath: '/api'
  },
  version: '1.0.0'
};

// Export settings for module usage
if (typeof module !== 'undefined') {
  module.exports = window.ILV_SETTINGS;
}