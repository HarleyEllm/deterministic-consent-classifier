
# Deterministic Data Consent Classifier

## What this is

This project implements a deterministic system for evaluating data consent **before data is used**.

It accepts a declared intent to use data and returns a clear, auditable decision:

- ALLOW
- ALLOW_WITH_CONTROLS
- ESCALATE
- DENY
- DELETE

The system is not advisory.  
It produces decisions, not suggestions.

---

## Why this exists

Most organisations cannot reliably answer the question:

> “Are we actually allowed to use this data for this purpose, right now?”

Consent is often:
- collected once and reused indefinitely
- inferred without evidence
- justified after the fact
- overridden informally

This system exists to remove assumption and replace it with **explicit authority**.

---

## Core principle

**No action is allowed unless it is explicitly permitted.**  
**Silence = denial.**

---

## What the system does

For each declared data use, the system:

1. Resolves the current consent state
2. Evaluates escalation conditions
3. Computes a consent cost
4. Applies a decision matrix
5. Writes an immutable audit record

All decisions occur **before** data is accessed or processed.

---

## What this system is not

This project is intentionally limited.

It is not:
- a consent collection tool
- a policy generator
- a dashboard
- a risk prediction model
- a configurable rules engine

It does not decide what *should* be allowed.  
It determines whether **authority exists**.

---

## Deterministic by design

- Same inputs → same outputs
- No machine learning
- No heuristics
- No probabilistic scoring

All logic is explicit and versioned.

---

## Failure behavior

This system fails closed.

- Missing input → DENY
- Unknown state → ESCALATE
- Audit failure → DENY
- Engine error → DENY

---

## Status

This repository is a reference implementation.  
The boundary is defined before the code.
