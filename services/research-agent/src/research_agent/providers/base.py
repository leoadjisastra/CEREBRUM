from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Interface buat semua LLM provider (Anthropic, Gemini, Ollama, dll)."""

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Kirim prompt, return teks respons."""
        raise NotImplementedError
