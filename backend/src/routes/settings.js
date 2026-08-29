const express = require("express");
const mongoose = require("mongoose");

const router = express.Router();

const settingsSchema = new mongoose.Schema({
  zAssumptionYears: { type: Number, default: 10 },
  weightQuantum: { type: Number, default: 0.40 },
  weightBusiness: { type: Number, default: 0.30 },
  weightMosca: { type: Number, default: 0.20 },
  weightExpiry: { type: Number, default: 0.10 }
});

const Settings = mongoose.model("Settings", settingsSchema);

async function getSettings() {
  let settings = await Settings.findOne();
  if (!settings) {
    settings = await Settings.create({});
  }
  return settings;
}

function sendResponse(res, success, data, error = null, status = 200) {
  res.status(status).json({ success, data, error });
}

router.get("/", async (req, res) => {
  try {
    const settings = await getSettings();
    sendResponse(res, true, settings);
  } catch (error) {
    sendResponse(res, false, null, error.message, 500);
  }
});

router.put("/", async (req, res) => {
  try {
    const settings = await getSettings();
    Object.assign(settings, req.body);
    await settings.save();
    sendResponse(res, true, settings);
  } catch (error) {
    sendResponse(res, false, null, error.message, 500);
  }
});

module.exports = router;