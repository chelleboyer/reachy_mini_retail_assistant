# 🤖 Reachy Mini: Retail Assistant Demo

Interactive demonstration of Reachy Mini's retail assistant capabilities, featuring conversational product search powered by SQLite FTS5 and GPT-4o-mini.

## 🌟 Features

- **Conversational Interface**: Natural language product queries
- **Smart Search**: SQLite FTS5 with BM25 ranking for relevance
- **AI-Powered Responses**: Microsoft Phi-3-mini (OSS model) generates contextual replies via HF Inference API
- **Visual Product Cards**: Rich UI with category emojis and pricing
- **Backend Telemetry**: Real-time view of database queries and analytics
- **Thread-Safe**: Handles concurrent requests in production

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the demo
python app.py
```

The demo will launch on http://localhost:7860 with sample products pre-loaded.

### HuggingFace Spaces Deployment

1. **Create New Space**:
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose "Gradio" SDK
   - Upload all files from this directory

2. **Optional - Set HF Token** (for private models):
   - Go to Space Settings → Repository secrets
   - Add secret: `HF_TOKEN` = `your-token-here`
   - Not needed for public models like Phi-3

3. **Deploy**:
   - Commit files to Space repository
   - Space will auto-build and deploy
   - Share your public URL!

## 📦 Sample Products

The demo includes 44 realistic truck stop products across 8 categories:
- ⛽ Fuel & Fluids (diesel, DEF, oil)
- 🚛 Trucker Supplies (logbooks, tie-downs)
- 📻 Electronics (CB radios, GPS)
- ☕ Energy & Snacks (coffee, drinks, jerky)
- 🍕 Hot Food & Beverages (pizza, burgers)
- 🚿 Services (showers, parking, truck wash)
- ⚠️ Safety & Lighting (flares, vests)
- 🛒 Convenience (sundries, hygiene)

## 💬 Example Queries

Try these to see Reachy in action:

- "Where can I get diesel fuel?"
- "I need a CB radio"
- "Do you have grape jelly?"
- "Where are the showers?"
- "I'm hungry, what do you have?"
- "Do you sell safety vests?"
- "What deals do you have today?"

## 🔧 Technical Architecture

### Stack
- **Frontend**: Gradio 6.3.0 (web interface)
- **Search**: SQLite FTS5 with BM25 ranking
- **LLM**: Microsoft Phi-3-mini-4k-instruct (via HF Inference API)
- **Data Models**: Pydantic 2.x for validation
- **Logging**: structlog for telemetry

### Thread Safety
Uses `ThreadSafeProductCache` with `threading.local()` to ensure each Gradio request gets its own SQLite connection. Critical for production deployment where multiple users interact simultaneously.

### Search Pipeline
1. User query → FTS5 tokenization
2. BM25 relevance ranking
3. Top 5 results retrieved
4. Phi-3-mini generates contextual response
5. Products displayed as visual cards
6. Telemetry logged for analytics

## 🎨 Customization

### Adding Your Own Products

Edit `data/sample_products.py`:

```python
products = [
    {
        "sku": "YOUR-SKU",
        "name": "Your Product Name",
        "description": "Product description...",
        "category": "Your Category",
        "price": 29.99,
        "location": "Aisle 1"
    },
    # ... more products
]
```

### Changing LLM Model

Edit `app.py` line 17:

```python
client = InferenceClient(model="microsoft/Phi-3-mini-4k-instruct", token=HF_TOKEN)
# Try other models:
# - "meta-llama/Llama-3.2-3B-Instruct"
# - "mistralai/Mistral-7B-Instruct-v0.2"
# - "HuggingFaceH4/zephyr-7b-beta"
```

### Adjusting Search Results

Edit `app.py` line 194:

```python
results = cache.search_products(message, max_results=5)  # Change limit
```

## 📊 Performance

- **Search Latency**: <100ms for typical queries
- **Products Indexed**: 44 (expandable to thousands)
- **Concurrent Users**: Thread-safe design supports multiple simultaneous sessions
- **Cache Size**: ~100KB for 44 products

## 🐛 Troubleshooting

**"No products found"**
- Check if `data/cache.db` exists and is populated
- App auto-loads samples on first run

**"LLM not working"**
- Demo uses HuggingFace Inference API (free on HF Spaces)
- Falls back to mock responses if HF unavailable
- Check model is public and accessible

**"Threading errors"**
- Ensure using `ThreadSafeProductCache`, not `ProductCache`
- Each thread needs isolated SQLite connection

## 📝 License

MIT License - See parent repository for details.

## 🔗 Links

- **Main Project**: [reachy-mini-retail-assistant](https://github.com/yourusername/reachy-mini-retail-assistant)
- **Story 1.2**: L2 Cache Implementation (this demo's foundation)
- **Reachy Robot**: [Pollen Robotics](https://www.pollen-robotics.com/)

---

**Built with ❤️ for the Reachy Mini project**
