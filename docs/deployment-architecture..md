# 🤖 Reachy Mini Deployment Architecture

## Wired, Wireless (CM4), and External Compute (Pi 5 + Hailo)

---

## 1. Design Principle (Lock This In)

> **Reachy Mini never “owns” the brain.
> Compute location is a deployment detail, not an architectural one.**

The same **application + orchestration model** must run regardless of:

* wired vs wireless
* host OS
* onboard vs external compute

Only **where processes run** changes.

---

## 2. Canonical Runtime Components (Always the Same)

There are **three runtime roles**, regardless of hardware:

### A. Reachy Runtime (Robot Interface)

* audio in/out
* gestures
* camera
* FSM conversation loop
* tool execution
* emits events

### B. Fast Lane LLM Runtime

* onboard or near-edge
* low-latency
* cache-only
* one-clarification rule

### C. π Client (Second Brain Connector)

* event sender
* cache sync
* heartbeat / idle detection
* debug telemetry

These are **logical roles**, not tied to a specific machine.

---

## 3. Deployment Profiles (What Runs Where)

### Profile 1: Wired Reachy Mini (Host PC Attached)

**Best default for development and early pilots**

**Where things run**

* Host PC (Windows / macOS / Linux):

  * Reachy Runtime
  * Fast Lane LLM
  * π Client
* Reachy Mini:

  * hardware only

**Why this is good**

* fastest iteration
* easiest debugging
* no ARM constraints
* easiest LLM experimentation

**Recommended use**

* development
* demos
* first store pilots

---

### Profile 2: Wireless Reachy Mini (CM4 Only)

**Best for clean floor deployments**

**Where things run**

* Reachy CM4:

  * Reachy Runtime
  * π Client
  * optional Fast Lane LLM (small model only)
* π:

  * remote

**Constraints**

* strict latency budgets
* small context windows
* aggressive caching

**Recommended use**

* simple promo + wayfinding
* offline-tolerant operation
* minimal fast-lane LLM usage

---

### Profile 3: Wireless Reachy + External Pi 5 (Preferred “Production Edge”) ⭐

**This is the sweet spot**

**Where things run**

* Reachy CM4:

  * hardware interface
  * minimal orchestration
* Raspberry Pi 5:

  * Reachy Runtime
  * Fast Lane LLM
  * π Client
  * local cache (L2)
* π:

  * deep intelligence

**Why this is ideal**

* keeps Reachy lightweight
* strong ARM performance
* easy updates
* isolates failures
* future-proofs compute

---

## 4. Where the Hailo Pi 5 Fits (Important)

The **Hailo 26 TOPS Pi 5** should **NOT** run general LLMs.

It should be reserved for:

* vision inference
* perception tasks
* fast classifiers
* detection pipelines

### Correct usage

* human presence detection (idle vs active)
* gesture/person detection
* shelf/product vision (future)
* camera-based triggers

### Incorrect usage

* text generation
* conversation logic
* long-context reasoning

This keeps:

* latency predictable
* thermal load stable
* system debuggable

---

## 5. Unified Orchestration (Same Everywhere)

Regardless of profile:

```
Reachy Hardware
   ↓
Reachy Runtime (FSM + tools)
   ↓
Fast Lane LLM (local if possible)
   ↓
Speech / Gesture
   ↓
Async Events → π
```

Only the **machine boundaries** change.

---

## 6. Cache & Sync Behavior (Consistent)

* L1: in-memory (where runtime lives)
* L2: local disk (host PC or Pi 5)
* L3: π only

Idle sync works the same whether:

* wired
* wireless
* edge-assisted

---

## 7. Debug Mode (Critical for All Profiles)

Debug mode must work identically:

* logs cache hits
* logs LLM path (onboard vs edge vs remote)
* logs latency per component
* logs prompt + model version hashes

This is how you avoid:

* “it works on my robot”
* environment-specific bugs

---

## 8. Recommended Default (If You Ask Me)

**Default production recommendation:**

> **Wireless Reachy Mini + Raspberry Pi 5 (edge brain) + π (cloud brain)**

Use:

* Pi 5 for fast lane LLM + cache
* Hailo for vision & presence
* π for intelligence, memory, eval

This gives you:

* speed
* reliability
* observability
* upgrade flexibility

---

## 9. What This Enables Later (Without Redesign)

* swap onboard vs edge LLMs
* add vision features incrementally
* add more Reachys per store
* move between wired/wireless freely
* ship updates without reflashing robots

---

## 10. Key Takeaway

> **Reachy Mini is a body.
> The Pi 5 is a reflex brain.
> π is the mind.**

Once you lock that mental model, the rest stays clean.

---

