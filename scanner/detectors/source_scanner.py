import os
import re
from typing import List, Dict, Any
from scanner.detectors.rules import SOURCE_DETECTION_RULES, LANGUAGE_EXTENSIONS, EXCLUDE_DIRS

def scan_source_files(target_path: str) -> List[Dict[str, Any]]:
    findings = []
    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext not in LANGUAGE_EXTENSIONS:
                continue
            language = LANGUAGE_EXTENSIONS[ext]
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                findings.extend(scan_file_content(file_path, content, language))
            except Exception:
                continue
    return findings

def scan_file_content(file_path: str, content: str, language: str) -> List[Dict[str, Any]]:
    findings = []
    rules = SOURCE_DETECTION_RULES.get(language, [])
    lines = content.split("\n")
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if language == "python":
            if stripped.startswith("#"):
                continue
        elif language in ("java", "c", "cpp", "javascript", "typescript"):
            if stripped.startswith(("//", "/*", "*")):
                continue
        for rule in rules:
            if re.search(rule["pattern"], line):
                findings.append({
                    "algorithm": rule["algorithm"],
                    "file_path": file_path,
                    "line_number": line_num,
                    "language": language,
                    "asset_type": "algorithm",
                    "quantum_risk": rule["risk"],
                    "mosca_urgent": False,
                    "risk_score": 0,
                    "recommendation": "",
                    "business_criticality": "medium"
                })
    return findings