# ECDAT - Enterprise Cryptographic Discovery & Analysis Tool

SIH Problem Statement: 26164

## Overview

ECDAT scans an organization's source code and certificates to build a **CBOM (Cryptographic Bill of Materials)** - an inventory of every cryptographic asset in use. It then assesses each asset's exposure to future quantum computers using **Mosca's inequality** (X + Y > Z) and recommends **NIST post-quantum replacements**.

## Architecture

```
Frontend (HTML/CSS/JS, port 5173)
   ↓ REST calls
Backend API — Node.js + Express (port 3000)
   ↓ POST http://localhost:8000/scan
Scanner microservice — Python + FastAPI (port 8000)
   ↓ reads files from disk
Target source code / certificates
   ↓ results stored in
MongoDB Atlas (free M0 cluster)
```

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB Atlas account (free M0 cluster)

### 1. Set up the Python scanner
```bash
cd scanner
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
Scanner runs on http://localhost:8000

### 2. Set up the Node backend
```bash
cd backend
cp .env.example .env
# Edit .env with your MongoDB URI
npm install
npm run dev
```
Backend runs on http://localhost:3000

### 3. Open the frontend
Open `frontend/index.html` in a browser (or serve with any static server on port 5173).

### 4. Run a test scan
In the frontend, go to the **Scan** tab:
- Project Name: "Test Scan"
- Scan Type: "Local Directory"
- Directory Path: `./scanner/sample-vulnerable-app`
- Click "Start Scan"

Then view results in **Dashboard**, **Assets**, **Risk**, **Recommendations**, and **Export** tabs.

## API Contract

### Scanner (Python) - POST /scan
```json
Request:  { "target_path": "/absolute/path/to/code" }
Response: { "assets": [...], "cbom_json": {}, "summary": {...} }
```

### Backend (Node) - Key Endpoints
- `POST /api/scans` - Start a scan
- `GET /api/scans` - List scans
- `GET /api/scans/:id` - Scan detail
- `GET /api/scans/:id/assets` - Assets for a scan
- `GET /api/scans/:id/cbom` - Download CBOM JSON
- `PATCH /api/scans/:id/assets/:aid` - Update business criticality
- `GET /api/settings` - Get Mosca Z value
- `PUT /api/settings` - Update Mosca Z value

## Milestones
- M0: Scaffold + Hello World ✓
- M1: Source Scanner (regex)
- M2: Certificate Scanner
- M3: Risk + Recommendation Engine
- M4: CBOM Output
- M5: Node Backend + MongoDB
- M6: Frontend (6 pages)

## Team
- Krish — Risk Engine + CBOM Builder
- Swwastik — Backend Architect
- Divay — Source Code Scanner
- Yash — Certificate Scanner
- Samridhi — Frontend Part 1
- Anant — Frontend Part 2