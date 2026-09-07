from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import sys
from fastapi import FastAPI, UploadFile, File, Form
import tempfile
import zipfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.detectors.source_scanner import scan_source_files
from scanner.detectors.cert_scanner import scan_cert_files
from scanner.risk.score import calculate_risk_score
from scanner.recommend import get_recommendation
from scanner.cbom_builder import build_cbom

app = FastAPI(title="ECDAT Scanner", version="0.1.0")

class ScanRequest(BaseModel):
    target_path: str
    z_years: int = 10
    weight_quantum: float = 0.40
    weight_business: float = 0.30
    weight_mosca: float = 0.20
    weight_expiry: float = 0.10

class Asset(BaseModel):
    algorithm: str
    file_path: str
    line_number: int
    language: str
    asset_type: str
    quantum_risk: str
    mosca_urgent: bool
    risk_score: int
    recommendation: str
    business_criticality: str

class ScanResponse(BaseModel):
    assets: List[Asset]
    cbom_json: Dict[str, Any]
    summary: Dict[str, int]

@app.get("/health")
def health():
    return {"status": "ok", "service": "ecdat-scanner"}

@app.post("/scan", response_model=ScanResponse)
async def scan(
    file: UploadFile = File(...),
    z_years: int = Form(10),
    weight_quantum: float = Form(0.40),
    weight_business: float = Form(0.30),
    weight_mosca: float = Form(0.20),
    weight_expiry: float = Form(0.10),
):
    tmp_dir = tempfile.mkdtemp()
    try:
        zip_path = os.path.join(tmp_dir, "upload.zip")
        with open(zip_path, "wb") as f:
            f.write(await file.read())

        extract_dir = os.path.join(tmp_dir, "extracted")
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_dir)

        target_path = extract_dir

        source_findings = scan_source_files(target_path)
        cert_findings = scan_cert_files(target_path)
        all_findings = source_findings + cert_findings

        enriched_assets = []
        for finding in all_findings:
            risk_result = calculate_risk_score(
                algorithm=finding["algorithm"],
                business_criticality=finding.get("business_criticality", "medium"),
                asset_type=finding.get("asset_type", "algorithm"),
                key_size=finding.get("key_size", 0),
                not_valid_after=finding.get("not_valid_after"),
                z_years=z_years,
                weight_quantum=weight_quantum,
                weight_business=weight_business,
                weight_mosca=weight_mosca,
                weight_expiry=weight_expiry,
            )
            finding["quantum_risk"] = risk_result["quantum_risk"]
            finding["mosca_urgent"] = risk_result["mosca_urgent"]
            finding["risk_score"] = risk_result["risk_score"]
            finding["recommendation"] = get_recommendation(finding["algorithm"])
            enriched_assets.append(finding)

        cbom_json = build_cbom(enriched_assets, project_name="ECDAT Scan")

        summary = {
            "totalAssets": len(enriched_assets),
            "critical": sum(1 for a in enriched_assets if a["risk_score"] >= 80),
            "high": sum(1 for a in enriched_assets if 60 <= a["risk_score"] < 80),
            "medium": sum(1 for a in enriched_assets if 35 <= a["risk_score"] < 60),
            "low": sum(1 for a in enriched_assets if a["risk_score"] < 35),
            "quantumSafeCount": sum(1 for a in enriched_assets if a["quantum_risk"] == "safe"),
            "quantumVulnerableCount": sum(1 for a in enriched_assets if a["quantum_risk"] != "safe"),
        }

        return ScanResponse(assets=enriched_assets, cbom_json=cbom_json, summary=summary)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
    
    source_findings = scan_source_files(target_path)
    cert_findings = scan_cert_files(target_path)
    all_findings = source_findings + cert_findings
    
    enriched_assets = []
    for finding in all_findings:
        risk_result = calculate_risk_score(
            algorithm=finding["algorithm"],
            business_criticality=finding.get("business_criticality", "medium"),
            asset_type=finding.get("asset_type", "algorithm"),
            key_size=finding.get("key_size", 0),
            not_valid_after=finding.get("not_valid_after"),
            z_years=request.z_years,
            weight_quantum=request.weight_quantum,
            weight_business=request.weight_business,
            weight_mosca=request.weight_mosca,
            weight_expiry=request.weight_expiry,
        )
        finding["quantum_risk"] = risk_result["quantum_risk"]
        finding["mosca_urgent"] = risk_result["mosca_urgent"]
        finding["risk_score"] = risk_result["risk_score"]
        finding["recommendation"] = get_recommendation(finding["algorithm"])
        enriched_assets.append(finding)
    
    cbom_json = build_cbom(enriched_assets, project_name="ECDAT Scan")
    
    summary = {
        "totalAssets": len(enriched_assets),
        "critical": sum(1 for a in enriched_assets if a["risk_score"] >= 80),
        "high": sum(1 for a in enriched_assets if 60 <= a["risk_score"] < 80),
        "medium": sum(1 for a in enriched_assets if 35 <= a["risk_score"] < 60),
        "low": sum(1 for a in enriched_assets if a["risk_score"] < 35),
        "quantumSafeCount": sum(1 for a in enriched_assets if a["quantum_risk"] == "safe"),
        "quantumVulnerableCount": sum(1 for a in enriched_assets if a["quantum_risk"] != "safe"),
    }
    
    return ScanResponse(
        assets=enriched_assets,
        cbom_json=cbom_json,
        summary=summary
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
