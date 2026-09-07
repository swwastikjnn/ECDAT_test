# Environment Variables — Plain English Summary

This document explains every environment variable the ECDAT project now uses, what it's for, and where to get real values.

---

## Backend Variables (`backend/.env`)

### `MONGODB_URI`
**What it is:** The connection string for your MongoDB Atlas database.  
**Where to get it:** 
1. Log into [MongoDB Atlas](https://cloud.mongodb.com)
2. Click **Connect** on your cluster
3. Choose **Drivers** → **Node.js**
4. Copy the connection string (looks like `mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/ecdat`)
5. Replace `USERNAME`, `PASSWORD`, and `cluster` with your actual credentials
6. The database name at the end (`ecdat`) can stay as-is or be changed

**Example:** `mongodb+srv://myuser:mypass@mycluster.mongodb.net/ecdat`

---

### `SCANNER_URL`
**What it is:** The URL where the Python scanner service is running. The Node backend calls this to start scans.  
**Where to get it:**
- **Local development:** `http://localhost:8000` (if you run the scanner locally on the default port)
- **Render deployment:** The public URL Render gives your scanner service (e.g., `https://ecdat-scanner.onrender.com`)

**Example:** `http://localhost:8000`

---

### `PORT`
**What it is:** The port the Node.js backend listens on.  
**Where to get it:**
- **Local development:** Defaults to `3000` if not set
- **Render:** Render automatically sets this — **do not override** on Render

**Example:** `3000`

---

## Scanner Variables (`scanner/.env`)

### `PORT`
**What it is:** The port the Python FastAPI scanner listens on.  
**Where to get it:**
- **Local development:** Defaults to `8000` if not set
- **Render:** Render automatically sets this — **do not override** on Render

**Example:** `8000`

---

## Quick Start for New Team Members

1. **Copy the example file:**
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Edit `.env` with your real values:**
   - Get your MongoDB Atlas connection string (see above)
   - Set `SCANNER_URL` to where your scanner runs (local: `http://localhost:8000`)
   - `PORT` can stay as `3000`

3. **Copy scanner example (optional):**
   ```bash
   cd ../scanner
   cp .env.example .env
   ```

4. **Start services:**
   ```bash
   # Terminal 1 - Scanner
   cd scanner
   uvicorn main:app --reload --port 8000
   
   # Terminal 2 - Backend
   cd backend
   npm run dev
   ```

---

## Render Deployment

When deploying to Render:
1. **Backend service:** Set `MONGODB_URI` and `SCANNER_URL` in Render dashboard Environment Variables. Render sets `PORT` automatically.
2. **Scanner service:** Set `PORT` in Render dashboard (or let Render set it). No other vars needed.
3. **Frontend:** No environment variables needed for MVP.

---

## Verification Checklist

- [ ] Backend starts and connects to MongoDB (logs "Connected to MongoDB")
- [ ] Backend logs "Backend running on port 3000" (or your PORT value)
- [ ] Scanner starts and logs "Uvicorn running on http://0.0.0.0:8000" (or your PORT value)
- [ ] `GET http://localhost:3000/health` returns `{ "status": "ok", "service": "ecdat-backend" }`
- [ ] `GET http://localhost:8000/health` returns `{ "status": "ok", "service": "ecdat-scanner" }`
- [ ] `POST http://localhost:3000/api/scans` with a zip file works end-to-end