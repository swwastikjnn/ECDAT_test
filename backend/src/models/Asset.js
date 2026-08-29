const mongoose = require("mongoose");

const assetSchema = new mongoose.Schema({
  scanId: { type: mongoose.Schema.Types.ObjectId, ref: "Scan", required: true },
  algorithm: { type: String, required: true },
  filePath: { type: String, required: true },
  lineNumber: { type: Number, default: 0 },
  language: { type: String },
  assetType: { type: String, enum: ["algorithm", "certificate", "protocol", "library"], default: "algorithm" },
  quantumRisk: { type: String, enum: ["critical", "high", "medium", "safe"], default: "medium" },
  moscaUrgent: { type: Boolean, default: false },
  riskScore: { type: Number, default: 0 },
  recommendation: { type: String },
  businessCriticality: { type: String, enum: ["critical", "high", "medium", "low"], default: "medium" },
  keySize: { type: Number },
  signatureAlgorithm: { type: String },
  notValidAfter: { type: Date },
  alias: { type: String }
}, { timestamps: true });

module.exports = mongoose.model("Asset", assetSchema);