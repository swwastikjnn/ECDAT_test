const mongoose = require("mongoose");

const scanSchema = new mongoose.Schema({
  projectName: { type: String, required: true },
  targetType: { type: String, enum: ["directory", "zip", "container"], required: true },
  sourceRef: { type: String, required: true },
  status: { type: String, enum: ["queued", "running", "completed", "failed"], default: "queued" },
  startedAt: { type: Date },
  completedAt: { type: Date },
  summary: {
    totalAssets: { type: Number, default: 0 },
    critical: { type: Number, default: 0 },
    high: { type: Number, default: 0 },
    medium: { type: Number, default: 0 },
    low: { type: Number, default: 0 },
    quantumSafeCount: { type: Number, default: 0 },
    quantumVulnerableCount: { type: Number, default: 0 }
  },
  cbomJson: { type: mongoose.Schema.Types.Mixed }
}, { timestamps: true });

module.exports = mongoose.model("Scan", scanSchema);