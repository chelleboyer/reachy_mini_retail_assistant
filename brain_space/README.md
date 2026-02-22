# 🧠 Brain Space - Universal Second Brain Demo

**A Gradio-based demo interface for the universal classification system**

---

## Overview

Brain Space is the **demo and admin interface** for the Universal Second Brain. It showcases multi-stage classification, canonical storage, and cross-domain reasoning in an interactive web UI.

**Not just a retail demo.** Brain Space demonstrates universal classification across any domain.

---

## What is Universal Second Brain?

The Universal Second Brain is a **domain-agnostic intelligence layer** that classifies any interaction into structured, searchable knowledge.

Think of it as:
- **Logseq/Roam** but with automatic classification
- **RAG** but with structured schemas, not just embeddings
- **Zapier** but for knowledge, not just actions
- **A universal second brain** for any AI assistant

### Core Capabilities

1. **Multi-Stage Classification**
   - Domain Detection (retail, personal, business, research, etc.)
   - Intent Classification (lookup, create, update, navigate, etc.)
   - Entity Extraction (products, people, dates, concepts, etc.)
   - Canonical Type Mapping (entity, event, knowledge, task, content)

2. **Universal Canonical Storage**
   - Entities: person, place, product, concept, organization
   - Events: interaction, transaction, observation, action
   - Knowledge: fact, rule, relationship, definition
   - Tasks: todo, reminder, goal, request
   - Content: document, media, message, note

3. **Cross-Domain Reasoning**
   - Link entities across domains
   - Build knowledge graphs
   - Enable contextual inference

---

## Features in This Demo

### 🎯 Classifier Tab

Test the multi-stage classifier with queries across any domain:

**Retail Examples:**
- "Where's the milk?"
- "Any deals on pasta?"
- "Take me to the dairy section"

**Personal Examples:**
- "Remind me to call mom tomorrow"
- "Add buy groceries to my todo list"
- "When did I last talk to John?"

**Business Examples:**
- "Log support ticket for Sarah's shipping issue"
- "Schedule meeting with Alex about product launch"

**Home Examples:**
- "Kitchen light is flickering"
- "Set temperature to 72 degrees"

The classifier will show:
1. Domain detection
2. Intent classification
3. Entity extraction
4. Canonical type mapping
5. Response generation
6. Confidence scores and reasoning

### 📦 Promo Manager Tab (Retail Domain Plugin)

Demonstrates domain-specific admin tools:
- Add/edit/delete promotions
- Set priorities and expiry dates
- View active campaigns

**This is just one domain.** Other domains would have their own tools:
- **Personal:** Contact manager, task dashboard
- **Business:** Support ticket queue, meeting scheduler
- **Research:** Paper library, concept graph

### 🔨 Cache Builder Tab

Shows how the system generates domain-filtered cache snapshots for edge devices:
- Add entries (products, promos, etc.)
- Export cache as JSON
- Preview cache structure

---

## Running Locally

```bash
cd brain_space
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
python app.py
```

Open http://localhost:7860

---

## Deploying to Hugging Face Spaces

1. Create new Space at https://huggingface.co/new-space
2. Choose **Gradio** as the SDK
3. Set hardware: CPU Basic (free) is sufficient for demo
4. Upload files: `app.py`, `requirements.txt`, `README.md`
5. Hugging Face will automatically detect Gradio and run app.py
6. Your demo will be live at `https://huggingface.co/spaces/YOUR_USERNAME/brain-space`

Optional: Set secrets in Space settings for real LLM integration:
   - `OPENAI_API_KEY` (for OpenAI)
   - `HF_TOKEN` (for Llama models)

---

## Current Status

**Phase 1:** Mock classifier with keyword-based intent detection

**What Works:**
- Basic intent classification (retail domain)
- Simple entity extraction
- Promo management interface
- Cache generation for retail

**Coming in Phase 2:**
- LLM-powered classification (Llama 3.2 3B)
- Multi-domain support with real canonical storage
- Knowledge graph visualization
- Cross-domain query examples
- Confidence scoring and explainability

---

## Architecture

```
┌─────────────────────────────────────┐
│      Brain Space (Gradio UI)           │
│  ┌───────────────────────────────┐  │
│  │  Classifier Demo              │  │
│  │  - Multi-domain testing       │  │
│  │  - Confidence visualization   │  │
│  │  - Reasoning explanation      │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  Domain Admin Tools           │  │
│  │  - Retail: Promo manager      │  │
│  │  - Personal: Task dashboard   │  │
│  │  - Business: Ticket queue     │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  Cache Builder                │  │
│  │  - Domain-filtered snapshots  │  │
│  │  - Export for edge devices    │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
           │
           │ (In production)
           │
┌──────────▼──────────────────────────┐
│  Classification Engine               │
│  - Multi-stage pipeline             │
│  - Canonical storage                │
│  - Knowledge graph                  │
│  - Context tracking                 │
└─────────────────────────────────────┘
```

---

## Demo vs Production

**This is a DEMO with in-memory storage.** 

For production you'd need:
- Persistent canonical database (PostgreSQL, Neo4j)
- Authentication and authorization (multi-tenant)
- Rate limiting and error handling
- Event queue with retry logic (Kafka, RabbitMQ)
- Backup and restore procedures
- Monitoring and alerting
- Horizontal scaling infrastructure

---

## Why This Matters

**This is not just a retail assistant demo.**

This demonstrates a **universal intelligence layer** that can power AI assistants across:
- 🛒 Retail (product lookup, deals, navigation)
- 📱 Personal productivity (reminders, notes, contacts)
- 💼 Business automation (CRM, support, scheduling)
- 🔬 Research (papers, concepts, knowledge management)
- 🏠 Home automation (devices, maintenance, control)
- ...and any other domain

**The same classification engine. The same canonical storage. Different domain configurations.**

That's the power of Universal Second Brain.

---

## Contributing

Ideas for new domains? Suggestions for improvements?

We're especially interested in:
- New domain plugin examples
- Classifier improvement ideas
- UI/UX enhancements
- Demo query examples

---

**Built with ❤️ to demonstrate the future of universal AI assistants**
     │  Mock Storage  │
     │  (In-Memory)   │
     └────────────────┘
```

## Usage

**Test Classification:**
- Enter customer query
- See how it's classified (intent, confidence, target DB)
- See what response would be generated

**Manage Promos:**
- Add promotions with descriptions
- Set priority and expiry
- See how they'd appear in cache

**Build Cache:**
- Generate mock L2 cache JSON
- Download for testing with edge backend
- See what would be pushed to devices
