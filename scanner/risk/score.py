from scanner.risk.classify import classify_quantum_risk
from scanner.risk.mosca import is_mosca_urgent, get_default_x_years, DEFAULT_Y_YEARS, DEFAULT_Z_YEARS

QUANTUM_WEIGHT = 0.40
BUSINESS_WEIGHT = 0.30
MOSCA_WEIGHT = 0.20
EXPIRY_WEIGHT = 0.10

QUANTUM_SCORES = {"critical": 100, "high": 75, "medium": 50, "safe": 0}
BUSINESS_SCORES = {"critical": 100, "high": 75, "medium": 50, "low": 25}
MOSCA_SCORES = {True: 100, False: 30}

def calculate_risk_score(
    algorithm: str,
    business_criticality: str = "medium",
    asset_type: str = "algorithm",
    key_size: int = 0,
    not_valid_after: str = None,
    z_years: int = DEFAULT_Z_YEARS
) -> dict:
    quantum_risk = classify_quantum_risk(algorithm)
    quantum_score = QUANTUM_SCORES.get(quantum_risk, 50)
    
    business_score = BUSINESS_SCORES.get(business_criticality, 50)
    
    x_years = get_default_x_years(asset_type, business_criticality)
    mosca_urgent = is_mosca_urgent(x_years, DEFAULT_Y_YEARS, z_years)
    mosca_score = MOSCA_SCORES[mosca_urgent]
    
    expiry_score = 0
    if not_valid_after and asset_type == "certificate":
        from datetime import datetime, timezone
        try:
            expiry = datetime.fromisoformat(not_valid_after.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            days_until_expiry = (expiry - now).days
            if days_until_expiry < 365:
                expiry_score = 100
            elif days_until_expiry < 1095:
                expiry_score = 60
            else:
                expiry_score = 20
        except Exception:
            expiry_score = 0
    
    risk_score = (
        QUANTUM_WEIGHT * quantum_score +
        BUSINESS_WEIGHT * business_score +
        MOSCA_WEIGHT * mosca_score +
        EXPIRY_WEIGHT * expiry_score
    )
    risk_score = int(round(risk_score))
    
    if risk_score >= 80:
        risk_bucket = "Critical"
    elif risk_score >= 60:
        risk_bucket = "High"
    elif risk_score >= 35:
        risk_bucket = "Medium"
    else:
        risk_bucket = "Low"
    
    return {
        "quantum_risk": quantum_risk,
        "mosca_urgent": mosca_urgent,
        "risk_score": risk_score,
        "risk_bucket": risk_bucket
    }