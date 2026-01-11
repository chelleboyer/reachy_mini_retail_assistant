# 📄 Product Requirements Document (PRD)

## π (Pi) Universal Second Brain - Intelligent Classification System

**Vision:** A domain-agnostic intelligence layer for any AI assistant  
**Initial Implementation:** Reachy Mini Retail Assistant

---

## 1. Product Overview

### Product Name

**π (Pi) Universal Second Brain**  
*Intelligent classification and memory system for AI assistants across any domain*

**First Use Case:** Reachy Mini Retail Assistant

### Vision Statement

π transforms unstructured interactions into structured, searchable knowledge using multi-stage classification. Think **Logseq meets RAG meets Zapier** - automatic classification, canonical storage, cross-domain reasoning. 

**Not just a retail assistant. Not just a chatbot. A universal intelligence layer.**

### One-Line Description

A domain-agnostic classification engine that transforms any interaction into structured knowledge, enabling contextual AI assistants across retail, personal productivity, business automation, research, and more.

---

## 2. Problem Statement

### Universal Challenge

AI assistants across domains (retail, personal, business, research) face common challenges:

* **Lack of memory**: Each interaction is isolated, no learning
* **Unstructured knowledge**: Information stored as chat logs, not searchable facts
* **No reasoning transparency**: Can't explain why they said something
* **Domain-locked**: Built for one use case, can't generalize
* **Slow or expensive**: Either fast but dumb, or smart but costly

### Retail-Specific Challenges (Initial Use Case)

* Customers miss promotions unless staff intervene
* Staff interrupted for basic wayfinding questions
* Digital signage lacks interactivity
* Robotic assistants feel slow, scripted, or untrustworthy

---

## 3. Product Goals

### Primary Goals (Universal)

1. **Classify any interaction** into structured, searchable knowledge
2. **Build canonical memory** that persists across sessions
3. **Enable contextual reasoning** using past interactions
4. **Maintain transparency** - always explainable classifications
5. **Support any domain** through pluggable configurations
6. **Continuous learning** without model retraining

### Retail Implementation Goals (Initial Use Case)

1. Provide **fast, natural, voice-based retail assistance**
2. Promote **active deals and campaigns**
3. Guide customers **physically to products**
4. Reduce staff interruptions
5. Increase customer engagement and dwell time

---

## 4. Non-Goals (Explicit)

* Checkout or payment
* Customer identity or personalization
* Facial recognition
* Autonomous learning on-robot
* Revenue attribution in MVP

---

## 5. Target Users & Domains

### Universal Platform Users

* **Developers** building AI assistants for any domain
* **Businesses** deploying domain-specific automation
* **Power users** wanting structured personal knowledge
* **Researchers** organizing information and insights
* **Operations teams** managing workflows and knowledge bases

### Initial Implementation: Retail

* Store customers seeking products and deals
* Store managers tracking engagement
* Demo teams showcasing AI capabilities
* Robotics operators monitoring system health

---

## 6. Core Concept: Universal Two-Brain Architecture

### Edge Layer (Domain-Specific Interfaces)

Different interfaces for different contexts:

| Domain | Interface | Edge Device |
|--------|-----------|-------------|
| **Retail** | Reachy Mini Robot | Pi 5 |
| **Personal** | Mobile/Desktop App | Phone/Laptop |
| **Business** | Slack/Teams Bot | Cloud Server |
| **Research** | Note-taking Plugin | Local Machine |
| **Home** | Voice Assistant | Smart Speaker |

**Edge Characteristics:**
* Fast conversational interface
* Local cache (L1/L2) for instant responses
* Domain-specific tools and actions
* Optional fast LLM calls for nuance
* Zero long-term memory writes
* Specialized UI/UX per domain

### π (Universal Second Brain)

**The domain-agnostic intelligence layer that powers all edges**

**Core Components:**

1. **Multi-Stage Classifier**
   * Stage 1: Domain Detection (retail, personal, business, etc.)
   * Stage 2: Intent Classification (lookup, create, update, etc.)
   * Stage 3: Entity Extraction (products, people, dates, etc.)
   * Stage 4: Canonical Type Mapping (entity, event, knowledge, etc.)
   * Stage 5: Response Generation & Action Planning

2. **Universal Canonical Storage**
   ```yaml
   entities: [person, place, product, concept, organization, device]
   events: [action, interaction, observation, transaction]
   knowledge: [fact, rule, relationship, definition]
   tasks: [todo, reminder, goal, request]
   content: [document, media, message, note]
   ```

3. **Context & Reasoning Engine**
   * Session tracking across conversations
   * Entity resolution (same person/product across mentions)
   * Cross-domain inference (link retail to calendar)
   * Knowledge graph traversal

4. **Domain Plugin System**
   * Pluggable domain configurations
   * Custom intent + entity definitions per domain
   * Shared canonical types across all domains
   * Easy onboarding of new domains

5. **Cache Generation Engine**
   * Push relevant knowledge to edge devices
   * Domain-filtered views of canonical data
   * Incremental sync protocol

6. **Evaluation & Learning**
   * Classification quality metrics
   * Replay interactions for testing
   * A/B test classifiers
   * No model retraining needed

> **Edge interfaces speak their domain language. π thinks universally.**

### Why This Architecture Matters

| Traditional Approach | π Universal Second Brain |
|---------------------|------------------------|
| Build separate AI per domain | One intelligence layer, many interfaces |
| Chat logs with no structure | Canonical knowledge graph |
| Retrain models for changes | Update configuration files |
| Opaque AI decisions | Explainable classifications |
| Siloed knowledge | Cross-domain reasoning |
| Expensive cloud calls | Local cache + smart classification |

---

## 7. Universal User Flows

### Example Flows Across Domains

#### 🛒 Retail: Deal Promotion
```
User: "Hi there!"
π Classification: Domain=retail, Intent=greeting, Context=start_interaction
Edge: "Hey! We've got 20% off organic milk and buy-one-get-one pasta today. Want to check them out?"
π Storage: Event(interaction) + links to Product entities
```

#### 📱 Personal: Create Reminder
```
User: "Remind me to call Sarah tomorrow at 2pm"
π Classification: Domain=personal, Intent=create_reminder
  Entities: Sarah(person), tomorrow 2pm(datetime), call(action)
π Action: Create Task(reminder) + link to Entity(Sarah)
Edge: "Reminder set for tomorrow at 2pm: Call Sarah"
```

#### 💼 Business: Support Ticket
```
User: "Customer John complained shipping was late"
π Classification: Domain=business, Intent=log_support_issue
  Entities: John(customer), shipping(service), late(sentiment:negative)
π Action: Create Event(support_ticket) + Entity(John) + Knowledge(shipping_issue)
Edge: "Logged as ticket #1234. John's 3rd shipping issue this month. Want me to escalate?"
```

#### 🏠 Home: Maintenance Tracking
```
User: "Kitchen light is flickering"
π Classification: Domain=home, Intent=maintenance_issue
  Entities: kitchen(place), light(device), flickering(problem)
π Action: Create Task(maintenance) + Entity(device) + Event(observation)
Edge: "Added to fix list. Last bulb change was 6 months ago. Might need replacement."
```

### Retail-Specific Flows (Initial Implementation)

#### 7.1 Deal Promotion Flow
1. Reachy greets customer
2. Shares 1–3 active promotions from cache
3. Explains value briefly (≤35 words)
4. Offers to show item location

**π Actions:** Log interaction event, track which promos mentioned

#### 7.2 Wayfinding Flow
1. Customer asks for product
2. Reachy answers immediately from L1/L2 cache
3. Points/gestures toward aisle
4. Gives spoken directions

**π Actions:** Log product query, track navigation success

#### 7.3 Clarification Flow
* If ambiguity exists, Reachy may ask **one clarifying question**
* After clarification, Reachy must answer or fallback
* No endless back-and-forth

**π Actions:** Log ambiguous query for classifier improvement

#### 7.4 Selfie Flow (Optional)
1. Reachy offers a selfie
2. If accepted, Reachy poses
3. Countdown and capture via external device
4. No image storage (privacy)

**π Actions:** Log engagement event (no image data)

---

## 8. Functional Requirements

### 8.1 Universal π Requirements

**Classification Engine:**
* Multi-stage classification (Domain → Intent → Entity → Canonical)
* Confidence scoring for each stage
* Explainability for all decisions
* Sub-100ms classification for cached patterns
* Support for ambiguity detection

**Canonical Storage:**
* Universal schema for all domains
* Entity deduplication and resolution
* Knowledge graph with relationships
* Temporal tracking (when things happened)
* Efficient querying and indexing

**Context Engine:**
* Session state management
* Cross-conversation entity tracking
* Inference and prediction
* Cross-domain relationship traversal

**Domain Plugin System:**
* YAML-based domain configurations
* Intent and entity definitions per domain
* Canonical type mappings
* Easy addition of new domains

**Evaluation & Learning:**
* Classification quality metrics
* Replay interactions for testing
* A/B test different classifiers
* Compare results without retraining

### 8.2 Retail Edge Requirements (Initial Implementation)

**Conversation & Interaction:**
* Voice input and output
* Natural language responses
* Gesture coordination (head, arm pointing)
* Single-question clarification support
* ≤35 words per spoken response

**Fast LLM Usage (Allowed):**
* Low-latency LLM calls for nuanced responses
* Strict prompt contracts with π-provided cache
* Bounded context and output
* No memory writes from edge LLM

**Memory System:**
* **L1 Working Memory** (RAM, hot, ≤1MB)
* **L2 Cached Knowledge** (SQLite FTS5, ≤100MB)
* **L3 Canonical Memory** (π only, unlimited)

**External Data Sources:**
* Price book feeds
* Promotion feeds
* Store configuration systems
* All data must flow through π for classification
* Normalized and cached for edge consumption

---

## 9. π (Universal Second Brain) Responsibilities

**Event Ingestion:**
* Receive interaction events from all edge devices (append-only log)
* Support multi-tenant event streams (store isolation, user isolation, etc.)
* Event schema validation and versioning

**Classification Pipeline:**
* Run multi-stage classification on each interaction
* Stage 1: Domain detection
* Stage 2: Intent classification
* Stage 3: Entity extraction
* Stage 4: Canonical type mapping
* Stage 5: Response/action planning

**Canonical Storage:**
* Store entities, events, knowledge, tasks, content
* Build knowledge graph with relationships
* Entity resolution and deduplication
* Temporal tracking (history, audit trail)

**Cache Generation:**
* Generate domain-filtered cache snapshots for edge devices
* Push incremental updates during idle time
* Optimize for edge query patterns (FTS, lookups)

**Domain Management:**
* Load and validate domain plugin configurations
* Support custom intents, entities, tools per domain
* Maintain canonical type mappings

**Evaluation & Learning:**
* Replay historical interactions
* A/B test classifier changes
* Track classification quality metrics
* Support model comparison without retraining

**Feed Ingestion:**
* Ingest external data sources (price feeds, calendars, etc.)
* Normalize and classify external data
* Update canonical storage and edge caches

---

## 10. Edge LLM Prompt Contract (Retail Implementation)

**For fast, nuanced responses on retail edge devices:**

* Uses **only L1/L2 cache** (no external lookups)
* Never invents facts not in cache
* Asks at most **one clarifying question** if ambiguous
* Outputs strict JSON with required fields
* Returns one of: ANSWER, CLARIFY, or FALLBACK
* Spoken responses ≤35 words
* Cache metadata includes: sku, aisle, promo details

(Full prompt contract maintained as a versioned artifact in π)

---

## 11. Orchestration Models

### Universal π Architecture

```
┌──────────────────────────────────────────┐
│  External Data Sources                   │
│  (Feeds, APIs, Files, Calendars, etc.)   │
└──────────┬───────────────────────────────┘
           │
┌──────────▼───────────────────────────────┐
│  π Event Ingestion API                   │
│  - Interaction events from edge devices  │
│  - External data feed processing         │
└──────────┬───────────────────────────────┘
           │
┌──────────▼───────────────────────────────┐
│  π Classification Pipeline               │
│  - Multi-stage classifier                │
│  - Domain plugins                        │
│  - Confidence scoring                    │
└──────────┬───────────────────────────────┘
           │
┌──────────▼───────────────────────────────┐
│  π Canonical Storage                     │
│  - Entities, Events, Knowledge, Tasks    │
│  - Knowledge Graph                       │
│  - Temporal tracking                     │
└──────────┬───────────────────────────────┘
           │
┌──────────▼───────────────────────────────┐
│  π Cache Generation Engine               │
│  - Domain-filtered snapshots             │
│  - Incremental sync                      │
│  - Edge-optimized queries                │
└──────────┬───────────────────────────────┘
           │
    ┌──────┴──────┬──────────┬──────────┐
    │             │          │          │
┌───▼───┐    ┌───▼───┐  ┌──▼────┐  ┌──▼─────┐
│Retail │    │Personal│  │Business│  │Research│
│ Edge  │    │  App   │  │  Bot   │  │  Tool  │
└───────┘    └────────┘  └────────┘  └────────┘
```

### Retail Edge (Reachy Mini) Architecture

```
┌──────────────────────────────────────────┐
│  Reachy Mini (Pi 5)                      │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  FSM Controller                    │ │
│  │  (Idle → Listen → Process → Act)  │ │
│  └────────┬───────────────────────────┘ │
│           │                              │
│  ┌────────▼───────────────────────────┐ │
│  │  L1 Cache (RAM, hot, ≤1MB)        │ │
│  │  - Active promos                  │ │
│  │  - Frequent products              │ │
│  │  - Session context                │ │
│  └────────┬───────────────────────────┘ │
│           │                              │
│  ┌────────▼───────────────────────────┐ │
│  │  L2 Cache (SQLite FTS5, ≤100MB)   │ │
│  │  - All products + locations       │ │
│  │  - All promos                     │ │
│  │  - Store config                   │ │
│  └────────┬───────────────────────────┘ │
│           │                              │
│  ┌────────▼───────────────────────────┐ │
│  │  Fast LLM (Optional)               │ │
│  │  - Cache-only responses           │ │
│  │  - Strict prompt contract         │ │
│  │  - ≤35 word answers               │ │
│  └────────┬───────────────────────────┘ │
│           │                              │
│  ┌────────▼───────────────────────────┐ │
│  │  Tool Router                       │ │
│  │  - Speak (TTS)                    │ │
│  │  - Gesture (point, nod, wave)    │ │
│  │  - Selfie (camera trigger)       │ │
│  └────────┬───────────────────────────┘ │
│           │                              │
│  ┌────────▼───────────────────────────┐ │
│  │  π Client (Event Emitter)         │ │
│  │  - Async event logging            │ │
│  │  - Cache sync requests            │ │
│  │  - Telemetry                      │ │
│  └────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

---

## 12. Observability & Debug Mode

### Required Observability

* One interaction = one trace
* Structured logs
* Latency metrics
* Prompt + model versioning
* Cache hit/miss tracking

### Debug Mode

When enabled:

* Logs cache slices used
* Logs LLM inputs/outputs
* Stores classifier decisions
* Enables replay with new prompts

Debug mode changes **visibility, not behavior**.

---

## 13. Success Metrics

### Reliability

* ≥99% crash-free interactions
* <1% unhandled errors

### Performance

* P95 interaction latency <1s
* Fast path responses <500ms

### Utility

* ≥30% wayfinding engagement
* ≥60% promo recall (spot checks)

### Delight

* 10–20% selfie acceptance
* Observable social engagement

### Retail Validation

* Positive staff feedback
* “Would you keep this on the floor?” ≠ No

---

## 14. Evaluation Strategy

### Universal Platform

**Offline:**
* Multi-domain gold datasets
* Replay with classifier variants
* A/B test strategies

**Synthetic:**
* Generate cross-domain test cases
* Edge case coverage

### Retail Implementation

**Shadow Mode:**
* Capture + classify without customer impact

**Pilot:**
* Limited live deployment (1–2 stores)
* Manual observation + structured logs

**Continuous:**
* Real-time quality dashboards
* Anomaly detection

---

## 15. Technical Constraints

* Must function under variable network conditions
* Must degrade gracefully
* Must support offline cache usage
* Must be auditable

---

## 16. Phased Development Roadmap

### Phase 1: Retail MVP (Current) ✅

**Goal:** Prove the two-brain architecture with one domain

**Included:**
* Retail domain plugin (intents, entities, tools)
* Edge backend for Pi 5 (FastAPI, L1/L2 cache)
* π classification system (basic single-domain)
* Demo UI (Gradio on Hugging Face)
* Deal promotion, wayfinding, clarification
* Optional selfie flow
* Cache sync protocol
* Debug & observability

**Excluded:**
* Personalization
* Checkout/payment
* Vision-based recognition
* Cross-store learning

### Phase 2: Universal Core 🚧

**Goal:** Expand to multi-domain support

**New Capabilities:**
* Domain plugin system (YAML configs)
* Personal domain (reminders, notes, contacts)
* Cross-domain context tracking
* Enhanced entity resolution
* Knowledge graph relationships
* Multi-domain demo UI

**Upgrades:**
* Advanced classifier (Llama 3.2 3B fine-tuned)
* Improved cache generation
* Multi-tenant support

### Phase 3: Advanced Intelligence 📋

**Goal:** Enable autonomous reasoning and prediction

**New Capabilities:**
* Cross-domain reasoning (e.g., "remind me to buy X when near store")
* Predictive task generation
* Autonomous learning from interactions
* Multi-modal support (voice, vision, text)
* Business domain (CRM, support tickets)
* Research domain (papers, knowledge management)

### Phase 4: Platform & Ecosystem 🔮

**Goal:** Enable third-party domains and integrations

**New Capabilities:**
* Domain marketplace (community plugins)
* API for third-party edge devices
* White-label deployments
* Enterprise features (SSO, audit logs, compliance)
* Open-source core components
* Developer SDK and documentation

---

## 17. Risks & Mitigations

| Risk | Mitigation | Priority |
|------|-----------|----------|
| **Hallucination** | Cache-only prompts, strict contracts | Critical |
| **Latency** | Fast LLM + L1/L2 caching | Critical |
| **Classification drift** | π owns canonical memory, replay testing | High |
| **Debug difficulty** | Full trace logging, explainability | High |
| **Domain complexity** | Start with retail, validate architecture first | Medium |
| **Store data changes** | External feed ingestion, sync protocol | Medium |
| **Multi-domain conflicts** | Domain priority rules, disambiguation prompts | Low (Phase 2) |
| **Privacy concerns** | No PII storage, local-first option | Medium |
| **Scalability** | Design for horizontal scaling from day 1 | Medium |

---

## 18. Definition of Done

### Phase 1 (Retail MVP)

**Technical:**
* ✅ Edge backend fully functional on Pi 5
* ✅ π classification system working for retail domain
* ✅ Demo UI deployed to Hugging Face Spaces
* Cache sync protocol implemented
* Full observability and debugging

**Functional:**
* Stable in simulated store conditions
* Fast, natural conversation (<1s P95)
* Accurate wayfinding (>90% cache hits)
* Observable and replayable
* All user flows working end-to-end

**Validation:**
* Positive feedback from retail stakeholders
* "Would you keep this on the floor?" ≥ Yes
* Demo-ready for investors/customers

### Phase 2 (Universal Core)

* Multi-domain classification working
* ≥3 domains functional (retail + personal + business)
* Domain plugin system validated
* Cross-domain context demonstrated
* Knowledge graph operational

---

## 19. Future Extensions

**Post-MVP Enhancements:**
* Multilingual support (Spanish, French, etc.)
* Vector search for semantic retrieval
* Adaptive cache strategies (learn query patterns)
* Cross-store analytics (retail-specific)
* Advanced campaign optimization (retail-specific)
* Voice cloning for brand personality
* Emotion detection and response adaptation
* Integration marketplace (Zapier, IFTTT, etc.)

---

## 20. Why This Matters

### The Bigger Picture

Traditional AI assistants are **stateless chat interfaces** that forget everything.

π is a **persistent, structured intelligence layer** that learns and reasons.

| Traditional AI Assistant | π Universal Second Brain |
|------------------------|------------------------|
| Chat logs | Structured knowledge graph |
| No memory between sessions | Persistent canonical storage |
| Single domain (retail OR personal) | Universal (retail AND personal AND...) |
| Opaque black box | Explainable classifications |
| Expensive retraining for changes | Configuration file updates |
| Siloed data per application | Shared knowledge across domains |
| Vector search only | Structured schema + relationships |

**This is the foundation for truly intelligent, context-aware AI assistants that work across every domain of human activity.**

### Success Looks Like

* **For Users:** AI that remembers, learns, and helps across all contexts (work, home, shopping, research)
* **For Developers:** A universal intelligence layer they can plug into any application
* **For Businesses:** Deploy domain-specific AI without building from scratch
* **For Robotics:** Reachy Mini is just the first interface; the brain scales infinitely

---

**The vision:** Every AI assistant, regardless of domain, powered by a universal second brain that makes them smarter over time.
