import sys
sys.path.insert(0, 'D:/Swway/Hackathons/SIH 26/test proj')
from scanner.cbom_builder import build_cbom

assets = [
    {
        "algorithm": "RSA",
        "file_path": "test.java",
        "line_number": 10,
        "language": "java",
        "asset_type": "algorithm",
        "quantum_risk": "critical",
        "mosca_urgent": False,
        "risk_score": 61,
        "recommendation": "Replace with ML-KEM (FIPS 203)",
        "business_criticality": "medium"
    }
]

cbom = build_cbom(assets)
print(cbom)