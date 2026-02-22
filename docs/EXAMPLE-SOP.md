# 🤖 Reachy Mini Onboarding SOP

**Standard Operating Procedure (v1)**
*For First Deployment, Additional Robots, and Multi-Store Rollouts*

---

## 1. Purpose

This SOP defines the **standard process** for onboarding Reachy Mini robots into the **Second Brain** system, ensuring:

* Fast, correct initial behavior
* Consistent intelligence across robots
* Zero on-robot configuration drift
* Full observability and auditability

This SOP applies to:

* First-ever Reachy Mini deployment
* Adding additional Reachy Minis to an existing store
* Rolling out Reachy Minis to new stores

---

## 2. Roles & Responsibilities

### Required Roles

* **Provisioning Operator**
  Performs onboarding steps in Admin UI / CLI

* **Store Representative (Optional)**
  Confirms store map, promos, and placement

* **Robotics Operator (Optional)**
  Handles physical setup and connectivity

---

## 3. Definitions

* **Reachy Mini**: The physical robot
* **Second Brain**: Central intelligence, memory, and orchestration system
* **Provisioning Mode**: Safe startup state before activation
* **L2 Cache**: Store-level cached knowledge pushed to Reachy
* **Zone**: Physical placement area (entrance, electronics, aisle hub)

---

## 4. Preconditions (Before Power-On)

Before onboarding begins, confirm:

* Reachy Mini is powered and network-capable
* Second Brain system is accessible
* Operator has provisioning permissions
* Store information is available:

  * store name / ID
  * rough store layout (can be coarse)
  * promo feed or confirmation that none exist

---

## 5. Onboarding Scenario A

## First-Ever Reachy Mini (Greenfield Deployment)

### Step A1 — Power On & Provisioning Mode

1. Power on Reachy Mini
2. Reachy automatically enters **PROVISIONING MODE**
3. Reachy displays:

   * pairing QR code **or**
   * provisioning code

Reachy behavior in this mode:

* No conversation
* No gestures
* No LLM calls
* No cache loaded

---

### Step A2 — Create Store in Second Brain

In Admin UI / CLI:

1. Create a new `store_id`
2. Select or assign a **store template**

   * (e.g., “General Retail”, “Electronics”, “Demo Space”)
3. Upload or define:

   * basic store map (can be high-level)
   * default language
   * idle behavior preferences

---

### Step A3 — Assign Reachy to Store

Using the pairing code:

```json
{
  "reachy_id": "auto-detected",
  "store_id": "STORE-001",
  "zone_id": "ENTRANCE",
  "role": "GENERALIST"
}
```

Defaults:

* `role = GENERALIST`
* `zone_id = ENTRANCE` (if unspecified)

---

### Step A4 — Initial Brain Provisioning

The system performs:

* Validation of store config
* Generation of **baseline L2 cache**
* Signing of cache payload

The system pushes to Reachy:

* L2 cache (default knowledge)
* L1 hot-start subset
* Cache version metadata

---

### Step A5 — Activation & Verification

Reachy:

1. Verifies payload signature
2. Loads cache atomically
3. Transitions to `IDLE` mode
4. Emits “activation successful” event

✅ Reachy is now live with a **safe default brain**

---

## 6. Onboarding Scenario B

## Additional Reachy Mini (Same Store)

### Step B1 — Power On

New Reachy enters **PROVISIONING MODE** automatically.

---

### Step B2 — Assign to Existing Store

In Admin UI:

```json
{
  "reachy_id": "RCH-002",
  "store_id": "STORE-001",
  "zone_id": "ELECTRONICS",
  "role": "GENERALIST"
}
```

---

### Step B3 — Inherit Store Brain

The system automatically:

* Assigns same L2 cache as existing Reachys
* Applies optional zone overlays (if defined)

No additional configuration required.

---

### Step B4 — Activate

Reachy loads cache and becomes active.

📌 Result:
**One store brain, many Reachy bodies**

---

## 7. Onboarding Scenario C

## New Store Rollout

### Step C1 — Create Store from Template

1. Clone existing store template
2. Assign new `store_id`
3. Inject:

   * store map
   * promo feed
   * price book (if available)

---

### Step C2 — Provision Reachys

Repeat Scenario A or B for each Reachy Mini.

---

## 8. Default Behavior (If Minimal Setup)

If no promos or detailed data are provided:

Reachy defaults to:

* Greeting customers
* Generic wayfinding assistance
* Safe fallback responses
* Staff handoff offers
* Onboard LLM enabled (cache-only mode)

This ensures **useful but conservative behavior**.

---

## 9. Idle Sync & Ongoing Updates

After onboarding:

* Reachy checks in with the Second Brain when idle
* The system pushes:

  * promo updates
  * cache improvements
  * corrections
* All updates are:

  * versioned
  * atomic
  * reversible

No re-provisioning required.

---

## 10. Re-Provisioning & Recovery SOP

### Moving Reachy to a New Store

1. The system revokes old store binding
2. Reachy wipes local cache
3. Reachy re-enters PROVISIONING MODE
4. Repeat onboarding steps

---

### Cache Corruption or Failure

* Reachy enters **SAFE MODE**
* Conversation disabled
* Cache refresh requested from the backend
* Incident logged automatically

---

### Network Outage

* Reachy continues using last valid cache
* Flags “offline” in telemetry
* Syncs on reconnect

---

## 11. Observability & Audit Requirements

Every onboarding action logs:

* operator identity
* timestamp
* store_id
* reachy_id
* cache version
* success/failure

This supports:

* audits
* debugging
* rollback
* fleet analytics

---

## 12. Acceptance Checklist (Go / No-Go)

Before declaring onboarding complete:

* [ ] Reachy speaks and responds correctly
* [ ] Wayfinding answers match store map
* [ ] Cache version visible in logs
* [ ] Idle sync heartbeat observed
* [ ] No errors in activation trace

---

## 13. SOP Versioning

* SOP Version: v1
* Changes require:

  * product approval
  * ops approval
  * update to provisioning logic

---

## 14. Key Principle (Final Reminder)

> **Reachy Minis are replaceable endpoints.
> The Second Brain is the intelligence.**

Onboarding must always preserve this invariant.

---
