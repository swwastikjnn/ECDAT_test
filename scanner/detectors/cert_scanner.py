import os
from typing import List, Dict, Any
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from scanner.detectors.rules import CERT_EXTENSIONS, EXCLUDE_DIRS

try:
    import jks
    HAS_JKS = True
except ImportError:
    HAS_JKS = False

def scan_cert_files(target_path: str) -> List[Dict[str, Any]]:
    findings = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in CERT_EXTENSIONS:
                continue
            file_path = os.path.join(root, file)
            try:
                if ext in {".pem", ".crt", ".cer"}:
                    findings.extend(parse_pem_cert(file_path))
                elif ext == ".der":
                    findings.extend(parse_der_cert(file_path))
                elif ext in {".p12", ".pfx"}:
                    findings.extend(parse_pkcs12(file_path))
                elif ext == ".jks" and HAS_JKS:
                    findings.extend(parse_jks(file_path))
            except Exception:
                continue
    return findings

def parse_pem_cert(file_path: str) -> List[Dict[str, Any]]:
    findings = []
    with open(file_path, "rb") as f:
        data = f.read()
    try:
        cert = x509.load_pem_x509_certificate(data)
        findings.append(extract_cert_info(file_path, cert))
    except Exception:
        pass
    return findings

def parse_der_cert(file_path: str) -> List[Dict[str, Any]]:
    findings = []
    with open(file_path, "rb") as f:
        data = f.read()
    try:
        cert = x509.load_der_x509_certificate(data)
        findings.append(extract_cert_info(file_path, cert))
    except Exception:
        pass
    return findings

def parse_pkcs12(file_path: str) -> List[Dict[str, Any]]:
    findings = []
    with open(file_path, "rb") as f:
        data = f.read()
    try:
        private_key, cert, additional_certs = pkcs12.load_key_and_certificates(data, password=None)
        if cert:
            findings.append(extract_cert_info(file_path, cert))
        for c in additional_certs or []:
            findings.append(extract_cert_info(file_path, c))
    except Exception:
        pass
    return findings

def parse_jks(file_path: str) -> List[Dict[str, Any]]:
    findings = []
    if not HAS_JKS:
        return findings
    try:
        with open(file_path, "rb") as f:
            keystore = jks.KeyStore.load(f, password=None)
        for alias, entry in keystore.trusted_certs.items():
            cert = entry.cert
            findings.append(extract_cert_info(file_path, cert, alias))
        for alias, entry in keystore.private_keys.items():
            cert = entry.cert_chain[0] if entry.cert_chain else None
            if cert:
                findings.append(extract_cert_info(file_path, cert, alias))
    except Exception:
        pass
    return findings

def extract_cert_info(file_path: str, cert: x509.Certificate, alias: str = "") -> Dict[str, Any]:
    pub_key = cert.public_key()
    key_size = pub_key.key_size if hasattr(pub_key, "key_size") else 0
    algo_name = cert.signature_hash_algorithm.name if cert.signature_hash_algorithm else "unknown"
    
    from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ec
    if isinstance(pub_key, rsa.RSAPublicKey):
        algorithm = f"RSA-{key_size}"
    elif isinstance(pub_key, ec.EllipticCurvePublicKey):
        algorithm = f"ECDSA-{key_size}"
    elif isinstance(pub_key, dsa.DSAPublicKey):
        algorithm = f"DSA-{key_size}"
    else:
        algorithm = f"Unknown-{key_size}"
    
    return {
        "algorithm": algorithm,
        "file_path": file_path,
        "line_number": 0,
        "language": "certificate",
        "asset_type": "certificate",
        "quantum_risk": "critical" if "RSA" in algorithm or "ECDSA" in algorithm or "DSA" in algorithm else "medium",
        "mosca_urgent": False,
        "risk_score": 0,
        "recommendation": "",
        "business_criticality": "medium",
        "key_size": key_size,
        "signature_algorithm": algo_name,
        "not_valid_after": cert.not_valid_after_utc.isoformat() if cert.not_valid_after_utc else None,
        "alias": alias
    }