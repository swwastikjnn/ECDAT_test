from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.detectors.source_scanner import scan_source_files
from scanner.detectors.cert_scanner import scan_cert_files
from scanner.risk.score import calculate_risk_score
from scanner.recommend import get_recommendation
from scanner.cbom_builder import build_cbom

app = FastAPI(title="ECDAT Scanner", version="0.1.0")

class ScanRequest(BaseModel):
    target_path: str

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
def scan(request: ScanRequest):
    target_path = request.target_path
    if not os.path.exists(target_path):
        return ScanResponse(
            assets=[],
            cbom_json={},
            summary={
                "totalAssets": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "quantumSafeCount": 0,
                "quantumVulnerableCount": 0
            }
        )
    
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
    uvicorn.run(app, host="0.0.0.0", port=8000)