// ECDAT Frontend Configuration
// Single source of truth for API base URL
// To change for production (e.g., Render deployment), modify ONLY this line:
const API_BASE_URL = "http://localhost:3000";

// Derived constants - do not modify these directly
const API_BASE = `${API_BASE_URL}/api`;
const SCANNER_URL = "http://localhost:8000";

// Export for module usage (if using ES modules)
// For plain script tags, these are available globally
window.ECDAT_CONFIG = {
  API_BASE_URL,
  API_BASE,
  SCANNER_URL
};