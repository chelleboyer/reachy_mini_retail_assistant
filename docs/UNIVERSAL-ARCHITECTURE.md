# 🧠 Universal Second Brain - Architecture

**A domain-agnostic intelligence layer that classifies any interaction into structured knowledge**

---

## Vision

The Universal Second Brain is a **universal classification and memory system** that can power any AI assistant, regardless of domain. It transforms unstructured interactions into searchable, actionable knowledge while maintaining full explainability.

**Think of it as:**
- **Logseq/Roam** but with automatic classification
- **Zapier** but for knowledge, not just actions
- **Vector DB** but with structured schemas, not just embeddings
- **RAG** but with reasoning and relationships

---

## Universal Use Cases

### 🛒 Retail Assistant (Initial Implementation)
```
"Where's the milk?" 
→ Domain: retail 
→ Intent: product_lookup 
→ Entity: milk (product) 
→ Response: "Aisle 5, dairy section"
→ Store: Product entity + Event
```

### 📱 Personal Assistant
```
"Remind me to call mom tomorrow"
→ Domain: personal
→ Intent: create_reminder
→ Entities: mom (person), tomorrow (date), call (action)
→ Response: "Reminder set for tomorrow"
→ Store: Task + links to Person entity
```

### 💼 Business Assistant
```
"Customer Sarah complained about slow shipping"
→ Domain: business
→ Intent: support_ticket
→ Entities: Sarah (customer), shipping (service), slow (sentiment: negative)
→ Response: "Logged support ticket #1234"
→ Store: Event + Customer entity + Support ticket
```

### 🔬 Research Assistant
```
"Paper on quantum computing by John Smith"
→ Domain: research
→ Intent: knowledge_capture
→ Entities: John Smith (person), quantum computing (concept), paper (content)
→ Response: "Saved. Related: 3 papers you've read on quantum"
→ Store: Content + links to Concept + Expert
```

### 🏠 Home Assistant
```
"Kitchen light is flickering"
→ Domain: home
→ Intent: maintenance_issue
→ Entities: kitchen (place), light (device), flickering (problem)
→ Response: "Added to maintenance list. Last bulb change: 6 months ago"
→ Store: Task + Device + Maintenance log
```

---

## Architecture

### Three-Layer System

```
┌───────────────────────────────────────────────────────┐
│         EDGE LAYER (Domain-Specific)                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │  Reachy  │ │   App    │ │   Bot    │ │   CLI    │  │
│  │  Robot   │ │ (Mobile) │ │ (Slack)  │ │  (Voice) │  │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │
│       └────────────┼─────────────┼────────────┘       │
└────────────────────┼─────────────┼────────────────────┘
                     │             │
┌────────────────────▼─────────────▼───────────────────┐
│         UNIVERSAL CLASSIFICATION LAYER               │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │  Multi-Stage Classifier                        │  │
│  │  Stage 1: Domain Detection                     │  │
│  │  Stage 2: Intent Classification                │  │
│  │  Stage 3: Entity Extraction                    │    │
│  │  Stage 4: Canonical Type Mapping               │    │
│  │  Stage 5: Response Generation                  │    │
│  └────────────────────────────────────────────────┘    │
│                                                        │
│  ┌────────────────────────────────────────────────┐    │
│  │  Context & Reasoning Engine                    │    │
│  │  - Session management                          │    │
│  │  - Entity resolution                           │    │
│  │  - Relationship tracking                       │    │
│  │  - Inference & prediction                      │    │
│  └────────────────────────────────────────────────┘    │
└──────────────────────┬───────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────┐
│         CANONICAL STORAGE LAYER                      │
│                                                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Entities │ │  Events  │ │Knowledge │ │  Tasks  │ │
│  │          │ │          │ │          │ │         │ │
│  │ Person   │ │Interaction│ │  Fact   │ │  TODO   │ │
│  │ Place    │ │Transaction│ │  Rule   │ │Reminder │ │
│  │ Product  │ │Observation│ │Relation  │ │  Goal   │ │
│  │ Concept  │ │  Action   │ │Definition│ │ Request │ │
│  └──────────┘ └──────────┘ └──────────┘ └─────────┘ │
│                                                       │
│  ┌───────────────────────────────────────────────┐   │
│  │         Knowledge Graph                       │   │
│  │  Entity ←→ Event ←→ Knowledge ←→ Task        │   │
│  └───────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────┘
```

---

## Domain Plugins

The system uses **pluggable domain configurations**:

### Retail Domain
```yaml
domain: retail
intents:
  - product_lookup
  - promo_query
  - navigation
  - staff_request
entities:
  - product (sku, name, aisle, category, price)
  - promo (description, discount, expiry)
  - location (aisle, section, zone)
canonical_mapping:
  product → entity.product
  promo → event.transaction + knowledge.rule
  navigation → task.request
```

### Personal Domain
```yaml
domain: personal
intents:
  - create_reminder
  - log_contact
  - capture_note
  - find_info
entities:
  - person (name, email, phone, expertise)
  - datetime (date, time, duration)
  - location (address, coordinates)
canonical_mapping:
  reminder → task.todo + entity.person
  contact → entity.person + event.interaction
  note → content.note + knowledge.fact
```

---

## Multi-Stage Classification

### Example: Complex Cross-Domain Query

**Input:** "Remind me to buy milk when I'm near the grocery store"

**Stage 1: Domain Detection**
```
Primary: personal (reminder)
Secondary: retail (product)
Tertiary: location (geofence)
Confidence: 95%
```

**Stage 2: Intent Classification**
```
Domain: personal
Intent: create_reminder
Sub-intents: [product_lookup, location_trigger]
Confidence: 92%
```

**Stage 3: Entity Extraction**
```
Entities:
- "milk" → product (retail domain)
- "grocery store" → place (location)
- "when I'm near" → trigger condition (location-based)
- [implicit] "me" → person (user)
```

**Stage 4: Canonical Type Mapping**
```
Task: Buy milk
  type: todo
  trigger: geofence(grocery store, radius=100m)
  linked_entities: [milk (product), grocery store (place)]
  
Product: milk
  type: entity.product
  context: shopping_list
  
Trigger: Location-based
  type: rule
  condition: distance(user, grocery_store) < 100m
  action: notify(task)
```

**Stage 5: Response Generation**
```
Response: "I'll remind you about milk when you're near a grocery store. 
          I found 3 stores on your usual route. Want me to check for deals?"

Additional Actions:
- Add milk to shopping list
- Set geofence trigger
- Query retail domain for milk deals
- Store cross-domain relationship
```

---

## Key Features

### 1. Context Tracking
```
Session 1: "Where's the milk?"
→ Store context: current_product = milk

Session 1 (continued): "Any deals on it?"
→ Resolve "it" → milk (from context)
→ Query: promos for milk
```

### 2. Cross-Domain Reasoning
```
Input: "Schedule meeting with Alex about the product launch"
→ Domain 1: Business (meeting scheduling)
→ Domain 2: Retail (product launch context)
→ Creates: Calendar event + links to Product entity
→ Smart: Pulls product launch details automatically
```

### 3. Knowledge Graph
```
Entities:
- Alex (person) → expertise: [robotics, AI]
- Product Launch (event) → date: March 15
- Meeting (event) → participants: [Alex, User]

Relationships:
- Alex ← met_at → AI Conference
- Meeting ← about → Product Launch
- Product Launch ← involves → Alex (expert)

Inferences:
- "Who knows about robotics?" → Alex
- "What's happening in March?" → Product Launch, Meeting
```

### 4. Explainability
```
Query: "Got any deals?"
Classification:
  Intent: promo_query (92% confidence)
  Why: 
    - Keyword "deals" (high weight)
    - Question format (moderate weight)
    - Context: retail domain (previous queries)
  Entities: None extracted
  Response: Top 3 promos by priority
  Reasoning: Selected high-priority promos expiring soon
```

---

## Deployment Models

### Cloud Deployment (Hugging Face Spaces)
- Shared instance across all edge devices
- Multi-tenant with store/user isolation
- Global learning and optimization
- Suitable for: SaaS, consumer products

### Edge Deployment (Local Server)
- Local instance per location/user
- Complete privacy and control
- Works offline
- Suitable for: Enterprise, privacy-critical

### Hybrid Deployment
- Local classification for speed
- Cloud sync for learning
- Best of both worlds

---

## Technology Stack

**Classification:**
- Llama 3.2 3B (local, fast)
- GPT-4 (cloud, high quality)
- Custom fine-tuned models per domain

**Storage:**
- SQLite (local, portable)
- PostgreSQL (cloud, scalable)
- Knowledge graph: Neo4j or custom

**Interface:**
- Gradio (demo and prototyping)
- FastAPI (production API)
- WebSockets (real-time)

---

## Roadmap

**Phase 1: Retail MVP** ✅
- Domain: Retail
- Entities: Products, Promos, Locations
- Interface: Edge backend (any device)
- Storage: SQLite

**Phase 2: Universal Core** 🚧
- Multi-domain support
- Canonical type system
- Knowledge graph
- Context engine

**Phase 3: Advanced Intelligence** 📋
- Cross-domain reasoning
- Predictive tasks
- Autonomous learning
- Multi-modal (voice, vision, text)

**Phase 4: Platform** 🔮
- Domain marketplace
- Plugin system
- API for third-party integrations
- White-label deployments

---

## Why This Matters

**Traditional AI assistants are stateless chat interfaces.**

**The Second Brain is a persistent, structured intelligence layer.**

| Traditional AI | Universal Second Brain |
|---------------|------------------------|
| Chat logs | Structured knowledge |
| No memory | Canonical entities |
| Single domain | Cross-domain |
| Opaque | Explainable |
| Expensive retraining | Configuration changes |
| Siloed data | Knowledge graph |

**This is the foundation for truly intelligent, context-aware AI assistants across any domain.**
