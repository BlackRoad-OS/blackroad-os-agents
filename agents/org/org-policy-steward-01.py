"""Policy Steward agent stub."""
from typing import Any, Dict, List


def review_change(change_doc: Dict[str, Any]) -> Dict[str, Any]:
    """Return a lightweight policy review summary."""
    return {
        "change_summary": change_doc.get("summary", "No summary provided"),
        "requires_signoff": True,
        "notes": change_doc.get("notes", []),
    }


def flag_risks(change_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify risks for the change document stub."""
    risks = []
    if change_doc.get("data_classification") == "sensitive":
        risks.append({"type": "data", "severity": "high"})
    if change_doc.get("contractual"):
        risks.append({"type": "contract", "severity": "medium"})
    return risks
