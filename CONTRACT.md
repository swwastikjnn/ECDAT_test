# CONTRACT.md
### ECDAT — The Rules Every Team Member Must Follow
### Breaking any rule in this file breaks everyone else's code simultaneously.

---

## THE DAILY HEALTH CHECK — RUN THIS BEFORE EVERY COMMIT

Every person runs this test before pushing any code to GitHub.
If it fails, do NOT commit. Fix it first.

### Step 1 — Start the scanner
```bash
cd scanner
uvicorn main:app --reload --port 8000
```

### Step 2 — Run the contract test (open a new terminal)
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"target_path": "./scanner/sample-vulnerable-app"}'
```

### Step 3 — Check the response shape
The response MUST contain all of these fields. If any are missing, the contract is broken.

```json
{
  "assets": [
    {
      "algorithm": "...",
      "file_path": "...",
      "line_number": 0,
      "language": "...",
      "asset_type": "...",
      "quantum_risk": "...",
      "mosca_urgent": true,
      "risk_score": 0,
      "recommendation": "...",
      "business_criticality": "..."
    }
  ],
  "cbom_json": {},
  "summary": {
    "totalAssets": 0,
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0,
    "quantumSafeCount": 0,
    "quantumVulnerableCount": 0
  }
}
```

### Step 4 — Check Node backend (if M5 is complete)
```bash
curl http://localhost:3000/api/scans
```
Expected: `{ "success": true, "data": [...] }`

### Step 5 — Only if both pass, commit your code
```bash
git add .
git commit -m "M1: regex scanner complete — contract test passing"
git push origin feature/your-branch-name
```

---

## PORTS — LOCKED. NEVER CHANGE.

| Service | Port |
|---|---|
| Python FastAPI scanner | 8000 |
| Node Express backend | 3000 |
| Frontend dev server | 5173 |

---

## BRANCH NAMING — USE THESE EXACT NAMES

```
feature/m0-scaffold
feature/m1-source-scanner
feature/m2-cert-scanner
feature/m3-risk-engine
feature/m4-cbom-builder
feature/m5-backend
feature/m6-frontend-p1
feature/m6-frontend-p2
```

Never commit directly to `main`.
Create a pull request. Another team member reviews it.
Only merge when the contract test passes.

---

## FILE OWNERSHIP — DO NOT EDIT EACH OTHER'S FILES

| Files | Owner | Others must not edit |
|---|---|---|
| `scanner/main.py` | Person 4 | ✓ hands off |
| `scanner/detectors/source_scanner.py` | Person 2 | ✓ hands off |
| `scanner/detectors/rules.py` | Person 2 | ✓ hands off |
| `scanner/detectors/cert_scanner.py` | Person 3 | ✓ hands off |
| `scanner/risk/classify.py` | Person 4 | ✓ hands off |
| `scanner/risk/mosca.py` | Person 4 | ✓ hands off |
| `scanner/risk/score.py` | Person 4 | ✓ hands off |
| `scanner/recommend.py` | Person 4 | ✓ hands off |
| `scanner/cbom_builder.py` | Person 4 | ✓ hands off |
| `backend/src/` (all files) | Person 1 | ✓ hands off |
| `frontend/` (all files) | Person 5, 6 | ✓ hands off |
| `BRAIN.md` | Everyone updates | Update after every session |
| `CONTRACT.md` | Person 1 maintains | Team agrees before changes |

---

## THE ONE THING THAT CANNOT CHANGE WITHOUT TEAM AGREEMENT

The shape of the scanner's JSON response (what Python returns to Node).

If Person 4 changes what the scanner returns:
- Person 1's backend breaks (it reads those fields)
- Person 5 and 6's frontend breaks (it displays those fields)
- Two people's work is instantly broken

Process for changing the contract:
1. Post the proposed change in the team group chat
2. All affected members agree
3. Update CONTRACT.md and BRAIN.md
4. All affected members update their code before anyone commits

---

## ENVIRONMENT VARIABLES — WHAT GOES WHERE

```
backend/.env          ← NEVER commit this file
  MONGODB_URI=your_atlas_connection_string
  SCANNER_URL=http://localhost:8000
  PORT=3000

scanner/.env          ← nothing required for MVP

frontend/.env         ← nothing required for MVP
```

`backend/.env.example` is committed with placeholder values:
```
MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/ecdat
SCANNER_URL=http://localhost:8000
PORT=3000
```

---

## WHAT BELONGS IN .gitignore (already configured — do not remove)

```
node_modules/
venv/
.env
__pycache__/
*.pyc
dist/
build/
.DS_Store
```

---

## COMMIT MESSAGE FORMAT

```
M1: what you did — contract test status

Examples:
M1: regex scanner detects RSA and AES in Python/Java — contract passing
M3: Mosca calculator complete — contract passing
M5: POST /api/scans wired to scanner — contract passing
```

Always say whether the contract test is passing or failing in your commit message.