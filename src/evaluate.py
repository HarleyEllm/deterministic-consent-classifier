from datetime import datetime
from hashlib import sha256
import json

# ---- Fixed vocabularies (v1) ----

CONSENT_STATES = {
    "EXPLICIT",
    "IMPLIED",
    "CONTRACTUAL",
    "ANONYMIZED",
    "UNKNOWN",
    "PROHIBITED",
}

INTENDED_USES = {
    "CORE_SERVICE",
    "ANALYTICS",
    "MARKETING",
    "MODEL_TRAINING",
}

DECISIONS = {
    "ALLOW",
    "ALLOW_WITH_CONTROLS",
    "ESCALATE",
    "DENY",
    "DELETE",
}


# ---- Deterministic evaluator ----

def evaluate(input_data: dict) -> dict:
    """
    Deterministic consent evaluation.
    Missing or unknown input always fails closed.
    """

    # ---- 1. Schema validation (fail closed) ----
    required_fields = [
        "consent_state",
        "intended_use",
        "sensitivity_level",
        "transfer",
        "aggregation",
        "timestamp",
    ]

    for field in required_fields:
        if field not in input_data:
            return _deny("missing_field", field)

    consent_state = input_data["consent_state"]
    intended_use = input_data["intended_use"]

    if consent_state not in CONSENT_STATES:
        return _escalate("unknown_consent_state")

    if intended_use not in INTENDED_USES:
        return _deny("unknown_intended_use")

    # ---- 2. Immediate prohibitions ----
    if consent_state == "PROHIBITED":
        return _deny("prohibited_consent")

    if consent_state == "UNKNOWN":
        return _escalate("unknown_consent")

    # ---- 3. Escalation triggers ----
    escalation_triggers = []

    if input_data["transfer"] is True:
        escalation_triggers.append("transfer")

    if input_data["aggregation"] is True:
        escalation_triggers.append("aggregation")

    if intended_use == "MODEL_TRAINING":
        escalation_triggers.append("model_training")

    if escalation_triggers:
        return _escalate("escalation_triggered", escalation_triggers)

    # ---- 4. Simple consent cost (symbolic, deterministic) ----
    base_cost = {
        "EXPLICIT": 1,
        "CONTRACTUAL": 2,
        "IMPLIED": 3,
        "ANONYMIZED": 2,
    }.get(consent_state, 5)

    sensitivity_multiplier = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 4,
    }.get(input_data["sensitivity_level"], 5)

    consent_cost = base_cost * sensitivity_multiplier

    # ---- 5. Decision matrix (minimal v1) ----
    if consent_cost <= 2:
        decision = "ALLOW"
    elif consent_cost <= 4:
        decision = "ALLOW_WITH_CONTROLS"
    else:
        decision = "ESCALATE"

    # ---- 6. Audit record ----
    record = {
        "decision": decision,
        "consent_cost": consent_cost,
        "timestamp": input_data["timestamp"],
    }

    record_hash = sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()
    record["audit_hash"] = record_hash

    return record


# ---- Internal helpers (not configurable) ----

def _deny(reason: str, detail=None) -> dict:
    return {
        "decision": "DENY",
        "reason": reason,
        "detail": detail,
        "audit_hash": _hash(reason, detail),
    }


def _escalate(reason: str, detail=None) -> dict:
    return {
        "decision": "ESCALATE",
        "reason": reason,
        "detail": detail,
        "audit_hash": _hash(reason, detail),
    }


def _hash(reason, detail) -> str:
    payload = {
        "reason": reason,
        "detail": detail,
        "ts": datetime.utcnow().isoformat(),
    }
    return sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
