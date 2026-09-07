const mongoose = require("mongoose");

const settingsSchema = new mongoose.Schema({
  zAssumptionYears: { type: Number, default: 10 },
  weightQuantum: { type: Number, default: 0.40 },
  weightBusiness: { type: Number, default: 0.30 },
  weightMosca: { type: Number, default: 0.20 },
  weightExpiry: { type: Number, default: 0.10 }
});

module.exports = mongoose.models.Settings || mongoose.model("Settings", settingsSchema);
