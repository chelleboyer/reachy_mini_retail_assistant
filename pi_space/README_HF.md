---
title: Pi Second Brain Demo
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# π (Pi) Second Brain - Demo

Demo interface for Reachy Mini's classification and knowledge management system.

## What This Space Does

1. **Classifies Customer Queries** - Shows how natural language is converted to structured intents
2. **Manages Promotions** - Simple interface to add/edit store deals
3. **Builds Edge Caches** - Generates JSON cache files for edge devices

## How It Works

- Customer query → Intent classification → Target database
- Promos → Cache builder → Download for edge device
- Events → Auto-log inbox → Manual review

## Try It

Use the tabs to:
- Test query classification
- Add demo promotions  
- Build a cache file

## Next Steps

This is a simplified demo. Production version needs:
- Persistent storage (SQLite/Postgres)
- Authentication
- Real LLM for classification
- Event queue with retry
- Multi-store support
