"""Text-to-speech adapter stub for Epic 2."""


class TTSAdapter:
    """Minimal TTS interface."""

    def synthesize(self, text: str) -> bytes:
        # Placeholder for provider integration
        return text.encode("utf-8")
