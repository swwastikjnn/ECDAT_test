const express = require("express");
const multer = require("multer");
const AdmZip = require("adm-zip");
const path = require("path");
const fs = require("fs");
const Scan = require("../models/Scan");
const Asset = require("../models/Asset");
const { callScanner } = require("../services/scannerClient");

const router = express.Router();

const upload = multer({ dest: "uploads/" });

function sendResponse(res, success, data, error = null, status = 200) {
  res.status(status).json({ success, data, error });
}

router.post("/", upload.single("zipFile"), async (req, res) => {
  try {
    const { projectName, targetType, sourceRef } = req.body;
    let targetPath = sourceRef;

    if (targetType === "zip" && req.file) {
      const extractDir = `uploads/extracted_${Date.now()}`;
      fs.mkdirSync(extractDir, { recursive: true });
      const zip = new AdmZip(req.file.path);
      zip.extractAllTo(extractDir, true);
      targetPath = extractDir;
    }

    const scan = new Scan({
      projectName: projectName || "Unnamed Scan",
      targetType: targetType || "directory",
      sourceRef: sourceRef || targetPath,
      status: "running",
      startedAt: new Date()
    });
    await scan.save();

    const scannerResult = await callScanner(targetPath);

    const assets = scannerResult.assets.map(a => ({
      scanId: scan._id,
      algorithm: a.algorithm,
      filePath: a.file_path,
      lineNumber: a.line_number,
      language: a.language,
      assetType: a.asset_type,
      quantumRisk: a.quantum_risk,
      moscaUrgent: a.mosca_urgent,
      riskScore: a.risk_score,
      recommendation: a.recommendation,
      businessCriticality: a.business_criticality
    }));

    if (assets.length > 0) {
      await Asset.insertMany(assets);
    }

    scan.status = "completed";
    scan.completedAt = new Date();
    scan.summary = scannerResult.summary;
    scan.cbomJson = scannerResult.cbom_json;
    await scan.save();

    sendResponse(res, true, { scanId: scan._id, ...scannerResult });
  } catch (error) {
    sendResponse(res, false, null, error.message, 500);
  }
});

router.get("/", async (req, res) => {
  try {
    const scans = await Scan.find().sort({ createdAt: -1 }).limit(50);
    sendResponse(res, true, scans);
  } catch (error) {
    sendResponse(res, false, null, error.message, 500);
  }
});

router.get("/:id", async (req, res) => {
  try {
    const scan = await Scan.findById(req.params.id);
    if (!scan) return sendResponse(res, false, null, "Scan not found", 404);
    sendResponse(res, true, scan);
  } catch (error) {
    sendResponse(res, false, null, error.message, 500);
  }
});

router.get("/:id/assets", async (req, res) => {
  try {
    const { page = 1, limit = 50, risk, search } = req.query;
    const query = { scanId: req.params.id };
    if (risk) query.quantumRisk = risk;
    if (search) query.algorithm = { $regex: search, $options: "i" };

    const assets = await Asset.find(query)
      .skip((page - 1) * limit)
      .limit(parseInt(limit))
      .sort({ riskScore: -1 });
    const total = await Asset.countDocuments(query);

    sendResponse(res, true, { assets, total, page: parseInt(page), limit: parseInt(limit) });
  } catch (error) {
    sendResponse(res, false, null, error.message, 500);
  }
});

router.get("/:id/cbom", async (req, res) => {
  try {
    const scan = await Scan.findById(req.params.id);
    if (!scan) return sendResponse(res, false, null, "Scan not found", 404);
    res.setHeader("Content-Type", "application/json");
    res.setHeader("Content-Disposition", `attachment; filename="cbom-${scan._id}.json"`);
    sendResponse(res, true, scan.cbomJson);
  } catch (error) {
    sendResponse(res, false, null, error.message, 500);
  }
});

router.patch("/:id/assets/:assetId", async (req, res) => {
  try {
    const { businessCriticality } = req.body;
    const asset = await Asset.findOneAndUpdate(
      { _id: req.params.assetId, scanId: req.params.id },
      { businessCriticality },
      { new: true }
    );
    if (!asset) return sendResponse(res, false, null, "Asset not found", 404);
    sendResponse(res, true, asset);
  } catch (error) {
    sendResponse(res, false, null, error.message, 500);
  }
});

module.exports = router;