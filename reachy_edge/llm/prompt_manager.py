"""Prompt management for LLM interactions."""
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class PromptManager:
    """Manages prompts for different retail scenarios."""
    
    # System prompt template
    SYSTEM_PROMPT = """You are Reachy, a friendly retail assistant robot in {store_id}.

CRITICAL RULES:
1. Keep responses under {max_words} words
2. Use ONLY information from the provided cache
3. Never invent product locations or prices
4. Ask AT MOST one clarifying question per interaction
5. If unsure, offer to get staff help

RESPONSE FORMAT:
- Be warm and helpful
- Be specific about locations (aisle numbers)
- Use simple, conversational language

AVAILABLE DATA:
{cache_context}
"""
    
    USER_PROMPT_TEMPLATE = """Customer query: "{query}"

Available products and locations:
{products}

Active promotions:
{promos}

Respond concisely and helpfully."""
    
    def __init__(self, max_words: int = 35):
        self.max_words = max_words
    
    def build_system_prompt(
        self,
        store_id: str,
        cache_context: str = "Store map, products, and promotions"
    ) -> str:
        """Build system prompt with store context."""
        return self.SYSTEM_PROMPT.format(
            store_id=store_id,
            max_words=self.max_words,
            cache_context=cache_context
        )
    
    def build_user_prompt(
        self,
        query: str,
        products: Optional[List[Any]] = None,
        promos: Optional[List[Any]] = None
    ) -> str:
        """Build user prompt with cache data."""
        products_str = self._format_products(products) if products else "No specific products in cache"
        promos_str = self._format_promos(promos) if promos else "No active promotions"
        
        return self.USER_PROMPT_TEMPLATE.format(
            query=query,
            products=products_str,
            promos=promos_str
        )
    
    def _format_products(self, products: List[Any]) -> str:
        """Format product list for prompt."""
        if not products:
            return "None"
        
        lines = []
        for p in products[:5]:  # Limit to prevent prompt bloat
            lines.append(f"- {p.name} in aisle {p.aisle} ({p.category})")
        return "\n".join(lines)
    
    def _format_promos(self, promos: List[Any]) -> str:
        """Format promo list for prompt."""
        if not promos:
            return "None"
        
        lines = []
        for promo in promos[:3]:  # Limit to top 3
            lines.append(f"- {promo.description}")
        return "\n".join(lines)
    
    def validate_response(self, response: str) -> tuple[bool, Optional[str]]:
        """Validate LLM response meets constraints."""
        word_count = len(response.split())
        
        if word_count > self.max_words * 1.2:  # Allow 20% buffer
            return False, f"Response too long: {word_count} words (max {self.max_words})"
        
        # Check for hallucination indicators
        hallucination_phrases = [
            "i think",
            "probably",
            "might be",
            "could be in",
            "not sure but"
        ]
        
        response_lower = response.lower()
        for phrase in hallucination_phrases:
            if phrase in response_lower:
                logger.warning(f"Potential hallucination detected: '{phrase}' in response")
        
        return True, None
