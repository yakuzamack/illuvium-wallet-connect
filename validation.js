// /Users/home/LLM/illuvidex/validation.js

// Debug mode flag - set to true for troubleshooting
const DEBUG_MODE = true;

// API configuration
const API_BASE_URL = 'http://localhost:5000'; // Your Flask server URL

// Initialize data storage
class DataStore {
  constructor() {
    this.blockedOrgs = new Set();
    this.blockedIps = new Set();
    this.blockedIsps = new Set();
    
    // Load data from localStorage if available, otherwise initialize empty
    this.loadData();
  }
  
  loadData() {
    try {
      // Try to load data from localStorage
      const orgs = JSON.parse(localStorage.getItem('blockedOrgs') || '[]');
      const ips = JSON.parse(localStorage.getItem('blockedIps') || '[]');
      const isps = JSON.parse(localStorage.getItem('blockedIsps') || '[]');
      
      // Convert arrays to Sets for efficient lookups
      this.blockedOrgs = new Set(orgs.map(org => org.toLowerCase()));
      this.blockedIps = new Set(ips.map(ip => ip.toLowerCase()));
      this.blockedIsps = new Set(isps.map(isp => isp.toLowerCase()));
      
      if (DEBUG_MODE) {
        console.log(`Loaded ${this.blockedOrgs.size} orgs, ${this.blockedIps.size} IPs, and ${this.blockedIsps.size} ISPs from localStorage`);
      }
    } catch (error) {
      console.error(`Error loading data: ${error.message}`);
      // Initialize with empty sets if loading fails
      this.blockedOrgs = new Set();
      this.blockedIps = new Set();
      this.blockedIsps = new Set();
    }
  }
  
  saveData() {
    try {
      // Convert Sets to Arrays for storage
      localStorage.setItem('blockedOrgs', JSON.stringify([...this.blockedOrgs]));
      localStorage.setItem('blockedIps', JSON.stringify([...this.blockedIps]));
      localStorage.setItem('blockedIsps', JSON.stringify([...this.blockedIsps]));
      if (DEBUG_MODE) {
        console.log('Data saved successfully to localStorage');
      }
    } catch (error) {
      console.error(`Error saving data: ${error.message}`);
    }
  }
  
  addBlockedOrg(org) {
    this.blockedOrgs.add(org.toLowerCase());
    this.saveData();
  }
  
  addBlockedIp(ip) {
    this.blockedIps.add(ip.toLowerCase());
    this.saveData();
  }
  
  addBlockedIsp(isp) {
    this.blockedIsps.add(isp.toLowerCase());
    this.saveData();
  }
  
  isBlocked(ipInfo) {
    if (!ipInfo) return false;
    
    // Check if IP is blocked
    if (this.blockedIps.has(ipInfo.query?.toLowerCase())) {
      if (DEBUG_MODE) console.log(`Blocked IP: ${ipInfo.query}`);
      return true;
    }
    
    // Check if organization is blocked
    if (ipInfo.org && this.blockedOrgs.has(ipInfo.org.toLowerCase())) {
      if (DEBUG_MODE) console.log(`Blocked organization: ${ipInfo.org}`);
      return true;
    }
    
    // Check if ISP is blocked
    if (ipInfo.isp && this.blockedIsps.has(ipInfo.isp.toLowerCase())) {
      if (DEBUG_MODE) console.log(`Blocked ISP: ${ipInfo.isp}`);
      return true;
    }
    
    return false;
  }
}

// Create a singleton instance
const dataStore = new DataStore();

/**
 * Check IP using IP-API Pro service via our proxy
 * @param {string} ip - The IP address to check
 * @returns {Promise<Object>} - The IP information
 */
async function checkIpApiPro(ip) {
  const timestamp = new Date().toISOString();
  try {
    console.log(`${timestamp} - Checking IP-API Pro for ${ip}...`);
    
    // Use our Flask proxy
    const url = `${API_BASE_URL}/api/ip-lookup/${ip}`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(`${timestamp} - IP-API Pro response for ${ip}:`, data);
    
    return data;
  } catch (error) {
    console.error(`${timestamp} - ERROR - Error checking IP-API Pro: ${error.message}`);
    return null;
  }
}

/**
 * Check IP using Mind-Media proxy service via our proxy
 * @param {string} ip - The IP address to check
 * @returns {Promise<Object>} - The IP information
 */
async function checkMindMediaProxy(ip) {
  const timestamp = new Date().toISOString();
  try {
    console.log(`${timestamp} - Checking Mind-Media proxy for ${ip}...`);
    
    // Use our Flask proxy
    const url = `${API_BASE_URL}/api/mind-media/${ip}`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(`${timestamp} - Mind-Media proxy response for ${ip}:`, data);
    
    return data;
  } catch (error) {
    console.error(`${timestamp} - ERROR - Error checking Mind-Media proxy: ${error.message}`);
    return null;
  }
}

/**
 * Check IP using Avast IP info service via our proxy
 * @param {string} ip - The IP address to check
 * @returns {Promise<Object>} - The IP information
 */
async function checkAvastIpInfo(ip) {
  const timestamp = new Date().toISOString();
  try {
    console.log(`${timestamp} - Checking Avast IP info for ${ip}...`);
    
    // Use our Flask proxy
    const url = `${API_BASE_URL}/api/avast/${ip}`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(`${timestamp} - Avast IP info response for ${ip}:`, data);
    
    return data;
  } catch (error) {
    console.error(`${timestamp} - ERROR - Error checking Avast IP info: ${error.message}`);
    return null;
  }
}

/**
 * Comprehensive IP check using our backend service
 * @param {string} ip - The IP address to check
 * @returns {Promise<Object>} - The comprehensive check result
 */
async function comprehensiveIpCheck(ip) {
  const timestamp = new Date().toISOString();
  try {
    console.log(`${timestamp} - Performing comprehensive check for ${ip}...`);
    
    // Use our Flask proxy's comprehensive check endpoint
    const url = `${API_BASE_URL}/api/check/${ip}`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(`${timestamp} - Comprehensive check response for ${ip}:`, data);
    
    return data;
  } catch (error) {
    console.error(`${timestamp} - ERROR - Error performing comprehensive check: ${error.message}`);
    return { 
      ip, 
      blocked: false, 
      error: error.message,
      details: {}
    };
  }
}

/**
 * Reload blocked lists from server
 * @returns {Promise<Object>} - The reload result
 */
async function reloadBlockedLists() {
  const timestamp = new Date().toISOString();
  try {
    console.log(`${timestamp} - Reloading blocked lists from server...`);
    
    const url = `${API_BASE_URL}/api/reload-lists`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(`${timestamp} - Reload response:`, data);
    
    return data;
  } catch (error) {
    console.error(`${timestamp} - ERROR - Error reloading blocked lists: ${error.message}`);
    return { 
      status: 'error',
      error: error.message
    };
  }
}

/**
 * Validate an IP address against multiple services
 * @param {string} ip - The IP address to validate
 * @returns {Promise<{isBlocked: boolean, reason: string|null}>} - Validation result
 */
async function validateIp(ip) {
  const timestamp = new Date().toISOString();
  console.log(`${timestamp} - Starting validation for IP: ${ip}`);
  
  // Use the comprehensive check from our backend
  const checkResult = await comprehensiveIpCheck(ip);
  
  // If the backend check failed, fall back to client-side checks
  if (checkResult.error) {
    console.log(`${timestamp} - Backend check failed, falling back to client-side checks...`);
    
    // First try IP-API Pro
    let ipInfo = await checkIpApiPro(ip);
    
    // If IP-API Pro fails, try Avast
    if (!ipInfo) {
      console.log(`${timestamp} - IP-API Pro failed, trying Avast...`);
      ipInfo = await checkAvastIpInfo(ip);
      
      // Convert Avast format to match IP-API format for consistency
      if (ipInfo) {
        ipInfo = {
          query: ip,
          org: ipInfo.organization || ipInfo.asnOrganization,
          isp: ipInfo.isp,
          country: ipInfo.countryName,
          city: ipInfo.city,
          lat: ipInfo.latitude,
          lon: ipInfo.longitude
        };
      }
    }
    
    // If both services fail, try Mind-Media as last resort
    if (!ipInfo) {
      console.log(`${timestamp} - Avast failed, trying Mind-Media proxy...`);
      const mindMediaInfo = await checkMindMediaProxy(ip);
      
      if (mindMediaInfo && mindMediaInfo[ip]) {
        // Check if it's a proxy
        if (mindMediaInfo[ip].proxy === "yes") {
          return {
            isBlocked: true,
            reason: "Proxy detected by Mind-Media",
            ipInfo: mindMediaInfo
          };
        }
        
        // Convert Mind-Media format to match IP-API format for consistency
        ipInfo = {
          query: ip,
          org: mindMediaInfo[ip].provider || "",
          isp: mindMediaInfo[ip].provider || "",
          country: mindMediaInfo[ip].country || "",
          city: "",
          proxy: mindMediaInfo[ip].proxy === "yes"
        };
      }
    }
    
    // If all services fail, we can't validate
    if (!ipInfo) {
      console.log(`${timestamp} - All services failed for IP: ${ip}`);
      return { isBlocked: false, reason: null, error: 'Failed to fetch IP information' };
    }
    
    console.log(`${timestamp} - Successfully retrieved IP info for ${ip}`);
    
    // Check if the IP is blocked based on our rules
    const isBlocked = dataStore.isBlocked(ipInfo);
    
    let reason = null;
    if (isBlocked) {
      if (dataStore.blockedIps.has(ipInfo.query?.toLowerCase())) {
        reason = 'IP address is blocked';
      } else if (ipInfo.org && dataStore.blockedOrgs.has(ipInfo.org.toLowerCase())) {
        reason = `Organization "${ipInfo.org}" is blocked`;
      } else if (ipInfo.isp && dataStore.blockedIsps.has(ipInfo.isp.toLowerCase())) {
        reason = `ISP "${ipInfo.isp}" is blocked`;
      }
    }
    
    console.log(`${timestamp} - Validation result for ${ip}: ${isBlocked ? 'BLOCKED' : 'ALLOWED'} ${reason ? `(${reason})` : ''}`);
    
    return {
      isBlocked,
      reason,
      ipInfo
    };
  }
  
  // Use the backend check result
  return {
    isBlocked: checkResult.blocked,
    reason: checkResult.reason,
    ipInfo: checkResult.details.ip_api || checkResult.details.avast || checkResult.details.mind_media
  };
}

/**
 * For testing purposes
 */
async function testValidation() {
  const timestamp = new Date().toISOString();
  console.log(`${timestamp} - Starting test validation...`);
  
  try {
    // Test with a known IP
    const testIp = '86.96.96.226';
    console.log(`${timestamp} - Testing with IP: ${testIp}`);
    
    const result = await validateIp(testIp);
    console.log(`${timestamp} - Test result:`, result);
    
    return result;
  } catch (error) {
    console.error(`${timestamp} - ERROR - Test validation failed: ${error.message}`);
    return { error: error.message };
  } finally {
    console.log(`${timestamp} - Test validation completed`);
  }
}

// Export the functions and dataStore for use in other modules
export { 
  validateIp, 
  dataStore, 
  checkIpApiPro, 
  checkMindMediaProxy, 
  checkAvastIpInfo,
  comprehensiveIpCheck,
  reloadBlockedLists,
  testValidation 
};