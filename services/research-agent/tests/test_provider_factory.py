import pytest

from research_agent.config import Settings
from research_agent.exceptions import ProviderError
from research_agent.providers.anthropic import AnthropicProvider
from research_agent.providers.factory import get_provider


def test_get_provider_returns_anthropic():
    settings = Settings(
        llm_provider="anthropic",
        api_key="fake-key-for-test",
        model="claude-sonnet-4-6",
        db_provider="sqlite",
        db_path="unused.db",
    )
    provider = get_provider(settings)
    assert isinstance(provider, AnthropicProvider)


def test_get_provider_unknown_raises():
    settings = Settings(
        llm_provider="unknown-provider",
        api_key="x",
        model="x",
        db_provider="sqlite",
        db_path="unused.db",
    )
    with pytest.raises(ProviderError):
        get_provider(settings)
