from __future__ import annotations

from dataclasses import dataclass
import re


CONFIDENTIAL_PATTERNS = [
    r"\bsecret\b",
    r"\bconfidential\b",
    r"\bprivate\b",
    r"\bpassword\b",
    r"\btoken\b",
    r"\bapi key\b",
    r"\bssh key\b",
    r"\bcredential\b",
    r"\bsecrets\.env\b",
    r"\bpatient\b",
    r"\bmedical\b",
    r"\bpayroll\b",
    r"\bsalary\b",
    r"\bcontract\b",
    r"\bclient data\b",
    r"\bproprietary\b",
    r"\binternal only\b",
]

HIGH_COMPLEXITY_PATTERNS = [
    r"\barchitecture\b",
    r"\brefactor\b",
    r"\bmigration\b",
    r"\bsecurity\b",
    r"\bdebug\b",
    r"\borchestrator\b",
    r"\bconsensus\b",
    r"\bvalidator\b",
    r"\bwireguard\b",
    r"\bopenclaw\b",
]

LOW_COMPLEXITY_PATTERNS = [
    r"\bsummarise\b",
    r"\brewrite\b",
    r"\btidy\b",
    r"\bformat\b",
    r"\brename\b",
    r"\bdraft\b",
]


@dataclass(frozen=True)
class TaskClassification:
    complexity: str
    confidentiality: str
    risk: str
    reasons: list[str]


def _matches_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text, flags=re.IGNORECASE) for p in patterns)


def classify_task(task_text: str, risk_hint: str | None = None) -> TaskClassification:
    reasons: list[str] = []
    text = task_text.strip()

    confidentiality = "normal"
    if _matches_any(text, CONFIDENTIAL_PATTERNS):
        confidentiality = "confidential"
        reasons.append("confidentiality_detected_from_content")

    complexity = "medium"
    if _matches_any(text, HIGH_COMPLEXITY_PATTERNS):
        complexity = "high"
        reasons.append("high_complexity_keywords_detected")
    elif _matches_any(text, LOW_COMPLEXITY_PATTERNS):
        complexity = "low"
        reasons.append("low_complexity_keywords_detected")

    risk = "normal"
    if risk_hint:
        lowered = risk_hint.strip().lower()
        if lowered in {"low", "normal", "high"}:
            risk = lowered
            reasons.append("risk_hint_applied")

    if confidentiality == "confidential":
        risk = "high"
        reasons.append("confidentiality_elevated_risk")

    if complexity == "high" and risk == "normal":
        risk = "high"
        reasons.append("complexity_elevated_risk")

    return TaskClassification(
        complexity=complexity,
        confidentiality=confidentiality,
        risk=risk,
        reasons=reasons,
    )
