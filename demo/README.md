---
title: Reachy Retail Assistant Demo
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 6.3.0
app_file: app.py
pinned: false
---

# 🤖 Reachy Mini Demo - Intelligent Truck Stop Assistant

Interactive demo showcasing conversational product search powered by FTS5 search and Llama 3 8B.

## Features

- 💬 **Natural Language Search**: Ask questions in plain English
- 🧠 **Smart Keyword Extraction**: Filters stop words and expands synonyms
  - "I'm hungry" → searches for food, meal, snack, pizza, burger, etc.
  - "Where's diesel fuel?" → searches for diesel OR fuel
- 🔍 **Full-Text Search**: SQLite FTS5 with BM25 relevance ranking
- 🤖 **Conversational AI**: Meta Llama 3 8B Instruct for natural responses
- 🎨 **Visual Product Cards**: Emoji-categorized products with pricing and location
- 📊 **Backend Telemetry**: Real-time visibility into cache queries and interaction logging
- 📈 **Analytics Tracking**: All interactions logged for continuous improvement

## Try These Queries

- "Where can I get diesel fuel?"
- "I'm hungry, what do you have?"
- "Do you have CB radios?"
- "Where are the showers?"
- "I need motor oil"
- "I'm thirsty"

## Tech Stack

- **Search**: SQLite FTS5 with stop word filtering and keyword expansion
- **LLM**: Meta Llama 3 8B Instruct via HuggingFace Inference API
- **UI**: Gradio 6.3.0
- **Backend**: Python with Pydantic, structlog

## Configuration

Set your `HF_TOKEN` as a Space secret to enable Llama 3 inference.

## Quick Start (Local)

```bash
# Install dependencies
cd demo
pip install -r requirements.txt

# Run the demo (loads 44 truck stop products automatically)
python app.py
```

## Deploy to HuggingFace Spaces

1. **Create a new Space** on HuggingFace
2. **Select SDK**: Gradio
3. **Upload all files** from the `demo/` folder:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `cache/` folder (l2_cache.py, __init__.py)
   - `models/` folder (__init__.py)
   - `data/` folder (sample_products.py)
4. **Set Space Secret**: Add `HF_TOKEN` with your HuggingFace API token
5. Space will auto-launch!

No .env file needed - HF_TOKEN comes from Space secrets.

## Customization

### Add Real LLM (OpenAI/Anthropic)

Replace the `get_mock_response()` function:

```python
import openai

def get_mock_response(query: str, products: list) -> str:
    """Generate response using OpenAI."""
    product_context = "\n".join([f"- {p.name} (${p.price})" for p in products[:3]])
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Reachy, a helpful truck stop retail assistant."},
            {"role": "user", "content": f"Customer asks: {query}\n\nAvailable products:\n{product_context}"}
        ]
    )
    return response.choices[0].message.content
```

### Styling

Edit `custom_css` variable in `gradio_app.py` to match your brand.

### Product Images

Replace emoji in `format_product_card()` with:
```python
<img src="{product.image_url}" style="width: 64px; height: 64px; object-fit: cover;">
```

## Architecture

```
Customer Query → Gradio Interface
                      ↓
                 Mock LLM Response
                      ↓
                L2 Cache Search (FTS5)
                      ↓
          Product Results + Telemetry
                      ↓
              HTML Cards + Activity Log
```
