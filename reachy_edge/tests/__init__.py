"""Test configuration and initialization."""
import pytest


def test_init():
    """Test module imports."""
    from reachy_edge import __version__
    assert __version__ == "0.1.0"


def test_config_defaults():
    """Test configuration defaults."""
    from reachy_edge.config import settings
    
    assert settings.reachy_id is not None
    assert settings.store_id is not None
    assert settings.max_response_words == 35
    assert settings.llm_temperature == 0.0
