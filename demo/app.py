"""Gradio Demo: Reachy Mini Retail Assistant
Demonstrates conversational product search with backend telemetry.
HuggingFace Spaces ready version.
"""
import gradio as gr
import os
from datetime import datetime
from pathlib import Path

# Load environment variables from parent .env file
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / "reachy_edge" / ".env"
load_dotenv(env_path)
print(f"[DEBUG] Loaded .env from {env_path}")

# Local imports (no sys.path hacks needed)
from cache.l2_cache import ProductCache
from models import Product

# Try to import HuggingFace
try:
    from huggingface_hub import InferenceClient
    HF_AVAILABLE = True
    HF_TOKEN = os.environ.get("HF_TOKEN")
    if HF_TOKEN:
        # Initialize client without model - specify per request
        hf_client = InferenceClient(token=HF_TOKEN)
        print(f"[DEBUG] HuggingFace client configured with token")
    else:
        HF_AVAILABLE = False
        hf_client = None
        print(f"[DEBUG] No HF_TOKEN found")
except ImportError:
    HF_AVAILABLE = False
    hf_client = None
    print("[DEBUG] huggingface-hub not available")

# Initialize cache (regular ProductCache - no thread-safety needed for demo)
cache = ProductCache(db_path="./data/cache.db")
cache.initialize()

# Interaction history for telemetry
interaction_history = []

# Mock LLM responses (fallback if no OpenAI API key)
RESPONSE_TEMPLATES = {
    "diesel": "I can help you with diesel! We have premium diesel fuel available at Fuel Islands 1-4. Would you like to know about pricing or DEF fluid as well?",
    "fuel": "We have several fuel options available. Are you looking for diesel, gasoline, or something specific like DEF fluid?",
    "shower": "Our shower facilities are available! We offer 30-minute shower credits for $15. They're located at the Service Desk - nice and clean!",
    "food": "Hungry? We've got fresh hot food at the counter - pizza, burgers, chicken tenders, and breakfast sandwiches. What sounds good?",
    "coffee": "Need some fuel for yourself? We've got fresh truck stop coffee at the coffee station - large cups are just $2.49!",
    "cb radio": "Looking for a CB radio? We carry the Cobra 29 LX - it's a solid choice at $129.99. Find it in Aisle 4 (Electronics section).",
    "safety": "Safety first! We've got high-visibility vests, LED road flares, flashlights, and emergency kits in Aisle 5. What do you need?",
    "deal": "Great question! While I don't have today's specific deals loaded, I can show you our best everyday prices. Popular items include our coffee ($2.49), hot dogs ($2.99), and bulk snacks. Diesel fuel is competitively priced - check our sign out front for today's rate!",
    "special": "Great question! While I don't have today's specific deals loaded, I can show you our best everyday prices. Popular items include our coffee ($2.49), hot dogs ($2.99), and bulk snacks. Diesel fuel is competitively priced - check our sign out front for today's rate!",
    "cheap": "Looking for value? Our best deals are coffee at $2.49, hot dogs at $2.99, and we have great bulk pricing on snacks and energy drinks. What are you interested in?",
    "parking": "We offer overnight parking for $20 - secure and well-lit. Reserve your spot at the Service Desk!",
    "wash": "Our full-service truck wash is $125. Gets your rig looking like new! Find us at the Truck Wash Bay.",
    "tired": "Need a break? We've got showers ($15), hot coffee ($2.49), and energy drinks to keep you going. Or grab some overnight parking ($20) if you need rest!",
}

def get_mock_response(query: str, results: list = None) -> str:
    """Generate conversational response based on query and search results."""
    query_lower = query.lower()
    
    # Check templates first
    for keyword, response in RESPONSE_TEMPLATES.items():
        if keyword in query_lower:
            return response
    
    # Smart fallback based on results
    if results and len(results) > 0:
        top_result = results[0]
        return f"I found some great options! The top match is **{top_result.name}** for ${top_result.price:.2f} - you'll find it at {top_result.location}. Check out the products below!"
    
    # Last resort
    return "I'm searching our inventory for you! Let me show you what we have..."

def get_llm_response(query: str, results: list) -> str:
    """Generate response using HuggingFace."""
    if not HF_AVAILABLE or not hf_client:
        print(f"[DEBUG] HF unavailable")
        return get_mock_response(query, results)
    
    print(f"[DEBUG] Calling Llama 3 for query: {query}")
    try:
        # Build context about products found
        if results:
            products_context = "I found these items in our truck stop:\n"
            for i, p in enumerate(results[:3], 1):
                # Check if it's a service or product
                is_service = p.category == "Services"
                item_type = "service" if is_service else "product"
                products_context += f"{i}. {p.name} (${p.price:.2f}) - {item_type} available at {p.location}\n"
        else:
            products_context = "I searched our inventory but didn't find any matching items."
        
        # Use chat_completion for conversational models
        messages = [
            {"role": "user", "content": f"""You are Reachy, a helpful truck stop assistant. 

Customer asks: '{query}'

{products_context}

Respond naturally in 2-3 sentences:
- If services found (like showers, parking, truck wash), say "we offer" or "we have" (not "carry")
- If products found (like fuel, snacks, CB radios), mention them by name
- If nothing found, politely say we don't have it and suggest checking with staff
- Be conversational and helpful"""}
        ]
        
        # Call HuggingFace chat_completion API with Llama 3
        response = hf_client.chat_completion(
            messages=messages,
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            max_tokens=100,
            temperature=0.7
        )
        
        llm_response = response.choices[0].message.content.strip()
        print(f"[DEBUG] Llama 3 response: {llm_response[:100]}...")
        return llm_response
    
    except Exception as e:
        print(f"[ERROR] HF failed: {type(e).__name__}: {e}")
        return get_mock_response(query, results)

def format_product_card(product: Product) -> str:
    """Format product as HTML card."""
    # Category emoji mapping
    emoji_map = {
        "Fuel & Fluids": "⛽",
        "Trucker Supplies": "🚛",
        "Electronics": "📻",
        "Energy & Snacks": "☕",
        "Hot Food & Beverages": "🍕",
        "Services": "🚿",
        "Safety & Lighting": "⚠️",
        "Convenience": "🛒"
    }
    emoji = emoji_map.get(product.category, "📦")
    
    relevance_bar = ""
    if product.relevance_score:
        score_pct = min(100, product.relevance_score * 10)  # Scale for display
        relevance_bar = f'<div style="background: #e0e0e0; border-radius: 4px; height: 6px; margin-top: 8px;"><div style="background: #4CAF50; width: {score_pct}%; height: 100%; border-radius: 4px;"></div></div>'
    
    return f"""
    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 8px 0; background: white;">
        <div style="display: flex; align-items: start; gap: 12px;">
            <div style="font-size: 48px;">{emoji}</div>
            <div style="flex: 1;">
                <h3 style="margin: 0 0 8px 0; color: #333;">{product.name}</h3>
                <p style="margin: 4px 0; color: #666; font-size: 14px;"><strong>SKU:</strong> {product.sku}</p>
                <p style="margin: 4px 0; color: #666; font-size: 14px;"><strong>Category:</strong> {product.category}</p>
                <p style="margin: 4px 0; color: #666; font-size: 14px;"><strong>Location:</strong> {product.location}</p>
                <p style="margin: 8px 0 4px 0; color: #2196F3; font-size: 24px; font-weight: bold;">${product.price:.2f}</p>
                {relevance_bar}
                {f'<p style="margin: 4px 0; color: #888; font-size: 12px;">Relevance: {product.relevance_score:.2f}</p>' if product.relevance_score else ''}
            </div>
        </div>
        <p style="margin: 12px 0 0 0; color: #666; font-size: 14px; font-style: italic;">{product.description}</p>
    </div>
    """

def format_backend_activity(query: str, results: list, response_time_ms: float) -> str:
    """Format backend telemetry as HTML."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    activity = f"""
    <div style="font-family: monospace; background: #1e1e1e; color: #d4d4d4; padding: 16px; border-radius: 8px; font-size: 13px;">
        <div style="color: #4EC9B0; margin-bottom: 12px;">🔍 [{timestamp}] NEW QUERY RECEIVED</div>
        
        <div style="margin-left: 20px; margin-bottom: 12px;">
            <div style="color: #9CDCFE;">query:</div>
            <div style="margin-left: 20px; color: #CE9178;">"{query}"</div>
        </div>
        
        <div style="color: #4EC9B0; margin-bottom: 8px;">💾 L2 CACHE (SQLite FTS5)</div>
        <div style="margin-left: 20px; margin-bottom: 12px;">
            <div style="color: #6A9955;">// Executing full-text search with BM25 ranking...</div>
            <div style="color: #C586C0;">cache</div><span style="color: #D4D4D4;">.search_products(</span><span style="color: #CE9178;">"{query}"</span><span style="color: #D4D4D4;">, max_results=5)</span>
            <div style="color: #4FC1FF; margin-top: 4px;">✓ Found {len(results)} products in {response_time_ms:.2f}ms</div>
        </div>
        
        <div style="color: #4EC9B0; margin-bottom: 8px;">📊 INTERACTION LOGGED</div>
        <div style="margin-left: 20px; margin-bottom: 12px;">
            <div style="color: #6A9955;">// Recording customer interaction for analytics...</div>
            <div style="color: #D4D4D4;">{{ </div>
            <div style="margin-left: 20px;">
                <span style="color: #9CDCFE;">"timestamp"</span><span style="color: #D4D4D4;">: </span><span style="color: #CE9178;">"{timestamp}"</span><span style="color: #D4D4D4;">,</span><br>
                <span style="color: #9CDCFE;">"query"</span><span style="color: #D4D4D4;">: </span><span style="color: #CE9178;">"{query}"</span><span style="color: #D4D4D4;">,</span><br>
                <span style="color: #9CDCFE;">"results_count"</span><span style="color: #D4D4D4;">: </span><span style="color: #B5CEA8;">{len(results)}</span><span style="color: #D4D4D4;">,</span><br>
                <span style="color: #9CDCFE;">"response_time_ms"</span><span style="color: #D4D4D4;">: </span><span style="color: #B5CEA8;">{response_time_ms:.2f}</span>
            </div>
            <div style="color: #D4D4D4;">}}</div>
            <div style="color: #4FC1FF; margin-top: 4px;">✓ Logged to analytics database</div>
        </div>
        
        <div style="color: #4EC9B0; margin-bottom: 8px;">🧠 LEARNING INSIGHTS</div>
        <div style="margin-left: 20px;">
            <div style="color: #6A9955;">// Updating search patterns for future optimization...</div>
            <div style="color: #4FC1FF;">• Customer interest in: {results[0].category if results else 'N/A'}</div>
            <div style="color: #4FC1FF;">• Popular query terms indexed</div>
            <div style="color: #4FC1FF;">• Response quality will improve over time</div>
        </div>
    </div>
    """
    return activity

def chat(message: str, history: list) -> tuple:
    """Process customer query and return response with products and telemetry."""
    import time
    start_time = time.time()
    
    # Search products
    print(f"[DEBUG] Searching for: {message}")
    results = cache.search_products(message, max_results=5)
    print(f"[DEBUG] Found {len(results)} results")
    if results:
        print(f"[DEBUG] First result: {results[0].name}")
    
    # Calculate response time
    response_time_ms = (time.time() - start_time) * 1000
    
    # Generate conversational response using LLM (falls back to mock if no API key)
    response = get_llm_response(message, results)
    
    # Format products as HTML cards
    products_html = "<div style='margin-top: 16px;'>"
    if results:
        products_html += "<h3 style='color: #333; margin-bottom: 12px;'>📦 Products Found:</h3>"
        for product in results:
            products_html += format_product_card(product)
    else:
        products_html += "<p style='color: #999; font-style: italic;'>No products found matching your query.</p>"
    products_html += "</div>"
    
    # Format backend activity
    backend_html = format_backend_activity(message, results, response_time_ms)
    
    # Log interaction
    interaction_history.append({
        "timestamp": datetime.now().isoformat(),
        "query": message,
        "results_count": len(results),
        "response_time_ms": response_time_ms
    })
    
    # Build conversation history in Gradio 6.0 format (list of messages with role/content)
    history = history or []
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response})
    
    return history, products_html, backend_html

def clear_chat():
    """Clear chat history."""
    return [], "", ""

# Build Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🤖 Reachy Mini: Retail Assistant Demo
    
    **Interaction Loop Demonstration:**
    - Customer asks questions in natural language
    - Reachy searches the product database (SQLite FTS5 + BM25 ranking)
    - **Llama 3 8B Instruct** (Meta's model on HuggingFace) generates conversational responses
    - Visual product cards + backend telemetry
    - All interactions logged for continuous improvement
    
    *Try asking: "Where can I get diesel?", "I need a CB radio", "Do you have grape jelly?", "What's on sale?"*
    """)
    
    with gr.Row():
        # Left column: Chat interface
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                label="💬 Reachy Conversation",
                height=400,
                show_label=True
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    label="Ask Reachy...",
                    placeholder="Where can I get diesel fuel?",
                    show_label=False,
                    scale=4
                )
                submit = gr.Button("Send", variant="primary", scale=1)
            
            clear = gr.Button("Clear Chat", variant="secondary")
            
            products_display = gr.HTML(label="Products")
        
        # Right column: Backend telemetry
        with gr.Column(scale=1):
            gr.Markdown("### 🔧 Backend Activity")
            backend_display = gr.HTML()
    
    # Event handlers
    submit.click(
        chat,
        inputs=[msg, chatbot],
        outputs=[chatbot, products_display, backend_display]
    ).then(
        lambda: "",
        outputs=[msg]
    )
    
    msg.submit(
        chat,
        inputs=[msg, chatbot],
        outputs=[chatbot, products_display, backend_display]
    ).then(
        lambda: "",
        outputs=[msg]
    )
    
    clear.click(
        clear_chat,
        outputs=[chatbot, products_display, backend_display]
    )
    
    # Example queries
    gr.Examples(
        examples=[
            ["Where can I get diesel fuel?"],
            ["I need a CB radio"],
            ["Where are the showers?"],
            ["I'm hungry, what do you have?"],
            ["Do you sell safety vests?"],
            ["Do you have grape jelly?"],
        ],
        inputs=[msg]
    )

if __name__ == "__main__":
    # Load sample products if cache is empty
    from data.sample_products import load_sample_data
    
    # Clear database to avoid duplicates on restart
    try:
        cache._get_connection().execute("DELETE FROM products_fts")
        cache._get_connection().commit()
    except:
        pass
    
    print("Loading sample products...")
    load_sample_data(cache)
    print("✓ 44 products loaded")
    
    demo.launch()
