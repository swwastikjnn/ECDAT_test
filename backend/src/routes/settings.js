const express = require("express");
const mongoose = require("mongoose");

const router = express.Router();
const Settings = require("../models/Settings");

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
