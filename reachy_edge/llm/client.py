"""Provider-agnostic LLM client for cache-only responses."""
from __future__ import annotations

from dataclasses import dataclass

from .inference import LLMInference


@dataclass
class LLMClient:
    provider: str
    model: str
    api_key: str | None = None
    temperature: float = 0.0
    max_tokens: int = 150

    def __post_init__(self) -> None:
        mode = "openai" if self.provider == "openai" else "local"
        self.inference = LLMInference(
            mode=mode,
            api_key=self.api_key,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

    async def generate_response(self, query: str, products: list[dict]) -> str:
        """Generate response with strict cache-only context."""
        system_prompt = (
            "You are Reachy, a helpful retail assistant. "
            "Only use the provided product cache. "
            "Never invent locations or prices. Keep responses under 35 words."
        )
        user_prompt = f"Query: {query}\nProducts: {products}"
        response = await self.inference.generate(system_prompt=system_prompt, user_prompt=user_prompt)
        if not response:
            return "I can help find that item if you share the exact product name."
        words = response.split()
        if len(words) > 35:
            return " ".join(words[:35])
        return response
