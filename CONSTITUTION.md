# Deterministic Consent System — Internal Constitution

## Purpose
Determine whether authority exists to use data for a declared purpose, before the data is used.

Nothing else.

---

## Prime Directive
No action is allowed unless it is explicitly permitted.  
Silence equals denial.

---

## System Nature
- Deterministic
- Pre-use
- Explainable
- Auditable
- Fail-closed

---

## Core Flow
1. Intent declared
2. Consent state resolved
3. Escalation evaluated
4. Consent cost computed
5. Decision applied
6. Audit record written

Failure at any step results in DENY or ESCALATE.

---

## Decision Outputs
- ALLOW
- ALLOW_WITH_CONTROLS
- ESCALATE
- DENY
- DELETE

No implied permission.

---

## Non-Negotiables
- No runtime configurability
- No override paths
- No silent allowance
- No post-hoc justification
- No outcome guarantees
- No shared rule authority
- No urgency exceptions

Rules change only by version.

---

## Failure Rules
- Missing input → DENY
- Unknown state → ESCALATE
- Audit failure → DENY
- Engine error → DENY

---

## Audit Principle
Every decision must be reproducible without re-running the system.  
Audit records are immutable.

---

## Responsibility Model
The system determines authority.  
Enforcement belongs to the caller.  
Ignoring decisions equals non-compliance by design.

---

## Exit Rule
If forced to choose between:
- staying involved and compromising authority
- or exiting with authority intact

Exit.
