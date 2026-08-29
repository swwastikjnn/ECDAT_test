require("dotenv").config();
const express = require("express");
const cors = require("cors");
const mongoose = require("mongoose");
const scansRouter = require("./routes/scans");
const settingsRouter = require("./routes/settings");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use("/api/scans", scansRouter);
app.use("/api/settings", settingsRouter);

app.get("/health", (req, res) => {
  res.json({ status: "ok", service: "ecdat-backend" });
});

mongoose.connect(process.env.MONGODB_URI)
  .then(() => {
    console.log("Connected to MongoDB");
    app.listen(PORT, () => {
      console.log(`Backend running on port ${PORT}`);
    });
  })
  .catch((err) => {
    console.error("MongoDB connection error:", err);
    process.exit(1);
  });