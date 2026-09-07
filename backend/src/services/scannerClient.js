const axios = require("axios");
const fs = require("fs");
const FormData = require("form-data"); // npm install form-data if not already present

const SCANNER_URL = process.env.SCANNER_URL || "http://localhost:8000";

async function callScanner(zipFilePath, settings = {}) {
  try {
    const form = new FormData();
    form.append("file", fs.createReadStream(zipFilePath));
    form.append("z_years", settings.z_years ?? 10);
    form.append("weight_quantum", settings.weight_quantum ?? 0.40);
    form.append("weight_business", settings.weight_business ?? 0.30);
    form.append("weight_mosca", settings.weight_mosca ?? 0.20);
    form.append("weight_expiry", settings.weight_expiry ?? 0.10);

    const response = await axios.post(`${SCANNER_URL}/scan`, form, {
      headers: form.getHeaders(),
      timeout: 300000,
      maxBodyLength: Infinity,
      maxContentLength: Infinity
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
