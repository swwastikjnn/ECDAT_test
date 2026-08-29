RECOMMENDATIONS = {
    "RSA": "Replace with ML-KEM (FIPS 203) for key exchange; ML-DSA (FIPS 204) for signatures",
    "ECC": "Replace with ML-KEM (FIPS 203) for key exchange; ML-DSA (FIPS 204) for signatures",
    "ECDSA": "Replace with ML-DSA (FIPS 204)",
    "ECDH": "Replace with ML-KEM (FIPS 203)",
    "Ed25519": "Replace with ML-DSA (FIPS 204)",
    "DSA": "Replace with ML-DSA (FIPS 204)",
    "DH": "Replace with ML-KEM (FIPS 203)",
    "MD5": "Replace with SHA-256 or SHA-3",
    "SHA-1": "Replace with SHA-256 or SHA-3",
    "SHA1": "Replace with SHA-256 or SHA-3",
    "DES": "Replace with AES-256",
    "3DES": "Replace with AES-256",
    "RC4": "Replace with AES-256",
    "AES-128": "Upgrade to AES-256",
    "SHA-256": "Consider SHA-384 or SHA-3 for long-term margin",
    "SHA256": "Consider SHA-384 or SHA-3 for long-term margin",
    "TLSv1": "Upgrade to TLS 1.2 or 1.3",
    "SSLv3": "Upgrade to TLS 1.2 or 1.3",
}

def get_recommendation(algorithm: str) -> str:
    for key, rec in RECOMMENDATIONS.items():
        if key in algorithm.upper():
            return rec
    return "No specific recommendation available"