According to a document from **2026-01-10**, the “Reachy Mini Second Brain” concept is built around **atomic interactions**, **automated classification**, and **structured/finite storage** (so you get reliability + later analytics), but it flags real risks around **real-time UX**, **context handling**, **cost**, and **multi-user/session/idempotency**.

Here are **metrics for success** and a practical **evaluation plan** that match that architecture.

## 1) Success metrics (what “good” looks like)

### A) Capture & classification quality (the “second brain works” metrics)

1. **Capture rate**: % of “valuable” customer/staff utterances that get captured as an atomic thought.
2. **Classifier accuracy** (overall + by label): precision/recall for:

   * storage bucket (People / Projects / Ideas / Admin / Auto-log inbox)
   * intent type (deal question vs product location vs general help)
   * any required tags (SKU/category, aisle, urgency, sentiment)
3. **Routing correctness**: % of captures that end up in the right database *without human correction*.
4. **Human review load**: median “seconds to correct” per item + % items needing correction (goal: low enough to scale).

### B) Retail impact (the “it actually helps the store” metrics)

5. **Item-find success rate**: % of “where do I find X?” sessions where the customer reaches the right location (validated by follow-up prompt or staff observation).
6. **Time-to-item**: median time from question → clear location instruction (and optionally: arrival confirmation).
7. **Promo conversion assist**: uplift in promo engagement among exposed users:

   * “add to cart / go-to-aisle / scan QR / ask staff”
8. **Deflection rate**: % of interactions resolved without human associate intervention (and “safe deflection”: not causing frustration).

### C) Experience & trust (the “customers like it” metrics)

9. **CSAT after interaction** (1-tap): overall + by flow (promo hype vs item location).
10. **Conversation breakdown rate**: % sessions ending in “I don’t understand / wrong aisle / repeated loop.”
11. **Selfie opt-in rate** (since you want this): % users who accept selfie prompt, plus **selfie completion rate** (accepted → completed).
12. **Brand safety**: # of policy/brand violations per 1,000 interactions (should be near zero).

### D) Reliability, speed, and cost (the “ops sanity” metrics)

13. **P95 latency**: user-perceived response time (speech-to-response). Track separately for:

* “fast path” (lookup + location)
* “slow path” (LLM classify + write)

14. **Uptime / crash-free sessions**: % sessions without app/robot faults.
15. **Cost per interaction**: total inference + tooling cost per captured thought and per resolved session.
16. **Multi-user robustness**: collision rate (two people interacting) causing incorrect state (should be ~0).

---

## 2) How we’ll evaluate (tight loop you can run this month)

### Phase 0: Offline validation (1–2 days)

1. Build a **gold dataset**: 200–500 labeled “atomic thoughts” from realistic store interactions (deals, location, questions, staff notes).
2. Run the classifier against it and measure **precision/recall**, plus “correction time” in a lightweight review UI.

**Exit criteria:** routing correctness + accuracy are “good enough” to not drown reviewers.

### Phase 1: Shadow mode in-store (2–4 days)

* Run the capture + classify + store pipeline, **but don’t show decisions to customers**.
* Staff reviews daily; you track:

  * capture rate
  * misroutes
  * cost per thought
  * top failure patterns (e.g., ambiguous product names)

**Exit criteria:** stable cost + manageable human review + clear taxonomy gaps identified.

### Phase 2: Limited live pilot (1–2 weeks)

* Turn on 2 narrow live flows:

  1. **Promo & Deal Hype** (with guardrails)
  2. **“Where do I find it?”** location answers
* A/B compare:

  * with/without “selfie offer”
  * with/without “confirm you found it?” follow-up

**Exit criteria:** improved item-find success + acceptable CSAT + no brand safety incidents.

### Phase 3: Post-pilot scorecard + go/no-go

* Produce a one-page scorecard with the metric groups above + top 10 failure modes + fixes.

---

## 3) A simple “Launch Score” to keep everyone aligned

If you want one composite KPI for the month:

**Launch Score = (0.35 * Task Success) + (0.25 * CSAT) + (0.20 * Correct Routing) + (0.10 * P95 Latency Target Hit) + (0.10 * Cost Target Hit)**

Where “Task Success” is mainly **item-find success** + **promo conversion assist**.

---

If you want, I’ll turn the above into a **PRD-ready “Success Metrics & Measurement Plan” section** tailored specifically to **Promo & Deal Hype Bot + Item Location + optional Selfie prompt**.
