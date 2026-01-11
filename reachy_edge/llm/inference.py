"""LLM inference handler."""
import time
import logging
from typing import Optional, Dict, Any
import json

logger = logging.getLogger(__name__)


class LLMInference:
    """Handles LLM inference calls (OpenAI or local)."""
    
    def __init__(
        self,
        mode: str = "openai",
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        temperature: float = 0.0,
        max_tokens: int = 100
    ):
        self.mode = mode
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        if mode == "openai" and not api_key:
            logger.warning("OpenAI mode selected but no API key provided")
        
        self._client = None
        self._init_client()
    
    def _init_client(self) -> None:
        """Initialize LLM client based on mode."""
        if self.mode == "openai":
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
                logger.info(f"Initialized OpenAI client with model {self.model}")
            except ImportError:
                logger.error("OpenAI package not installed. Install with: pip install openai")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        
        elif self.mode == "local":
            # TODO: Initialize local model (llama.cpp, etc.)
            logger.warning("Local LLM mode not yet implemented")
    
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        timeout_s: float = 1.0
    ) -> Optional[str]:
        """Generate response from LLM."""
        if not self._client:
            logger.error("LLM client not initialized")
            return None
        
        start_time = time.time()
        
        try:
            if self.mode == "openai":
                response = await self._generate_openai(system_prompt, user_prompt)
            elif self.mode == "local":
                response = await self._generate_local(system_prompt, user_prompt)
            else:
                logger.error(f"Unknown LLM mode: {self.mode}")
                return None
            
            latency_ms = (time.time() - start_time) * 1000
            
            if latency_ms > timeout_s * 1000:
                logger.warning(f"LLM latency exceeded timeout: {latency_ms:.1f}ms > {timeout_s*1000}ms")
            
            logger.info(f"LLM generation completed in {latency_ms:.1f}ms")
            return response
        
        except Exception as e:
            logger.error(f"LLM generation failed: {e}", exc_info=True)
            return None
    
    async def _generate_openai(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Generate using OpenAI API."""
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return None
    
    async def _generate_local(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Generate using local model."""
        # TODO: Implement local inference
        logger.warning("Local inference not yet implemented")
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get inference statistics."""
        return {
            "mode": self.mode,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "client_initialized": self._client is not None
        }
