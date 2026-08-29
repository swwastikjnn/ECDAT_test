const axios = require("axios");

const SCANNER_URL = process.env.SCANNER_URL || "http://localhost:8000";

async function callScanner(targetPath) {
  try {
    const response = await axios.post(`${SCANNER_URL}/scan`, {
      target_path: targetPath
    }, {
      timeout: 300000
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(`Scanner error: ${error.response.status} - ${JSON.stringify(error.response.data)}`);
    } else if (error.request) {
      throw new Error(`Scanner unreachable at ${SCANNER_URL}. Is the Python scanner running?`);
    } else {
      throw new Error(`Scanner request failed: ${error.message}`);
    }
  }
}

async function checkScannerHealth() {
  try {
    const response = await axios.get(`${SCANNER_URL}/health`, { timeout: 5000 });
    return response.data.status === "ok";
  } catch {
    return false;
  }
}

module.exports = { callScanner, checkScannerHealth };