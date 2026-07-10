from ..config import Settings
from ..exceptions import ProviderError
from .anthropic import AnthropicProvider
from .base import LLMProvider

PROVIDERS = {
    "anthropic": AnthropicProvider,
    # "gemini": GeminiProvider,   # belum diimplementasi
    # "ollama": OllamaProvider,   # belum diimplementasi
}


def get_provider(settings: Settings) -> LLMProvider:
    provider_cls = PROVIDERS.get(settings.llm_provider)
    if provider_cls is None:
        raise ProviderError(f"Unknown LLM provider: {settings.llm_provider}")

    return provider_cls(api_key=settings.api_key, model=settings.model)
