# BRAIN.md
### ECDAT — Enterprise Cryptographic Discovery & Analysis Tool
### SIH Problem Statement: 26164
### READ THIS BEFORE WRITING A SINGLE LINE OF CODE

---

## HOW TO USE THIS FILE

This file is the shared memory of the entire project.
Every team member pastes this file + CONTRACT.md into their Claude chat
before asking Claude to write anything.

Without this file, Claude has no idea what the rest of the team has built.
With this file, any Claude chat on any device becomes instantly productive.

Update the CURRENT STATE section every single time you finish a work session.
This file is more important than any individual piece of code.

---

## WHAT THIS PROJECT IS

ECDAT is a tool that scans an organisation's source code and certificates
to build a CBOM (Cryptographic Bill of Materials) — an inventory of every
cryptographic asset in use. It then assesses each asset's exposure to future
quantum computers using Mosca's inequality (X + Y > Z) and recommends
NIST post-quantum replacements.

One-line pitch: "We find your broken crypto before quantum computers do."

---

## CURRENT STATE

```
Last updated:        2026-08-27
Last thing done:     M0 Scaffold + Hello World complete - all three services scaffolded
Currently broken:    Need to install dependencies and test
Next thing to do:    Install Python deps, install Node deps, start services, run contract test
```

### Milestone Status
```
M0 — Scaffold + Hello World:         [x] COMPLETE
M1 — Source Scanner (regex):         [x] COMPLETE
M2 — Certificate Scanner:            [x] COMPLETE
M3 — Risk + Recommendation Engine:   [x] COMPLETE
M4 — CBOM Output:                    [x] COMPLETE
M5 — Node Backend + MongoDB:         [x] COMPLETE
M6 — Frontend (6 pages):             [x] COMPLETE
```
Change [ ] to [x] when complete. Change to [~] if in progress.

---

## ARCHITECTURE

```
Browser (port 5173)
   ↓ REST fetch/axios
Node.js + Express (port 3000)
   ↓ POST http://localhost:8000/scan
Python + FastAPI scanner (port 8000)
   ↓ reads files from disk
Target source code / certificates
   ↓ results stored in
MongoDB Atlas (free M0 cluster)
```

Node and Python talk over plain HTTP.
Frontend talks to Node only — never directly to Python.
Python talks to nobody — it only receives requests and returns results.

---

## PORTS — NEVER CHANGE THESE

```
Python FastAPI scanner:  8000
Node Express backend:    3000
Frontend dev server:     5173
```

If you change a port, every other person's code breaks immediately.

---

## LIVE URLS (fill in as they become available)

```
GitHub repo:        https://github.com/[FILL IN]
MongoDB Atlas:      connection string lives in backend/.env only
Deployed backend:   [FILL IN when deployed]
Deployed frontend:  [FILL IN when deployed]
```

---

## REPOSITORY STRUCTURE

```
ecdat/
├── scanner/                          ← Python FastAPI (Person 2, 3, 4 work here)
│   ├── main.py                       ← FastAPI app, /scan endpoint
│   ├── detectors/
│   │   ├── source_scanner.py         ← regex + AST detection (Person 2)
│   │   ├── cert_scanner.py           ← certificate/key parsing (Person 3)
│   │   └── rules.py                  ← detection rule tables (Person 2)
│   ├── risk/
│   │   ├── classify.py               ← quantum-vulnerability classification (Person 4)
│   │   ├── mosca.py                  ← Mosca's inequality calculator (Person 4)
│   │   └── score.py                  ← composite risk score (Person 4)
│   ├── recommend.py                  ← PQC recommendation engine (Person 4)
│   ├── cbom_builder.py               ← CycloneDX CBOM builder (Person 4)
│   ├── requirements.txt
│   └── sample-vulnerable-app/        ← test fixtures (Person 1 creates on Day 1)
│       ├── legacy_hash.py
│       ├── LegacyAuth.java
│       └── old_crypto.c
├── backend/                          ← Node.js Express (Person 1 works here)
│   ├── src/
│   │   ├── server.js
│   │   ├── routes/scans.js
│   │   ├── models/Scan.js
│   │   ├── models/Asset.js
│   │   └── services/scannerClient.js ← axios calls to Python
│   ├── package.json
│   └── .env.example
├── frontend/                         ← HTML/CSS/JS (Person 5, 6 work here)
│   └── index.html / src/
├── BRAIN.md                          ← THIS FILE
├── CONTRACT.md                       ← API shapes and rules
├── TEAM_GUIDE.md                     ← who does what
├── README.md
└── .gitignore
```

---

## TECH STACK — DO NOT SUBSTITUTE WITHOUT TEAM AGREEMENT

| Layer | Choice | Who owns it |
|---|---|---|
| Scanner engine | Python 3.11+, FastAPI, uvicorn | Person 2, 3, 4 |
| Code parsing | tree-sitter + tree-sitter-languages + regex | Person 2 |
| Certificate parsing | cryptography, pyOpenSSL, pyjks | Person 3 |
| CBOM generation | cyclonedx-python-lib | Person 4 |
| Backend API | Node.js LTS, Express | Person 1 |
| Database | MongoDB Atlas free M0, Mongoose | Person 1 |
| File upload | multer + adm-zip | Person 1 |
| Frontend | Plain HTML/CSS/JS + Chart.js via CDN | Person 5, 6 |

---

## API CONTRACT (the most important section in this file)

### Contract 1 — Python Scanner endpoint

```
POST http://localhost:8000/scan
Content-Type: application/json

Request body:
{
  "target_path": "/absolute/path/to/code/folder"
}

Response (200 OK):
{
  "assets": [
    {
      "algorithm":            "RSA-2048",
      "file_path":            "src/auth/Login.java",
      "line_number":          42,
      "language":             "java",
      "asset_type":           "algorithm",
      "quantum_risk":         "critical",
      "mosca_urgent":         true,
      "risk_score":           85,
      "recommendation":       "Replace with ML-KEM (FIPS 203)",
      "business_criticality": "medium"
    }
  ],
  "cbom_json": { ... },
  "summary": {
    "totalAssets":           12,
    "critical":              4,
    "high":                  3,
    "medium":                3,
    "low":                   2,
    "quantumSafeCount":      2,
    "quantumVulnerableCount": 10
  }
}
```

### Contract 2 — Node Backend endpoints (what frontend calls)

```
All responses follow this envelope — no exceptions:
{ "success": true/false, "data": {...} or [...], "error": "message or null" }

POST   /api/scans                    Start a scan
GET    /api/scans                    List all scans
GET    /api/scans/:id                One scan detail + summary
GET    /api/scans/:id/assets         All assets for a scan (paginated)
GET    /api/scans/:id/cbom           Download CBOM JSON file
PATCH  /api/scans/:id/assets/:aid    Update businessCriticality on one asset
GET    /api/settings                 Get Mosca Z value + weights
PUT    /api/settings                 Update Mosca Z value + weights
```

### Contract 3 — MongoDB document shapes

```javascript
// scans collection
{
  projectName:  String,
  targetType:   "directory" | "zip" | "container",
  sourceRef:    String,
  status:       "queued" | "running" | "completed" | "failed",
  startedAt:    Date,
  completedAt:  Date,
  summary: {
    totalAssets: Number, critical: Number, high: Number,
    medium: Number, low: Number,
    quantumSafeCount: Number, quantumVulnerableCount: Number
  },
  cbomJson: Object
}

// assets collection
{
  scanId:               ObjectId,
  algorithm:            String,
  filePath:             String,
  lineNumber:           Number,
  language:             String,
  assetType:            "algorithm" | "certificate" | "protocol",
  quantumRisk:          "critical" | "high" | "medium" | "safe",
  moscaUrgent:          Boolean,
  riskScore:            Number,
  recommendation:       String,
  businessCriticality:  "critical" | "high" | "medium" | "low"
}

// settings collection (one document)
{
  zAssumptionYears:     Number,   // default 10
  weightQuantum:        Number,   // default 0.40
  weightBusiness:       Number,   // default 0.30
  weightMosca:          Number,   // default 0.20
  weightExpiry:         Number    // default 0.10
}
```

---

## RISK SCORING LOGIC (Person 4 implements this — everyone else reads it)

### Quantum vulnerability classification
```
RSA, ECDSA, ECDH    → critical   (broken by Shor's algorithm)
DSA, DH             → critical
MD5, SHA-1          → critical   (already broken classically)
DES, 3DES, RC4      → critical   (weak, broken classically)
AES-128, SHA-256    → medium     (weakened by Grover's)
AES-256, SHA-384+   → safe
ML-KEM, ML-DSA, SLH-DSA → safe  (NIST PQC standards)
```

### Mosca's inequality
```python
def is_mosca_urgent(x, y, z):
    # X = years data must stay confidential
    # Y = years migration will take
    # Z = years until cryptographically relevant quantum computer
    return (x + y) > z  # True = already in the risk window
```

### Composite risk score (0–100)
```
risk_score =
    0.40 × quantum_vulnerability  (critical=100, medium=50, safe=0)
  + 0.30 × business_criticality  (critical=100, high=75, medium=50, low=25)
  + 0.20 × mosca_urgency         (urgent=100, not urgent=30)
  + 0.10 × expiry_proximity      (cert <1yr=100, <3yr=60, else=20, N/A=0)

Buckets: 80–100=Critical, 60–79=High, 35–59=Medium, 0–34=Low
```

---

## ENVIRONMENT VARIABLES

```
backend/.env (never commit this file):
  MONGODB_URI=mongodb+srv://...
  SCANNER_URL=http://localhost:8000

scanner/.env (nothing required for MVP)
```

`.env.example` files with placeholder values are committed.
`.env` files with real values are NEVER committed.
Both are in .gitignore.

---

## GUARDRAILS EVERY PERSON MUST FOLLOW

- Never change a port number without updating CONTRACT.md and telling the team
- Never rename a MongoDB collection
- Never change the shape of the scanner's JSON response without updating CONTRACT.md
- Never commit node_modules/, venv/, .env, __pycache__/ — they are in .gitignore
- Never commit directly to main — use feature branches
- Guard against zip-slip: validate extracted file paths stay inside target directory
- Skip unreadable files gracefully — wrap all file reads in try/except
- Exclude node_modules/, .git/, venv/, build/ from scans

---

## WHAT TO PASTE INTO A NEW CLAUDE CHAT

```
Read these two files completely before writing any code:
1. BRAIN.md (paste full content)
2. CONTRACT.md (paste full content)

Today's task: [describe in 2 sentences what you need help with]
Relevant existing files: [paste only the 1-3 files relevant to today's task]
```

Do NOT paste the entire codebase. Paste only what Claude needs for today's task.
The contracts and architecture in BRAIN.md tell Claude everything else it needs.