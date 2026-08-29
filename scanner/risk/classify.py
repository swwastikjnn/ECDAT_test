QUANTUM_VULNERABILITY = {
    "RSA": "critical",
    "ECC": "critical",
    "ECDSA": "critical",
    "ECDH": "critical",
    "Ed25519": "critical",
    "DSA": "critical",
    "DH": "critical",
    "MD5": "critical",
    "SHA-1": "critical",
    "SHA1": "critical",
    "DES": "critical",
    "3DES": "critical",
    "RC4": "critical",
    "AES-128": "medium",
    "SHA-256": "medium",
    "SHA256": "medium",
    "AES-256": "safe",
    "AES256": "safe",
    "SHA-384": "safe",
    "SHA384": "safe",
    "SHA-512": "safe",
    "SHA512": "safe",
    "SHA-3": "safe",
    "SHA3": "safe",
    "ML-KEM": "safe",
    "ML-DSA": "safe",
    "SLH-DSA": "safe",
}

def classify_quantum_risk(algorithm: str) -> str:
    for key, risk in QUANTUM_VULNERABILITY.items():
        if key in algorithm.upper():
            return risk
    return "medium"