from anthropic import Anthropic

from ..exceptions import ProviderError
from .base import LLMProvider


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str):
        if not api_key:
            raise ProviderError("ANTHROPIC_API_KEY belum di-set. Cek file .env")
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
        except Exception as e:
            raise ProviderError(f"Anthropic API call failed: {e}") from e

        return "".join(block.text for block in response.content if hasattr(block, "text"))
