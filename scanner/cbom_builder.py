from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.model import Property
from cyclonedx.output.json import JsonV1Dot6
from typing import List, Dict, Any
import json

def build_cbom(assets: List[Dict[str, Any]], project_name: str = "ECDAT Scan") -> Dict[str, Any]:
    bom = Bom()
    bom.metadata.component = Component(name=project_name, type=ComponentType.APPLICATION)
    
    for asset in assets:
        comp = Component(
            name=asset.get("algorithm", "Unknown"),
            type=ComponentType.CRYPTOGRAPHIC_ASSET,
            bom_ref=asset.get("file_path", "") + str(asset.get("line_number", 0))
        )
        
        props = []
        props.append(Property(name="assetType", value=asset.get("asset_type", "algorithm")))
        props.append(Property(name="quantumRisk", value=asset.get("quantum_risk", "medium")))
        props.append(Property(name="moscaUrgent", value=str(asset.get("mosca_urgent", False)).lower()))
        props.append(Property(name="riskScore", value=str(asset.get("risk_score", 0))))
        props.append(Property(name="recommendation", value=asset.get("recommendation", "")))
        props.append(Property(name="businessCriticality", value=asset.get("business_criticality", "medium")))
        props.append(Property(name="filePath", value=asset.get("file_path", "")))
        props.append(Property(name="lineNumber", value=str(asset.get("line_number", 0))))
        props.append(Property(name="language", value=asset.get("language", "")))
        
        comp.properties = props
        bom.components.add(comp)
    
    outputter = JsonV1Dot6(bom)
    return json.loads(outputter.output_as_string())