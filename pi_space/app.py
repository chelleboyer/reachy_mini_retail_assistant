"""π (Pi) Second Brain - Demo Space

A demo Gradio interface showing how the Reachy Mini Second Brain
classifies customer interactions and manages store knowledge.

This is a DEMO - uses in-memory storage, mock data, and simplified logic.
"""

import gradio as gr
import json
from datetime import datetime
from typing import Dict, List, Any
import random

# ============================================================================
# MOCK DATA STORAGE (in-memory for demo)
# ============================================================================

MOCK_PRODUCTS = [
    {"sku": "001", "name": "Milk", "aisle": "5", "category": "Dairy", "price": 3.99},
    {"sku": "002", "name": "Bread", "aisle": "2", "category": "Bakery", "price": 2.49},
    {"sku": "003", "name": "Eggs", "aisle": "5", "category": "Dairy", "price": 4.29},
    {"sku": "004", "name": "Apples", "aisle": "1", "category": "Produce", "price": 5.99},
    {"sku": "005", "name": "Chicken", "aisle": "7", "category": "Meat", "price": 8.99},
]

MOCK_PROMOS = []

EVENT_INBOX = []


# ============================================================================
# CLASSIFIER (simplified for demo)
# ============================================================================

def classify_query(query: str) -> Dict[str, Any]:
    """Demo classifier - uses simple keyword matching."""
    query_lower = query.lower()
    
    # Intent classification
    if any(word in query_lower for word in ["where", "find", "looking for", "location", "aisle"]):
        intent = "product_lookup"
        confidence = 0.95
        target_db = "Products"
    elif any(word in query_lower for word in ["deal", "sale", "promo", "discount", "offer", "special"]):
        intent = "promo_query"
        confidence = 0.92
        target_db = "Campaigns"
    elif any(word in query_lower for word in ["selfie", "picture", "photo"]):
        intent = "selfie"
        confidence = 0.98
        target_db = "Operations"
    elif any(word in query_lower for word in ["help", "staff", "employee", "manager"]):
        intent = "staff_request"
        confidence = 0.88
        target_db = "Operations"
    else:
        intent = "general_inquiry"
        confidence = 0.60
        target_db = "Auto-log Inbox"
    
    # Generate response
    response = _generate_response(intent, query_lower)
    
    return {
        "intent": intent,
        "confidence": confidence,
        "target_db": target_db,
        "response": response,
        "timestamp": datetime.utcnow().isoformat(),
        "query": query
    }


def _generate_response(intent: str, query_lower: str) -> str:
    """Generate demo response based on intent."""
    if intent == "product_lookup":
        # Try to find matching product
        for product in MOCK_PRODUCTS:
            if product["name"].lower() in query_lower:
                return f"{product['name']} is in aisle {product['aisle']}. Look for the {product['category']} section."
        return "I'm not sure where that is. Let me get a staff member to help you."
    
    elif intent == "promo_query":
        if MOCK_PROMOS:
            promo = MOCK_PROMOS[0]
            return f"Great deal today: {promo['description']}!"
        return "We don't have special deals right now, but I can help you find what you need!"
    
    elif intent == "selfie":
        return "Would you like to take a selfie with me? Say cheese!"
    
    elif intent == "staff_request":
        return "I'll call a staff member to help you. Someone will be right over!"
    
    else:
        return "I'm here to help! You can ask me about product locations, deals, or take a selfie."


# ============================================================================
# GRADIO UI - TAB 1: CLASSIFIER DEMO
# ============================================================================

def demo_classify(query: str) -> tuple:
    """Classify query and show results."""
    if not query.strip():
        return "❌ Please enter a query", "", ""
    
    result = classify_query(query)
    
    # Format classification result
    classification = f"""## Classification Result

**Intent:** {result['intent']}
**Confidence:** {result['confidence']:.0%}
**Target Database:** {result['target_db']}

**Generated Response:**
> {result['response']}

**Timestamp:** {result['timestamp']}
"""
    
    # Format as JSON for technical view
    json_output = json.dumps(result, indent=2)
    
    # Add to event inbox
    EVENT_INBOX.append(result)
    
    return classification, json_output, f"✅ Event logged (total: {len(EVENT_INBOX)})"


# ============================================================================
# GRADIO UI - TAB 2: PROMO MANAGER
# ============================================================================

def add_promo(description: str, category: str, discount: float, priority: int) -> tuple:
    """Add a promotion."""
    if not description.strip():
        return "❌ Description required", _format_promos()
    
    promo = {
        "id": f"PROMO-{len(MOCK_PROMOS)+1:03d}",
        "description": description,
        "category": category or "All",
        "discount_percent": discount,
        "priority": priority,
        "created_at": datetime.utcnow().isoformat()
    }
    
    MOCK_PROMOS.append(promo)
    
    return f"✅ Added promo: {promo['id']}", _format_promos()


def _format_promos() -> str:
    """Format promos for display."""
    if not MOCK_PROMOS:
        return "No promotions yet. Add some above!"
    
    output = "## Current Promotions\n\n"
    for promo in sorted(MOCK_PROMOS, key=lambda p: p['priority'], reverse=True):
        output += f"**{promo['id']}** (Priority: {promo['priority']})\n"
        output += f"- {promo['description']}\n"
        if promo['discount_percent'] > 0:
            output += f"- Discount: {promo['discount_percent']:.0f}%\n"
        output += f"- Category: {promo['category']}\n\n"
    
    return output


# ============================================================================
# GRADIO UI - TAB 3: CACHE BUILDER
# ============================================================================

def build_cache(store_id: str) -> tuple:
    """Generate L2 cache JSON for download."""
    cache = {
        "version": f"1.0.{random.randint(1, 999)}",
        "store_id": store_id or "STORE-DEMO",
        "timestamp": datetime.utcnow().isoformat(),
        "products": MOCK_PRODUCTS,
        "promos": MOCK_PROMOS,
        "metadata": {
            "product_count": len(MOCK_PRODUCTS),
            "promo_count": len(MOCK_PROMOS),
            "generated_by": "pi_demo_space"
        }
    }
    
    json_str = json.dumps(cache, indent=2)
    
    summary = f"""## Cache Built Successfully

**Store ID:** {cache['store_id']}
**Version:** {cache['version']}
**Products:** {len(MOCK_PRODUCTS)}
**Promotions:** {len(MOCK_PROMOS)}
**Timestamp:** {cache['timestamp']}

This cache can be loaded into the edge backend's L2 SQLite database.
"""
    
    return summary, json_str


# ============================================================================
# GRADIO APP CONSTRUCTION
# ============================================================================

def create_app():
    """Create the Gradio interface."""
    
    with gr.Blocks(title="π Second Brain Demo", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🧠 π (Pi) Second Brain - Demo
        
        **Demo interface for Reachy Mini's classification and knowledge management system.**
        
        This shows how customer queries are classified, promos are managed, and cache is built for edge devices.
        """)
        
        with gr.Tabs():
            # TAB 1: Classifier
            with gr.Tab("🔍 Classifier Demo"):
                gr.Markdown("""
                Enter a customer query to see how it would be classified and what response would be generated.
                
                **Try examples like:**
                - "Where can I find milk?"
                - "What deals do you have today?"
                - "Can I take a selfie?"
                """)
                
                with gr.Row():
                    query_input = gr.Textbox(
                        label="Customer Query",
                        placeholder="Where is the milk?",
                        lines=2
                    )
                
                classify_btn = gr.Button("🔍 Classify", variant="primary")
                
                with gr.Row():
                    with gr.Column():
                        classification_output = gr.Markdown(label="Classification Result")
                    with gr.Column():
                        json_output = gr.Code(label="JSON Output", language="json")
                
                status_output = gr.Textbox(label="Status")
                
                classify_btn.click(
                    demo_classify,
                    inputs=[query_input],
                    outputs=[classification_output, json_output, status_output]
                )
            
            # TAB 2: Promo Manager
            with gr.Tab("🎁 Promo Manager"):
                gr.Markdown("""
                Add and manage promotions that will be pushed to edge devices.
                """)
                
                with gr.Row():
                    promo_desc = gr.Textbox(
                        label="Promo Description",
                        placeholder="50% off all dairy products",
                        lines=2
                    )
                
                with gr.Row():
                    promo_category = gr.Textbox(
                        label="Category (optional)",
                        placeholder="Dairy"
                    )
                    promo_discount = gr.Number(
                        label="Discount %",
                        value=0,
                        minimum=0,
                        maximum=100
                    )
                    promo_priority = gr.Slider(
                        label="Priority",
                        minimum=1,
                        maximum=10,
                        value=5,
                        step=1
                    )
                
                add_promo_btn = gr.Button("➕ Add Promo", variant="primary")
                
                promo_status = gr.Textbox(label="Status")
                promo_list = gr.Markdown(value=_format_promos())
                
                add_promo_btn.click(
                    add_promo,
                    inputs=[promo_desc, promo_category, promo_discount, promo_priority],
                    outputs=[promo_status, promo_list]
                )
            
            # TAB 3: Cache Builder
            with gr.Tab("📦 Cache Builder"):
                gr.Markdown("""
                Generate L2 cache file for edge devices. This contains all products and promos
                that will be available for fast lookup.
                """)
                
                store_id_input = gr.Textbox(
                    label="Store ID",
                    placeholder="STORE-001",
                    value="STORE-DEMO"
                )
                
                build_btn = gr.Button("🔨 Build Cache", variant="primary")
                
                cache_summary = gr.Markdown()
                cache_json = gr.Code(label="Cache JSON (download this)", language="json")
                
                build_btn.click(
                    build_cache,
                    inputs=[store_id_input],
                    outputs=[cache_summary, cache_json]
                )
        
        gr.Markdown("""
        ---
        **Note:** This is a demo with in-memory storage. Restarting will clear all data.
        
        For production: Use persistent database, authentication, and proper event queue.
        """)
    
    return demo


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    app = create_app()
    app.launch()
